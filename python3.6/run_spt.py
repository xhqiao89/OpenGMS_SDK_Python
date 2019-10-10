# Author : Xiaohui Qiao
# Date : 2019/10/4
# Description : Script to run streamflow prediction service for Bangladesh
from __init__ import OGMSService_DEBUG
import datetime

# server address
server = OGMSService_DEBUG.CreateServer("127.0.0.1", 8060)
server.connect()

service_inputs_dir = "/home/sherry/Downloads/erai_test/"
for i in range(1995,2000):
    year = str(i)
    print("Running streamflow prediction service for "+ year)

    if server.connect() :
        access = server.getServiceAccess()
        list_ms = access.getModelServicesList()
        for index, item in enumerate(list_ms):
            print("ID : " + item.id + " - Name : " + item.name + " - Type : " + item.type)

        # upload inputs for each event
        rapid_io_files = access.uploadDataByFile("rapid_io_files", service_inputs_dir+"input.zip")
        print("rapid_io_files - Input Data ID : " + rapid_io_files)
        lsm_data = access.uploadDataByFile("lsm_data", service_inputs_dir+"data/"+ year +"_erai_runoff.zip")
        print("lsm_data - Input Data ID : " + lsm_data)
        python_file = access.uploadDataByFile("python_file", service_inputs_dir+"run_rapid.py")
        print("python_file - Input Data ID : " + python_file)

        # access service by id
        rapidpy = access.getModelServiceByID("5d9ceecf703e530b6d356882")
        recordid = rapidpy.invoke([access.createDataConfigurationItem("mainProcess", "rapid_io_files", rapid_io_files),
                                access.createDataConfigurationItem("mainProcess", "lsm_data", lsm_data),
                                access.createDataConfigurationItem("mainProcess", "python_file", python_file)])
        record = access.getModelServiceRunningRecordByID(recordid)
        instance = access.getModelServiceInstanceByGUID(record.guid)
        instance.wait4Status(4, 7200, True)
        print("Streamflow prediction has been finished")
        record.refresh()
        # save results to dir
        #time=str(datetime.datetime.now()).split('.')[1]
        for index,item in enumerate(record.outputs):
            dat = access.getDataByID(item.dataid)
            dat.save("/home/sherry/Downloads/erai_test/Qout_" + item.eventname + year + "123.nc")

        i=i+1