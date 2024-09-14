import os
import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import openpyxl
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.DEBUG)

NGROK_URL = os.environ.get('NGROK_URL')

@app.route('/')
def index():
    base_url = NGROK_URL or request.url_root.rstrip('/')
    app.logger.info(f"Accessed index page. Remote addr: {request.remote_addr}, Base URL: {base_url}")
    return render_template('index.html', base_url=base_url)

@app.route('/sign_in')
def sign_in():
    user_agent = request.headers.get('User-Agent')
    app.logger.info(f"Received sign_in request. User-Agent: {user_agent}, Remote addr: {request.remote_addr}")
    if 'Mobile' in user_agent:
        return render_template('sign_in.html')
    else:
        return redirect(url_for('index'))

@app.route('/test')
def test():
    return jsonify({"status": "ok", "message": "Server is running"})

@app.route('/submit_login', methods=['POST'])
def submit_login():
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    phone = request.form.get('phone')

    # 打开现有的 Excel 文件或创建新文件
    try:
        workbook = openpyxl.load_workbook('user_data.xlsx')
        sheet = workbook.active
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['时间', '姓名', '学号', '手机号'])

    # 添加新行
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append([now, name, student_id, phone])

    # 保存文件
    workbook.save('user_data.xlsx')

    return jsonify({"success": True, "message": "数据已成功保存"})

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {str(e)}", exc_info=True)
    return "An error occurred", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)