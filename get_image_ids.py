import json
import os
import requests

# 定义全局变量
lastMatchedMoment = 0
realPhotoIndex = 0

# 定义通用的文件操作函数，用于判断文件是否存在并打开文件
def open_file(file_path, mode, encoding='utf-8'):
    if not os.path.exists(file_path):
        print(f"{file_path} 文件不存在，无法进行后续操作。")
        return None
    return open(file_path, mode, encoding=encoding)


# 定义获取图片信息并存储ID的函数
def getinfo_and_store_id(photonum=0, recursion_depth=0, count=0):
    """
    函数功能：
    - 发送请求获取图片信息
    - 递归调用自身，直到获取到足够数量的图片信息
    - 将获取到的图片ID存储到ID.TXT文件中

    参数说明：
    - photonum：需要获取的图片数量，用于判断是否已经获取足够的图片。
    - recursion_depth：递归深度，用于限制递归次数。
    - count：已处理的图片数量，这里是记录获取到的图片个数，用于判断是否结束递归。
    """
    global lastMatchedMoment  # 声明使用全局变量
    global realPhotoIndex  # 声明使用全局变量

    # 使用字典变量存储请求参数
    request_params = {
       'size': '100',
       'state': 'active',
       'smallPhotoScaleParams': 'image/resize,m_mfit,h_250,w_250',
       'originalPhotoScaleParams': 'image/resize,m_mfit,h_1300,w_1300',
	   'cursor': str(lastMatchedMoment),
       'photoIndex': str(realPhotoIndex)
    }


    try:
        # 发送POST请求到获取图片列表的接口
        print(f"请求前request_params: {request_params}")
        response = requests.post('https://cloud.h2os.com/gallery/pc/listNormalPhotos',
                                 headers=headers,
                                 cookies=cookies,
                                 data=request_params)
        response.raise_for_status()
        response_data = response.json()

        # 从接口响应中获取图片数据相关信息
        photos = response_data.get('photos')
        lastMatchedMoment = response_data.get('lastMatchedMoment')  # 更新全局变量
        realPhotoIndex = response_data.get('realPhotoIndex')  # 更新全局变量
        print(f"从服务器获取到的新lastMatchedMoment: {lastMatchedMoment}，新realPhotoIndex: {realPhotoIndex}")


        # 用于存储本次请求获取到的所有图片ID的列表
        current_photo_ids = []

        # 打开ID.TXT文件，以追加模式写入图片ID
        id_file = open_file("ID.TXT", "a")
        if id_file:
            try:
                for key, value in photos.items():
                    for item in value:
                        photo_id = item.get("id")
                        id_file.write(photo_id + "\n")
                        current_photo_ids.append(photo_id)
                        count += 1

                progress = (count / photonum) * 100  # 计算当前进度
                print(f"获取图片ID进度: {progress:.2f}%")
            except IOError as e:
                print(f"向ID.TXT文件写入图片ID时出错: {e}，请检查文件权限或文件是否被占用")
            finally:
                id_file.close()

        # 如果已获取的图片数量小于需要获取的图片数量，且递归深度未超过限制，继续递归调用自身获取更多图片
        if count < photonum and recursion_depth < MAX_RECURSION_DEPTH:
            print(f"即将进行第 {recursion_depth + 1} 次递归调用，传入的lastMatchedMoment: {lastMatchedMoment}，"
                  f"realPhotoIndex: {realPhotoIndex}，photonum: {photonum}，recursion_depth: {recursion_depth}，count: {count}")
            getinfo_and_store_id(photonum, recursion_depth + 1, count)
        elif count < photonum:
            print(f"达到最大递归深度，无法获取足够数量的图片ID。")

    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.ConnectionError):
            print(f"网络错误，尝试重新连接...")
            # 可以在这里添加重试逻辑，例如设置合理的重试次数等
            # 以下是简单示例，设置重试3次
            for _ in range(3):
                try:
                    return getinfo_and_store_id(photonum, recursion_depth, count)
                except requests.exceptions.RequestException as retry_e:
                    if isinstance(retry_e, requests.ConnectionError):
                        continue
                    else:
                        print(f"重试请求获取图片列表出错: {retry_e}")
                        break
            print("多次重试后仍无法连接，程序终止。")
        elif isinstance(e, requests.Timeout):
            print(f"请求超时，请检查网络连接或服务器响应情况，尝试重新运行程序。")
        elif isinstance(e, requests.TooManyRedirects):
            print(f"重定向过多，请检查请求的URL是否正确或服务器配置是否异常。")
        else:
            print(f"请求获取图片列表出错: {retry_e}")


# 定义cookies字典，用于模拟登录状态等信息
cookies = {
    # 填入实际的cookies信息，示例：
   
}
# 定义headers字典，包含了User-Agent和Content-Type等信息
headers = {
    # 填入实际的headers信息，示例：
    
}

# 需要获取的图片数量
photonum = 2493

# 最大递归深度=photonum / 7 + 20
MAX_RECURSION_DEPTH = 370

# 调用函数进行图片ID获取与存储
getinfo_and_store_id(photonum=photonum)
print("图片ID获取并存储完毕")