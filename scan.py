# import cv2
# from pyzbar import pyzbar

# def scan_barcode():
#     cap = cv2.VideoCapture(0)  # Используем камеру по умолчанию
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Не удалось получить изображение с камеры.")
#             break
        
#         # Ищем штрих-коды на кадре
#         barcodes = pyzbar.decode(frame)
        
#         for barcode in barcodes:
#             # Извлекаем данные и тип штрих-кода
#             barcode_data = barcode.data.decode("utf-8")
#             barcode_type = barcode.type
#             print(f"Найден штрих-код типа {barcode_type}: {barcode_data}")
            
#             # Рисуем прямоугольник вокруг штрих-кода
#             (x, y, w, h) = barcode.rect
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
#             # Выводим текст с данными штрих-кода
#             cv2.putText(frame, barcode_data, (x, y - 10), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
#             # Показываем последний кадр с обнаруженным штрих-кодом
#             cv2.imshow("Сканер штрих-кода", frame)
#             cv2.waitKey(2000)  # Задержка 2 секунды
            
#             # Освобождаем ресурсы камеры и закрываем окна
#             cap.release()
#             cv2.destroyAllWindows()
#             return  # Выходим из функции после первого найденного штрих-кода
        
#         # Показываем кадр
#         cv2.imshow("Сканер штрих-кода", frame)
        
#         # Выход по нажатию 'q'
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     scan_barcode()

# from flask import Flask, render_template, request, jsonify
# import cv2
# import numpy as np
# from pyzbar.pyzbar import decode
# import tempfile
# import os
# from time import time

# app = Flask(__name__)

# # Конфигурация
# app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB лимит
# ALLOWED_EXTENSIONS = {'webp', 'jpg', 'jpeg', 'png'}

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def process_image(file_path):
#     """Обработка изображения и распознавание штрих-кода"""
#     try:
#         # Чтение с проверкой формата
#         img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
#         if img is None:
#             return None, "Invalid image format"
        
#         # Улучшение контраста (CLAHE)
#         clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#         enhanced = clahe.apply(img)
        
#         # Детектирование штрих-кодов
#         barcodes = decode(enhanced)
        
#         if not barcodes:
#             # Попробуем с оригинальным изображением
#             barcodes = decode(img)
        
#         if barcodes:
#             return barcodes, None
#         return None, "No barcodes found"
    
#     except Exception as e:
#         return None, str(e)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/scan', methods=['POST'])
# def scan_barcode():
#     if 'image' not in request.files:
#         return jsonify({'success': False, 'error': 'No image provided'}), 400
    
#     file = request.files['image']
#     if not file or file.filename == '':
#         return jsonify({'success': False, 'error': 'Empty file'}), 400
    
#     if not allowed_file(file.filename):
#         return jsonify({'success': False, 'error': 'Unsupported file type'}), 400
    
#     # Сохраняем во временный файл
#     temp_fd, temp_path = tempfile.mkstemp()
#     try:
#         file.save(temp_path)
        
#         # Обработка изображения
#         barcodes, error = process_image(temp_path)
        
#         if error:
#             return jsonify({'success': False, 'error': error}), 400
        
#         if barcodes:
#             # Возвращаем все найденные штрих-коды
#             results = []
#             for barcode in barcodes:
#                 try:
#                     data = barcode.data.decode('utf-8')
#                 except UnicodeDecodeError:
#                     data = barcode.data.hex()
                
#                 results.append({
#                     'barcode': data,
#                     'type': barcode.type,
#                     'quality': barcode.quality,
#                     'rect': [(p.x, p.y) for p in barcode.polygon]
#                 })
            
#             return jsonify({
#                 'success': True,
#                 'barcodes': results,
#                 'count': len(results)
#             })
        
#         return jsonify({'success': False, 'error': 'Barcode not detected'}), 404
    
#     finally:
#         os.close(temp_fd)
#         os.unlink(temp_path)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, threaded=True)

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)  # Разрешаем CORS для всех доменов

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate():
    return render_template('generate.html')

@app.route('/scan', methods=['POST'])
def handle_scan():
    data = request.json
    print(f"Received scan: {data}")  # Выводим в консоль сервера

    # Здесь можно добавить сохранение в базу данных
    # Например:
    # db.save_scan(data['code'], data['code_type'])

    # return jsonify({
    #     'status': 'success',
    #     'message': 'Scan received',
    #     'received_data': data
    # })
    return render_template('out.html',message = data)

@app.route('/out')
def show_data():
    data = request.json


    return render_template('out.html',message = data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)