from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pyzbar.pyzbar import decode
from PIL import Image
import io
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Обязательно измените на свой ключ

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    # Проверяем, есть ли файл в запросе
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    # Проверяем, что файл не пустой
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Читаем изображение прямо из памяти без сохранения на диск
        img = Image.open(io.BytesIO(file.read()))
        
        # Конвертируем в формат, который понимает pyzbar
        img = img.convert('RGB')
        
        # Распознаем штрих-коды
        barcodes = decode(img)
        
        if barcodes:
            barcode_data = barcodes[0].data.decode('utf-8')
            session['barcode_data'] = barcode_data
            return jsonify({'success': True, 'redirect': url_for('result')})
        else:
            return jsonify({'error': 'Barcode not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/result')
def result():
    barcode_data = session.get('barcode_data')
    if barcode_data:
        return render_template('result.html', barcode=barcode_data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)