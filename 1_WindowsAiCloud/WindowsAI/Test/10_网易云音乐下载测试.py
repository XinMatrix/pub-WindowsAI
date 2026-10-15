import requests

url = 'https://d1.music.126.net/dmusic/NeteaseCloudMusic_Music_official_3.0.0.Beta.03.25.202691.64.exe'  # 替换为要下载的文件的URL
filename = '网易云音乐.exe'  # 替换为保存的文件名

response = requests.get(url, stream=True)
response.raise_for_status()

with open(filename, 'wb') as file:
    for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)

print('文件下载完成')
