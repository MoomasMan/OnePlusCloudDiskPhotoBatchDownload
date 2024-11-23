import os
import requests


# 定义通用的文件操作函数，用于判断文件是否存在并打开文件
def open_file(file_path, mode, encoding='utf-8'):
    if not os.path.exists(file_path):
        print(f"{file_path} 文件不存在，无法进行后续操作。")
        return None
    return open(file_path, mode, encoding=encoding)


def get_urls_and_store():
    # 打开ID.TXT文件读取图片ID
    id_file = open_file("ID.TXT", "r")
    if not id_file:
        return

    count = 0
    total_ids = 0
    with id_file:
        ids = id_file.readlines()
        total_ids = len(ids)
    with open_file("URL.TXT", "a") as url_file:
        if url_file:
            for photo_id in ids:
                photo_id = photo_id.strip()
                try:
                    # 发送POST请求到获取真实图片URL的接口
                    real = requests.post('https://cloud.h2os.com/gallery/pc/getRealPhotoUrls',
                                         headers=headers,
                                         cookies=cookies,
                                         data='ids=["' + photo_id + '"]')
                    real.raise_for_status()
                    real_data = real.json()
                    img_url = real_data.get(photo_id)
                    # 将图片ID和URL写入文件，每行格式为 "ID,URL"
                    url_file.write(f"{photo_id},{img_url}\n")
                    count += 1
                    progress = (count / total_ids) * 100
                    print(f"获取URL进度: {progress:.2f}%")
                except requests.exceptions.RequestException as e:
                    print(f"请求获取图片 {photo_id} 的真实URL时出错: {e}")
    print("图片URL获取并存储完毕。")


# 定义cookies字典，用于模拟登录状态等信息
cookies = {
    # 填入实际的cookies信息，示例：
    
}
# 定义headers字典，包含了User-Agent和Content-Type等信息
headers = {
    # 填入实际的headers信息，示例：
   
}

get_urls_and_store()