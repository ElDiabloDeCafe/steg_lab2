import sys

import utilities
import struct

def read_bmp_headers(file_path):
    with open(file_path, 'rb') as bmp_file:
        bmp_header = bmp_file.read(14)  # Заголовок BMP (14 байт)
        header_fields = struct.unpack('<2sIHHI', bmp_header)

        dib_header = bmp_file.read(40)  # Заголовок DIB (40 байт)
        dib_fields = struct.unpack('<IIIHHIIIIII', dib_header)

        return header_fields, dib_fields

# Для записи заголовков для новой картинки
def write_bmp_headers(bmp_file, header_fields, dib_fields):
    bmp_header = struct.pack('<2sIHHI', header_fields[0], header_fields[1],
                             header_fields[2], header_fields[3],
                             header_fields[4])
    bmp_file.write(bmp_header)

    dib_header = struct.pack('<IIIHHIIIIII', dib_fields[0], dib_fields[1],
                             dib_fields[2], dib_fields[3],
                             dib_fields[4], dib_fields[5],
                             dib_fields[6], dib_fields[7],
                             dib_fields[8], dib_fields[9],
                             dib_fields[10])
    bmp_file.write(dib_header)

#Перевод из буковок в аски
def text_to_ascii_decimal(text):
    if len(text) > 12:
        raise ValueError("Текст должен быть не длиннее 12 символов.")
    ascii_values = ''.join(str(ord(char)) for char in text)
    print (int(ascii_values))
    return int(ascii_values)

def ascii_decimal_to_text(ascii_value, length):
    return ''.join(chr(int(ascii_value[i:i+2])) for i in range(0, length * 2, 2))
def modify_reserved_and_save(input_file_path, output_file_path, new_reserved_text):
    header_fields, dib_fields = read_bmp_headers(input_file_path)

    reserved1_text = new_reserved_text[:2]
    reserved2_text = new_reserved_text[2:4]
    x_text = new_reserved_text[4:8]
    y_text = new_reserved_text[8:12]
    new_reserved1_value = text_to_ascii_decimal(reserved1_text)
    new_reserved2_value = text_to_ascii_decimal(reserved2_text)
    new_x_text = text_to_ascii_decimal(x_text)
    new_y_text = text_to_ascii_decimal(y_text)

    header_fields = list(header_fields)
    header_fields[2] = new_reserved1_value
    header_fields[3] = new_reserved2_value

    dib_fields = list(dib_fields)
    dib_fields[7] = new_x_text
    dib_fields[8] = new_y_text

    with open(output_file_path, 'wb') as bmp_file:
        write_bmp_headers(bmp_file, header_fields, dib_fields)

        with open(input_file_path, 'rb') as input_file:
            input_file.seek(54)
            bmp_data = input_file.read()
            bmp_file.write(bmp_data)

    print(f"Изменённый BMP файл сохранён как: {output_file_path}")

    """
    В res1 и res2 по 2 буквы, в x и y по 4 букв, итого 12. ЛАТИНИЦА КАПСОМ!
    """

def decode (input_file_path):
    header_fields, dib_fields = read_bmp_headers(input_file_path)

    reserved1_value = header_fields[2]
    reserved2_value = header_fields[3]
    x_text_value = dib_fields[7]
    y_text_value = dib_fields[8]

    reserved1_value = ascii_decimal_to_text(str(reserved1_value),2)
    reserved2_value = ascii_decimal_to_text(str(reserved2_value), 2)
    x_text = ascii_decimal_to_text(str(x_text_value),4)
    y_text = ascii_decimal_to_text(str(y_text_value), 4)

    final_text = reserved1_value + reserved2_value + x_text + y_text
    print(f"Полученный текст:{final_text}")


action = input("Выберите действие (encode/decode): ").strip().lower()

if action == "encode":
    new_reserved_text = input("Введите текст для сокрытия (не более 12 символов): ")
    new_reserved_text = utilities.lovushka_na_duraka(new_reserved_text)
    input_file_path = utilities.open_file_dialog("Выберите BMP файл для кодирования")

    output_file_path = utilities.save_file_dialog("Сохраните новый BMP файл")

    modify_reserved_and_save(input_file_path, output_file_path, new_reserved_text)

    new_header_fields, new_dib_fields = read_bmp_headers(output_file_path)
    print(f"Новое значение Reserved1: {new_header_fields[2]} (в десятичной системе)")
    print(f"Новое значение Reserved2: {new_header_fields[3]} (в десятичной системе)")
    print(f"Новое значение X Pixels per Meter: {new_dib_fields[7]} (в десятичной системе)")
    print(f"Новое значение Y Pixels per Meter: {new_dib_fields[8]} (в десятичной системе)")

elif action == "decode":
    input_file_path = utilities.open_file_dialog("Выберите BMP файл для декодирования")
    decode(input_file_path)
else:
    print("Неверное действие. Пожалуйста, выберите 'encode' или 'decode'.")

