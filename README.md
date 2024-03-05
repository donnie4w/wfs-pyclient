# wfs-pyclient

###### WFS的 PYTHON3实现访问接口

------------
创建wfsclient实例对象

	def newClient() -> WfsClient:
    	client = WfsClient()
    	wa = client.newConnect(False, "127.0.0.1", 6802, "admin", "123")
    	print(wa)
    	return client

参数说明：client.newConnect(False, "127.0.0.1", 6802, "admin", "123")
1. 第一个参数：是否TLS
2. 第二个参数：wfs thrift 服务ip或域名
3. 第三个参数：端口
4. 第四个参数：后台用户名
5. 第五个参数：后台密码

------------

上传文件

	def test_Append():
    	client = newClient()
    	wf = WfsFile()
    	wf.name = "test/py/1.jpeg"
    	wf.data = open('1.jpeg', 'rb').read()
    	client.Append(wf)

删除文件

	def test_Delete():
    	client = newClient()
    	ack = client.Delete("test/py/1.jpeg")
    	print("delete ack:", ack)

拉取文件

	def test_Get():
    	client = newClient()
    	wd = client.Get("test/py/1.jpeg")
    	if wd.data is not None:
        	length = len(wd.data)
        	print("file length:", length)
    	else:
        	print("file not exist")
		

