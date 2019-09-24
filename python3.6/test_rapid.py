# Author : Fengyuan(Franklin) Zhang
# Date : 2019/1/4
# Description : Test for service SDK
from __init__ import OGMSService_DEBUG

# server address
server = OGMSService_DEBUG.CreateServer("127.0.0.1", 8060)
server.connect()

service_inputs_dir = "/home/sherry/Downloads/rapid_test_data/"

if server.connect() : 
    access = server.getServiceAccess()
    list_ms = access.getModelServicesList()
    for index, item in enumerate(list_ms):
        print("ID : " + item.id + " - Name : " + item.name + " - Type : " + item.type)

    # upload inputs for each event
    rapid_io_files = access.uploadDataByFile("rapid_io_files", service_inputs_dir+"input.zip")
    print("rapid_io_files - Input Data ID : " + rapid_io_files)
    lsm_data = access.uploadDataByFile("lsm_data", service_inputs_dir+"data.zip")
    print("lsm_data - Input Data ID : " + lsm_data)
    python_file = access.uploadDataByFile("python_file", service_inputs_dir+"run_rapid.py")
    print("python_file - Input Data ID : " + python_file)

    # access service by id
    rapidpy = access.getModelServiceByID("5d89729ba8f79a7a0761ae7d")
    recordid = rapidpy.invoke([access.createDataConfigurationItem("mainProcess", "rapid_io_files", rapid_io_files),
                            access.createDataConfigurationItem("mainProcess", "lsm_data", lsm_data),
                            access.createDataConfigurationItem("mainProcess", "python_file", python_file)])
    record = access.getModelServiceRunningRecordByID(recordid)
    instance = access.getModelServiceInstanceByGUID(record.guid)
    instance.wait4Status(4, 7200, True)
    print("Streamflow prediction has been finished")
    record.refresh()
    # save results to dir
    for index,item in enumerate(record.outputs):
        dat = access.getDataByID(item.dataid)
        dat.save("/home/sherry/Downloads/rapid_test_data/Qout_" + item.eventname + ".nc")