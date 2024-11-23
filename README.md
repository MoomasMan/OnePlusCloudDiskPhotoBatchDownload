# OnePlusCloudDiskPhotoBatchDownload

# 用于一加云盘照片批量下载


### 1.进入照片列表页面

![1732380651753.png](https://github.com/MoomasMan/OnePlusCloudDiskPhotoBatchDownload/tree/main/IMG/1732380651753.png)

### 2.通过f12抓到这个请求

![1732380923873.png](https://github.com/MoomasMan/OnePlusCloudDiskPhotoBatchDownload/tree/main/IMG/1732380923873.png)


### 3.右键复制为cURL(bash) 这是edge的用法

![1732381122018.png](https://github.com/MoomasMan/OnePlusCloudDiskPhotoBatchDownload/tree/main/IMG/1732381122018.png)

### 4.进入 [爬虫工具库-spidertools.cn](https://spidertools.cn/#/curl2Request) copy进去 

![1732381122032.png](https://github.com/MoomasMan/OnePlusCloudDiskPhotoBatchDownload/tree/main/IMG/1732381122032.png)

### 5.取 cookie与 headers 的内容复制到 get_image_ids.py 和 get_image_urls.py 代码文件中 

![1732384351249.png](https://github.com/MoomasMan/OnePlusCloudDiskPhotoBatchDownload/tree/main/IMG/1732384351249.png)

### 6.PYthon环境准备与脚本运行

```powershell
	#安装依赖
	pip install requests
	pip install jsonpath-python
	pip install Image
	pip install ByteIO


  ##脚本未设计文件创建相关代码，运行脚本时注意相关文件创建

1.先运行 get_image_ids.py 获取照片ID列表，写入文件ID.TXT

2.再去运行 get_image_urls.py 获取照片真实URL列表，写入文件URL.TXT
    
3.最后运行 download_images.py 开始批量下载照片到PNG文件夹

