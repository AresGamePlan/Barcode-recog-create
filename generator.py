# import barcode
# from barcode.writer import ImageWriter
# from PIL import Image
# import os

# def generate_barcode(data, barcode_type='code128', output_dir='output'):
#     # Создаем директорию, если ее нет
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     # Генерируем штрих-код
#     code = barcode.get(barcode_type, data, writer=ImageWriter())
    
#     # Сохраняем изображение
#     filename = f"{output_dir}/{data}"
#     code.save(filename)
    
#     print(f"Штрих-код сохранен как {filename}.png")
#     # Открываем изображение для просмотра
#     img = Image.open(f"{filename}.png")
#     img.show()

# if __name__ == "__main__":
#     data = input("Введите данные для штрих-кода: ")
#     generate_barcode(data)

import barcode
from barcode.writer import ImageWriter
from PIL import Image
import os

def generate_barcode(data, barcode_type='code128', output_dir='output'):
    # Создаем директорию, если ее нет
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Генерируем штрих-код, принудительно используя указанный тип
        code = barcode.get(barcode_type, data, writer=ImageWriter())
        
        # Сохраняем изображение
        filename = f"{output_dir}/code"
        code.save(filename)
        
        print(f"Штрих-код сохранен как {filename}.png")
        
        # Открываем изображение для просмотра
        img = Image.open(f"{filename}.png")
        img.show()
    
    except barcode.errors.BarcodeError as e:
        print(f"Ошибка: Невозможно создать штрих-код типа {barcode_type} с данными '{data}': {e}")

if __name__ == "__main__":
    data = input("Введите данные для штрих-кода: ")
    strings = data.split()
    data = ""
    for i in strings:
        if strings[len(strings) - 1] != i:
            data += i + "\n"
        else:
            data += i
    generate_barcode(data)