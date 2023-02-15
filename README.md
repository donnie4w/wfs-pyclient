# wfs-pyclient
**WFS的THRIFT PYTHON3实现访问接口**


------------
上传文件

    获取wfs客户端实例：
	wfs = WfsClient("http://127.0.0.1:3434/thrift")
	
    bs=getFileBytes("1.jpg")
	#上传 文件bytes, 文件名
    wfs.PostFile(bs,"22.jpg","") 
	#相当于：curl -F "file=@1.jpg" "http://127.0.0.1:3434/u/22.jpg"
	#1.jpg 是本地文件，22.jpg是上传到服务自定义的文件名，
	#也可以：
	wfs.PostFile(bs,"fff/ggg/1.jpg","") 
	#访问则为：http://127.0.0.1:3434/r/fff/ggg/1.jpg
	
拉取 文件

    f = wfs.GetFile("22.jpg")
	#相当于：http://127.0.0.1:3434/r/22.jpg
	 f = wfs.GetFile("fff/ggg/22.jpg")
	#相当于：http://127.0.0.1:3434/r/fff/ggg/22.jpg
    print(len(f.fileBody))
	#保存文件到本地
    saveFileByBytes(f.fileBody,"22_1.jpg")

删除文件

    wfs.DelFile("22.jpg")

