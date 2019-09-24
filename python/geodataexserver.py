# Author : Fengyuan(Franklin) Zhang
# Date : 2019/1/4
# Description : Using of data exchange server

import urllib
import requests
import json

from base import Service
from utils import CommonMethod
from utils import HttpHelper


class ExData(Service):
    def __init__(self, ip, port, id, pwd):
        Service.__init__(self, ip, port)
        self.id = id
        self.pwd = pwd

    def getURL(self):
        dataid = self.id
        if self.pwd == '':
            pwd_c = ''
        else:
            pwd_c = CommonMethod.encryption(self.pwd)
        url = "http://" + self.ip + ":" + str(self.port) + "/data/" + dataid + "?pwd=" + pwd_c
        return str(url)

    def download(self, path):
        filepath = path
        url = self.getURL()
        urllib.urlretrieve(url, filepath)

class GeoDataExServer(Service):
    def __init__(self, ip, port):
        Service.__init__(self, ip, port)

    def upload(self, datapath, tag = "", security = False):
        md5 = CommonMethod.getFileMd5(datapath)
        path = "/data?md5=" + md5
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, path)
        data = None
        if jsData['result'] == 'suc':
            if(jsData['data'] <> ''):
                pwd = jsData['data']['d_pwd']
                pwd = CommonMethod.decryption(CommonMethod.decryption(pwd))
                data = ExData(self.ip, self.port, str(jsData['data']['id']), pwd)
            else:
                data = {"datatag" : tag, "pwd" : "true"}
                files = {  
                    "datafile" : open(datapath, "rb")  
                }
                r = requests.post("http://" + self.ip + ":" + str(self.port) + "/data", data, files=files)
                jsData = json.loads(r.text)
                if jsData['result'] == 'suc':
                    pwd = jsData['data']['d_pwd']
                    pwd = CommonMethod.decryption(CommonMethod.decryption(pwd))
                    data = ExData(self.ip, self.port, str(jsData['data']['id']), pwd)
        return data
    
