import struct

def read_bmp_headers(file_path):
    with open(file_path, 'rb') as bmp_file:
        # Читаем заголовок BMP
        bmp_header = bmp_file.read(14)  # Заголовок BMP (14 байт)
        header_fields = struct.unpack('<2sIHHI', bmp_header)

        # Читаем заголовок DIB
        dib_header = bmp_file.read(40)  # Заголовок DIB (40 байт)
        dib_fields = struct.unpack('<IIIHHIIIIII', dib_header)

        return header_fields, dib_fields

# Для записи заголовков для новой картинки
def write_bmp_headers(bmp_file, header_fields, dib_fields):
    # Записываем заголовок BMP
    bmp_header = struct.pack('<2sIHHI', header_fields[0], header_fields[1],
                             header_fields[2], header_fields[3],
                             header_fields[4])
    bmp_file.write(bmp_header)

    # Записываем заголовок DIB
    dib_header = struct.pack('<IIIHHIIIIII', dib_fields[0], dib_fields[1],
                             dib_fields[2], dib_fields[3],
                             dib_fields[4], dib_fields[5],
                             dib_fields[6], dib_fields[7],
                             dib_fields[8], dib_fields[9],
                             dib_fields[10])
    bmp_file.write(dib_header)

#Перевод из буковок в аски
def text_to_ascii_decimal(text):
    if len(text) > 4:
        raise ValueError("Текст должен быть не длиннее 4 символов.")
    ascii_values = ''.join(str(ord(char)) for char in text)
    return int(ascii_values)

def modify_reserved_and_save(input_file_path, output_file_path, new_reserved_text):
    # Читаем заголовки
    header_fields, dib_fields = read_bmp_headers(input_file_path)


    reserved1_text = new_reserved_text[:2]  # Первые 2 символа для Reserved1
    reserved2_text = new_reserved_text[2:4]  # Следующие 2 символа для Reserved2

    new_reserved1_value = text_to_ascii_decimal(reserved1_text)  # Преобразуем текст в десятичное значение
    new_reserved2_value = text_to_ascii_decimal(reserved2_text)  # Преобразуем текст в десятичное значение

    header_fields = list(header_fields)  # Преобразуем кортеж в список для изменения
    header_fields[2] = new_reserved1_value  # Изменяем Reserved1
    header_fields[3] = new_reserved2_value  # Изменяем Reserved2

    # Открываем новый файл для записи
    with open(output_file_path, 'wb') as bmp_file:
        # Записываем измененные заголовки
        write_bmp_headers(bmp_file, header_fields, dib_fields)

        # Копируем данные изображения
        with open(input_file_path, 'rb') as input_file:
            input_file.seek(54)  # Пропускаем заголовкиdssdsdsdsdsds
            bmp_data = input_file.read()  # Читаем все данные изображения
            bmp_file.write(bmp_data)  # Записываем данные в новый файл

    print(f"Изменённый BMP файл сохранён как: {output_file_path}")

# Пример использования (4 для xy)
input_file_path = 'F:\\Учёба\\4 курс\\Стеганография\\Лаб2\\Программа\\lab2_steg\\steg_lab2\\bmp\\container.bmp'  # Укажите путь к вашему BMP файлу
output_file_path = 'F:\\Учёба\\4 курс\\Стеганография\\Лаб2\\Программа\\lab2_steg\\steg_lab2\\bmp\\modified_container.bmp'  # Путь для сохранения нового BMP файла
new_reserved_text = 'XDDD'  # Новый текст для Reserved1 и Reserved2

modify_reserved_and_save(input_file_path, output_file_path, new_reserved_text)

# Читаем и выводим новые значения Reserved1 и Reserved2
new_header_fields, _ = read_bmp_headers(output_file_path)
print(f"Новое значение Reserved1: {new_header_fields[2]} (в десятичной системе)")
print(f"Новое значение Reserved2: {new_header_fields[3]} (в десятичной системе)")
# import struct
#
#
# def read_bmp_headers(file_path):
#     with open(file_path, 'rb') as bmp_file:
#         # Читаем заголовок BMP
#         bmp_header = bmp_file.read(14)  # Заголовок BMP (14 байт)
#         header_fields = struct.unpack('<2sIHHI', bmp_header)
#
#         # Читаем заголовок DIB
#         dib_header = bmp_file.read(40)  # Заголовок DIB (40 байт)
#         dib_fields = struct.unpack('<IIIHHIIIIII', dib_header)
#
#         # Выводим заголовки
#         print("BMP Header:")
#         print(f"  Signature: {header_fields[0].decode('utf-8')}")
#         print(f"  File Size: {header_fields[1]}")
#         print(f"  Reserved1: {header_fields[2]}") 2 буквы
#         print(f"  Reserved2: {header_fields[3]}") 2 буквы
#         print(f"  Offset: {header_fields[4]}")
#
#         print("\nDIB Header:")
#         print(f"  Header Size: {dib_fields[0]}")
#         print(f"  Image Width: {dib_fields[1]}")
#         print(f"  Image Height: {dib_fields[2]}")
#         print(f"  Planes: {dib_fields[3]}")
#         print(f"  Bits per Pixel: {dib_fields[4]}")
#         print(f"  Compression: {dib_fields[5]}")
#         print(f"  Image Size: {dib_fields[6]}")
#         print(f"  X Pixels per Meter: {dib_fields[7]}") 5 букв
#         print(f"  Y Pixels per Meter: {dib_fields[8]}") 5 букв
#         print(f"  Total Colors: {dib_fields[9]}")
#         print(f"  Important Colors: {dib_fields[10]}")
#
#
# # Пример использования
# file_path = 'F:\\Учёба\\4 курс\\Стеганография\\Лаб2\\Программа\\lab2_steg\\bmp\\modified_container.bmp'  # Укажите путь к вашему BMP файлу
# read_bmp_headers(file_path)

