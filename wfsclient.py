#
# https://github.com/donnie4w/wfs-pyclient
#  wfs client of python3
# wfs : https://github.com/donnie4w/wfs
# donnie4w@gmail.com
#
#!/usr/bin/python3
from thrift.transport.THttpClient import THttpClient
from thrift.protocol import TCompactProtocol
import IWfs as IW


class WfsClient:
    def __init__(self,url) -> None:
        self.serverUrl=url
        transport = THttpClient(self.serverUrl)
        protocol = TCompactProtocol.TCompactProtocol(transport)       
        self.client = IW.Client(protocol)
        transport.open() 

    def PostFile(self,bs,name,fileType):
        wf = IW.WfsFile()
        wf.fileBody,wf.fileType,wf.name = bs,fileType,name
        return self.client.wfsPost(wf)
       
    def GetFile(self,name) :
        return self.client.wfsRead(name)

    def DelFile(self,name):
        return self.client.wfsDel(name)        

def getFileBytes(filename):
    return open(filename, "rb").read()

def saveFileByBytes(bs,filename):
    open(filename, "wb").write(bs)

if __name__ == "__main__":
    wfs = WfsClient("http://127.0.0.1:3434/thrift")
    bs= getFileBytes("1.jpg")
    wfs.PostFile(bs,"22","")
    f = wfs.GetFile("22")
    print(len(f.fileBody))
    saveFileByBytes(f.fileBody,"22_1.jpg")
    # wfs.DelFile("22")

