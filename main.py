import cv2
from tkinter import Tk, Button, Label, filedialog, StringVar, OptionMenu
from PIL import Image, ImageTk

class ImageDenoiser:
    def __init__(self, master):
        self.master = master
        master.title("Görüntü Gürültü Giderme Uygulaması")

        self.label = Label(master, text="Bir görüntü yükleyin:")
        self.label.pack()

        self.load_button = Button(master, text="Görüntü Yükle", command=self.load_image)
        self.load_button.pack()

        self.filter_option = StringVar(master)
        self.filter_option.set("Median")  # Default value
        self.filter_menu = OptionMenu(master, self.filter_option, "Median", "Gaussian", "Bilateral")
        self.filter_menu.pack()

        self.denoise_button = Button(master, text="Gürültüyü Gider", command=self.denoise_image, state='disabled')
        self.denoise_button.pack()

        self.save_button = Button(master, text="Görüntüyü Kaydet", command=self.save_image, state='disabled')
        self.save_button.pack()

        self.original_image_label = Label(master)
        self.original_image_label.pack(side='left')

        self.denoised_image_label = Label(master)
        self.denoised_image_label.pack(side='right')

        self.image_path = None
        self.original_image = None

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            self.original_image = cv2.imread(self.image_path)
            self.show_image(self.original_image, self.original_image_label)
            self.denoise_button.config(state='normal')

    def show_image(self, image, label):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        label.config(image=image)
        label.image = image

    def denoise_image(self):
        if self.original_image is not None:
            filter_type = self.filter_option.get()
            if filter_type == "Median":
                denoised_image = cv2.medianBlur(self.original_image, 5)
            elif filter_type == "Gaussian":
                denoised_image = cv2.GaussianBlur(self.original_image, (5, 5), 0)
            elif filter_type == "Bilateral":
                denoised_image = cv2.bilateralFilter(self.original_image, 9, 75, 75)
            self.show_image(denoised_image, self.denoised_image_label)
            self.save_button.config(state='normal')

    def save_image(self):
        if self.denoised_image_label.image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                       filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
            if save_path:
                denoised_image = cv2.cvtColor(cv2.imread(self.image_path), cv2.COLOR_BGR2RGB)  # Reconvert to RGB
                cv2.imwrite(save_path, denoised_image)

if __name__ == "__main__":
    root = Tk()
    app = ImageDenoiser(root)
    root.mainloop()

