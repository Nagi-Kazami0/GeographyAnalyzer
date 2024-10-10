from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder='.')  # 指定當前目錄作為靜態檔案目錄
CORS(app)  # 啟用CORS，允許所有來源訪問

# 連接到本地的 MongoDB 資料庫
client = MongoClient('mongodb+srv:///////////////////////////////&appName=GeoData')
db = client['////////////////']  # 資料庫名稱
locations_collection = db['///////////////////']  # 集合名稱

# 提供首頁路由，返回 googlemapsapi.html
@app.route('/')
def serve_homepage():
    return send_from_directory(app.static_folder, 'googlemapsapi.html')

# POST 接口，用於儲存地理資料
@app.route('/locations', methods=['POST'])
def save_location():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'fail', 'message': '無效資料'}), 400
    
    locations_collection.insert_one(data)
    return jsonify({'status': 'success'}), 201

# GET 接口，用於獲取地理資料
@app.route('/locations', methods=['GET'])
def get_locations():
    locations = list(locations_collection.find({}, {'_id': 0}))
    return jsonify({'status': 'success', 'locations': locations}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  
