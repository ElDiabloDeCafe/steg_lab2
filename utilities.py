import tkinter as tk
from tkinter import filedialog
import sys
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
