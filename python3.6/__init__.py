from server import Server
from data import DataConfigrationItem
from geotaskserver import GeoTaskServer
from geodataexserver import GeoDataExServer
from geodatacontainerserver import GeoDataServiceServer

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
    def CreateDataExchangeServer(ip, port):
        dataExchangeServer = GeoDataExServer(ip, port)
        if dataExchangeServer.connect():
            return dataExchangeServer
        return None
    @staticmethod
    def CreateDataServiceServer(ip, port, userName):
        dataServiceServer = GeoDataServiceServer(ip, port, userName)
        if dataServiceServer.connect():
            return dataServiceServer
        return None