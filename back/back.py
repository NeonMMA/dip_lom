from io import StringIO

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS, cross_origin
from dateutil import parser as date_parser  # для автоматического распознавания форматов дат
from exif_control import getExif, checkHEIC


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'

jwt = JWTManager(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Проверяем, что файл был отправлен
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    uploaded_file = request.files['file']
    content_type = uploaded_file.content_type
    
    # Обработка в зависимости от типа файла
    if content_type == 'image/heic':
        # Сохраняем временно файл для обработки HEIC
        temp_path = "./temp_heic.heic"
        uploaded_file.save(temp_path)
        res = checkHEIC(temp_path)
        # Здесь можно добавить удаление временного файла
        return jsonify(res), 200
        
    elif content_type == 'image/jpeg':
        file_bytes = uploaded_file.read()
        res = getExif(file_bytes)
        return jsonify(res), 200
        
    else:
        return jsonify({"error": "Unsupported file type"}), 400


@app.route('/check', methods=['POST'])
@cross_origin()
def check_fast_api():
    data = request.get_json()
    print(data)
    return jsonify({"message": "ALL GOOOOOD in check"}), 200


print(__name__)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)