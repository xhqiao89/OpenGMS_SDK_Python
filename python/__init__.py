from server import Server
from data import DataConfigrationItem
from geotaskserver import GeoTaskServer

class OGMSService_DEBUG:
    @staticmethod
    def CreateServer(ip, port):
        return Server(ip, port)

    @staticmethod
    def CreateTaskServer(ip, port):
        taskServer = GeoTaskServer(ip, port)
        if taskServer.connect():
            return taskServer
        return None

    @staticmethod
    def CreateTask(name):
        pass