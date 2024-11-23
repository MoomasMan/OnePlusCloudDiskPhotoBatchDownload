import os
import requests
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor


# 定义通用的文件操作函数，用于判断文件是否存在并打开文件
def open_file(file_path, mode, encoding='utf-8'):
    if not os.path.exists(file_path):
        print(f"{file_path} 文件不存在，无法进行后续操作。")
        return None
    return open(file_path, mode, encoding=encoding)


def download_image(img_id, img_url):
    """
    单个图片下载的函数，用于在线程中执行
    """
    try:
        response_img = requests.get(img_url)
        response_img.raise_for_status()
        os.makedirs(os.path.dirname(f"PNG\\{img_id}.png"), exist_ok=True)
        with open(f"PNG\\{img_id}.png", "wb") as code:
            code.write(response_img.content)
        print(f"图片 {img_id} 下载成功")
    except requests.exceptions.RequestException as e:
        print(f"下载图片 {img_id} 时出错: {e}")


def download_images_from_file():
    # 打开URL.TXT文件读取图片ID和URL
    url_file = open_file("URL.TXT", "r")
    if not url_file:
        return

    all_groups = []
    group = []
    for line in url_file.readlines():
        line = line.strip()
        if line:
            group.append(line)
        else:
            if group:
                all_groups.append(group)
                group = []
    if group:
        all_groups.append(group)

    with ThreadPoolExecutor(max_workers=5) as executor:  # 创建线程池，最大线程数为5
        for index, group in enumerate(all_groups):
            tasks = []
            if len(group) < 5:
                for item in group:
                    img_id, img_url = item.split(",")
                    tasks.append(executor.submit(download_image, img_id, img_url))
            else:
                for item in group:
                    img_id, img_url = item.split(",")
                    tasks.append(executor.submit(download_image, img_id, img_url))
            # 等待当前组所有线程任务完成
            concurrent.futures.wait(tasks)
            print(f"第 {index + 1} 组图片下载完毕")

    print("所有图片下载完毕。")


download_images_from_file()