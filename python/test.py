# Author : Fengyuan(Franklin) Zhang
# Date : 2019/1/4
# Description : Test for service SDK
from __init__ import OGMSService_DEBUG


server = OGMSService_DEBUG.CreateServer("127.0.0.1", 8060)
# server = OGMSService_DEBUG.CreateServer("172.21.212.7", 8060)
server.connect()
if server.connect() : 
    access = server.createServiceAccess()
    list_ms = access.getModelServicesList()
    for index, item in enumerate(list_ms):
        print("ID : " + item.id + " - Name : " + item.name + " - Type : " + item.type)
    dataid1 = access.uploadDataByFile("rapid_io_files", "/home/sherry/Downloads/rapid_test_data/input.zip")
    print("rapid_io_files - Input Data ID : " + dataid1)
    dataid2 = access.uploadDataByFile("lsm_data", "/home/sherry/Downloads/rapid_test_data/data.zip")
    print("lsm_data - Input Data ID : " + dataid2)
    dataid3 = access.uploadDataByFile("python_file", "/home/sherry/Downloads/rapid_test_data/run_rapid.py")
    print("python_file - Input Data ID : " + dataid3)
    swat = access.getModelServiceByID("5d89729ba8f79a7a0761ae7d")
    recordid = swat.invoke([access.createDataConfigurationItem("mainProcess", "rapid_io_files", dataid1),
                            access.createDataConfigurationItem("mainProcess", "lsm_data", dataid2),
                            access.createDataConfigurationItem("mainProcess", "python_file", dataid3)])
    record = access.getModelServiceRunningRecordByID(recordid)
    instance = access.getModelServiceInstanceByGUID(record.guid)
    instance.wait4Status(4, 7200, True)
    print("AreaD8 has been finished")
    record.refresh()
    for index,item in enumerate(record.outputs):
        dat = access.getDataByID(item.dataid)
        dat.save("/home/sherry/Downloads/rapid_test_data/Qout" + item.eventname + ".zip")