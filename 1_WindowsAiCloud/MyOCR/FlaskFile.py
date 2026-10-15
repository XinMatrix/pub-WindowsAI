import os
import subprocess
import socket
from flask import Flask, request, send_from_directory, render_template_string

# 初始化 Flask 应用
app = Flask(__name__)
# 设置上传文件夹路径（默认为用户桌面的 "SharedFolder" 文件夹）
UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop", "SharedFolder")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 创建共享文件夹并设置权限（适用于 Windows）
def setup_shared_folder():
    # 检查文件夹是否存在
    if not os.path.exists(UPLOAD_FOLDER):
        # 创建文件夹
        os.makedirs(UPLOAD_FOLDER)
        print(f"创建了共享文件夹，路径为: {UPLOAD_FOLDER}")
        try:
            # 设置文件夹权限，使得所有用户都可以读写
            print(f"正在设置文件夹权限...")
            subprocess.run(["icacls", UPLOAD_FOLDER, "/grant", "Everyone:(OI)(CI)(F)"], check=True)
            print("文件夹权限已成功设置。")
        except subprocess.CalledProcessError as e:
            print(f"设置权限失败: {e}")
    else:
        print(f"共享文件夹已存在，路径为: {UPLOAD_FOLDER}")


# Flask 路由：处理文件上传
@app.route('/upload', methods=['POST'])
def upload_file():
    print("接收到上传请求...")
    # 检查是否有文件上传
    if 'file' not in request.files:
        print("上传失败：没有文件部分。")
        return '没有文件上传', 400
    file = request.files['file']
    # 检查文件是否有有效名称
    if file.filename == '':
        print("上传失败：未选择文件。")
        return '未选择文件', 400
    # 保存文件到指定的上传文件夹
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)
    print(f"文件 {file.filename} 上传成功，保存路径为: {save_path}")
    return '文件上传成功', 200


# Flask 路由：处理文件下载
@app.route('/files/<filename>')
def download_file(filename):
    print(f"请求下载文件: {filename}")
    # 从共享文件夹中提供文件下载
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Flask 路由：显示共享文件列表
@app.route('/')
def list_files():
    # 列出共享文件夹中的所有文件
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [f for f in files if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    # 生成文件链接列表
    file_links = ''.join([f'<li><a href="/files/{file}">{file}</a></li>' for file in files])
    # 渲染 HTML 页面显示文件列表
    html = f'''
    <!doctype html>
    <html>
    <head><title>文件列表</title></head>
    <body>
        <h1>共享文件</h1>
        <ul>
            {file_links}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(html)


# 主程序入口
if __name__ == '__main__':
    setup_shared_folder()
    # 获取主机名和 IP 地址
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    port = 5000
    # 启动 Flask 应用，监听所有网络接口
    app.run(host='0.0.0.0', port=port, debug=True)

# TODO: 使用 pyinstaller 打包应用为单文件：pyinstaller --onefile FlaskTest.py
