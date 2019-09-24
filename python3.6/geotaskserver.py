# Author : Fengyuan(Franklin) Zhang
# Date : 2019/1/23
# Description : Using of task server

import json
import time
import os
import requests
import urllib

from base import Service
from geodataexserver import ExData
from geodataexserver import GeoDataExServer
from utils import HttpHelper
from geodatacontainerserver import GeoDataServiceServer

class Task(Service):
    def __init__(self, ip, port, pid, dxserver, username = "Unknown"):
        Service.__init__(self, ip, port)
        self.pid = pid
        self.dxserver = dxserver
        self.inputdata = []
        self.outputdata = []
        self.username = username
        self.tid = None
        self.status = None

    def configInputData(self, state, event, data, tag = ""):
        dataItem = {
            "StateName" : state,
            "Event" : event,
            "Url" : "",
            "Tag" : tag
        }
        data_n = self.dxserver.upload(data, tag)
        dataItem["Url"] = data_n.getURL()
        self.inputdata.append(dataItem)
        return 1

    # status : 'Inited', 'Started', 'Finished' and 'Error'
    def wait4Status(self, status_w, timeout = 7200):
        currtime = time.time()
        endtime = currtime + timeout
        self.refresh()
        status = self.status
        while status != status_w and currtime < endtime:
            time.sleep(2)
            self.refresh()
            status = self.status
            currtime = time.time()
        if endtime >= currtime:
            # TODO more judgement
            return -1
        return 1

    def downloadResultByStateEvent(self, state, event, path):
        for item in self.outputdata:
            if item["StateName"] == state and item["Event"] == event:
                urllib.urlretrieve(item["Url"], path)

    def downloadAllData(self):
        pass


    def wait4Finish(self, timeout = 7200):
        return self.wait4Status('Finished', timeout)
        

    def refresh(self):
        resJson = HttpHelper.Request_get_sync(self.ip, self.port, '/task/' + self.tid)
        if resJson['result'] == 'suc':
            self.status = resJson['data']['t_status']
            for item in resJson['data']['t_outputs']:
                dataItem = {
                    "StateName" : item["StateName"],
                    "Event" : item["Event"],
                    "Url" : item["Url"],
                    "Tag" : item["Tag"]
                }
                self.outputdata.append(dataItem)
        return self.status

    def _bind(self, tid, status):
        self.tid = tid
        self.status = status
        return 1

class GeoTaskServer(Service):
    def __init__(self, ip, port):
        Service.__init__(self, ip, port)

    def subscribeTask(self, task):
        params = {
            "inputs" : json.dumps(task.inputdata),
            "username" : task.username,
            "pid" : task.pid
        }
        resJson = HttpHelper.Request_post_sync(self.ip, self.port, '/task', params)
        if resJson != "Error":
            if resJson["result"] == "suc":
                task._bind(resJson["data"], "Inited")
                return 1
            return -2
        return -1

    def createTask(self, pid, dxserver = None, username = "Unknown"):
        resJson = HttpHelper.Request_get_sync(self.ip, self.port, '/server?pid=' + pid)
        if resJson['result'] != 'suc' or resJson['code'] != 1:
            return None
        if dxserver == None:
            resJson = HttpHelper.Request_get_sync(self.ip, self.port, '/dxserver?ac=recommend')
            if resJson['result'] == 'suc' and len(resJson['data']) > 0:
                type = resJson['data']['type']
                if type == 1:
                    dxserver = GeoDataExServer(resJson['data']['ds_ip'], int(resJson['data']['ds_port']))
                else:
                    dxserver = GeoDataServiceServer(resJson['data']['ds_ip'], int(resJson['data']['ds_port']), username)
            else:
                return None
        return Task(self.ip, self.port, pid, dxserver, username)