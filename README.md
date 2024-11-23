# OnePlusCloudDiskPhotoBatchDownload
用于一加云盘照片批量下载
### 1.进入照片列表页面

![image-20240325010302748](https://github.com/MoomasMan/OnePlusCloudDiskPhotoBatchDownload/blob/main/IMG/1732381122032.png)

### 2.通过f12抓到这个请求



右键复制为cURL(bash) 这是edge的用法

### 3.进入 [爬虫工具库-spidertools.cn](https://spidertools.cn/#/curl2Request) copy进去 



取cookie 那一段的内容 copy到saveUrl代码中 



### 4.脚本运行

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
