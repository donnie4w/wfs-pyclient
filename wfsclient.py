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
        self._serverUrl=url
        self._transport = THttpClient(self._serverUrl)
        protocol = TCompactProtocol.TCompactProtocol(self._transport)       
        self._client = IW.Client(protocol)
        self._transport.open() 

    def PostFile(self,bs,name,fileType):
        wf = IW.WfsFile()
        wf.fileBody,wf.fileType,wf.name = bs,fileType,name
        return self._client.wfsPost(wf)
       
    def GetFile(self,name) :
        return self._client.wfsRead(name)

    def DelFile(self,name):
        return self._client.wfsDel(name) 

    def Close(self):
        self._transport.close()

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
    wfs.Close()

