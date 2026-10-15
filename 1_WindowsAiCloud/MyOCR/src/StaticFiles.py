import glob
import os

from flask import Flask, send_file, abort, jsonify

from DataFile import local_data

app = Flask(__name__)


# 定义路由，返回本地数据，测试用
# @app.route('/data', methods=['GET'])
# def get_data():
#     return jsonify(local_data)


@app.route('/', methods=['GET'])
def showHello():
    temp_str = 'gitee.com 账号 aYOUR_PHONE 密码 AA2231197878CXcx<br>ce.bktencent.com 账号 3210932037X 密码 -4$AwR1pA*@6tL6ahOst'
    # temp_str = 'JuK56lxkTmTpKz7b8ruy'
    return temp_str
    # return 'Hello Word!'


@app.route('/download', methods=['GET'])
def download():
    return send_file('Local/BlueKingProject.zip')
    # return send_file('Local/WindowsAiChat.exe')


@app.route('/download_file/<file_name>', methods=['GET'])
def download_file(file_name):
    file_path_pattern = os.path.join('static/file', file_name)  # 使用完整搜索
    matching_files = glob.glob(file_path_pattern)
    if matching_files:
        file_path = matching_files[0]
        print(f'found file: {file_path}')
        return send_file(file_path, as_attachment=True)
    else:
        return abort(404, description="File not found")


@app.route('/download_program/<program_name>', methods=['GET'])
def download_program(program_name):
    file_path_pattern = os.path.join('static/program', program_name)  # 使用完整搜索
    matching_files = glob.glob(file_path_pattern)
    if matching_files:
        file_path = matching_files[0]
        print(f'found program: {file_path}')
        return send_file(file_path, as_attachment=True)
    else:
        return abort(404, description="Program not found")


@app.route('/download_project/<project_name>', methods=['GET'])
def download_project(project_name):  # Sample_YOLOv8.zip
    folder_path = os.path.join('static/project', project_name)
    matching_files = glob.glob(folder_path)
    if matching_files:
        file_path = matching_files[0]
        print(f'found project: {file_path}')
        return send_file(file_path, as_attachment=True)
    else:
        return abort(404, description="File not found")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002)
    # app.run('127.0.0.1', port=5002)
