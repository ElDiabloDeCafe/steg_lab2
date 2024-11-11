import tkinter as tk
from tkinter import filedialog
import sys
from PIL import Image
import numpy as np
def open_file_dialog(title):
    root = tk.Tk()
    root.title(title)
    root.geometry('0x0')
    root.update()
    file_path = filedialog.askopenfilename(parent=root, title=title)
    root.destroy()
    return file_path


def save_file_dialog(title):
    root = tk.Tk()
    root.title(title)
    root.geometry('0x0')
    root.update()
    file_path = filedialog.asksaveasfilename(parent=root, title=title, defaultextension=".bmp")
    root.destroy()
    return file_path

def lovushka_na_duraka(new_reserved_text):
    new_reserved_text = new_reserved_text.upper()
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if (len(new_reserved_text) > 12):
        print("Текст превышает 12 символов")
        sys.exit()
    if (len(new_reserved_text) < 12):
        print("Т.к. текст был меньше 12 символов, он будет дополнён до нужной длинны")
        new_reserved_text = new_reserved_text.ljust(12, 'W')
        new_reserved_text = new_reserved_text.upper()
        print(f"Новый текст: {new_reserved_text}")
    if any(char.isdigit() for char in new_reserved_text):
        print("Текст не должен содержать цифры")
        sys.exit()
    if not all(char in allowed for char in new_reserved_text):
        print("Текст должен содержать только заглавные латинские буквы")
        sys.exit()

    bit_count = len(new_reserved_text)*8
    print(f"Кол-во вставленных бит равняется = {bit_count}")
    return new_reserved_text


def calculate_psnr(image1_path, image2_path):
    # Открываем изображения
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    img1_array = np.array(img1)
    img2_array = np.array(img2)

    if img1_array.shape != img2_array.shape:
        print("Изображения должны быть одного размера для вычисления PSNR.")
        return None

    #MSE (Mean Squared Error)
    mse = np.mean((img1_array - img2_array) ** 2)
    if mse == 0:
        return float('inf')  # PSNR бесконечен, если изображения идентичны!!!!

    #PSNR
    max_pixel_value = 255.0
    psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
    return psnr


def open_and_compare_images():
    print("Выберите первое BMP изображение:")
    image1_path = open_file_dialog("Выберите первое BMP изображение")

    print("Выберите второе BMP изображение:")
    image2_path = open_file_dialog("Выберите второе BMP изображение")

    psnr_value = calculate_psnr(image1_path, image2_path)
    if psnr_value is not None:
        print(f"PSNR между изображениями: {psnr_value:.2f} dB")
