import urllib
import httplib
import json
import requests
import hashlib
import os
import random
import string
import base64

charstr = 'QWERTYUIOPASDFGHJKLZXCVBNMzyxwvutsrqponmlkjihgfedcba!@#$%^&*()'

class HttpHelper:
    @staticmethod
    def Request_get_sync(ip, port, path):
        try :
            conn = httplib.HTTPConnection(ip, port)
            conn.request("GET", path)
            res = conn.getresponse()
            resData = res.read().decode('utf-8').encode('mbcs')
            jsData = json.loads(resData.decode('gbk'))
            return jsData
        except Exception as e :
            return "Error"

    @staticmethod
    def Request_get_stream_sync(ip, port, path):
        try :
            conn = httplib.HTTPConnection(ip, port)
            conn.request("GET", path)
            res = conn.getresponse()
            jsData = res.read().decode('utf-8').encode('mbcs')
            return jsData
        except Exception as e :
            return "Error"

    
    @staticmethod
    def Request_post_sync(ip, port, path, params = None, files = None):
        try :
            r = requests.post("http://" + ip + ":" + str(port) + path, params, files=files)
            jsData = json.loads(r.text)
            return jsData
        except Exception as e :
            return "Error"


    @staticmethod
    def Request_put_sync(ip, port, path):
        conn = httplib.HTTPConnection(ip, port)
        conn.request("PUT", path)
        res = conn.getresponse()
        jsData = json.loads(res.read())
        return jsData

class CommonMethod:
    @staticmethod
    def IsGUID(statevalue):
        if isinstance(statevalue, (str, unicode)) :
            if len(statevalue) == 36:
                strs = statevalue.split('-')
                for index, item in enumerate(strs):
                    if len(item) == 0:
                        return False
                return True
            else :
                return False
        else:
            return False

    @staticmethod
    def getJsonValue(jsobject, key):
        if jsobject == "" or isinstance(jsobject, (str, unicode)):
            return ""
        if key in jsobject:
            return jsobject[key]
        else:
            return ""

    @staticmethod
    def getFileMd5(filename):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = open(filename,'rb')
        while True:
            b = f.read(8096)
            if not b :
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    @staticmethod
    def encryption(buffer):
        a = str(buffer)
        a = a.encode('hex')
        a = (base64.encodestring(a))[0:-1]
        a = ''.join(random.sample(charstr, 5)) + a + ''.join(random.sample(charstr, 5))
        a = (base64.encodestring(a))[0:-1]
        return a

    @staticmethod
    def decryption(buffer):
        b = base64.decodestring(str(buffer))
        b = b[5:]
        b = b[0:-5]
        b = base64.decodestring(b)
        b = b.decode('hex')
        return b
