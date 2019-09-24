from __init__ import OGMSService_DEBUG

taskServer = OGMSService_DEBUG.CreateTaskServer('127.0.0.1', 8061)
task = taskServer.createTask("51c650cd6320c08b54a71a0efa7b7d8a")

if task <> None:
    task.configInputData("RUNSTATE", "LOADDATASET", "E:\\DemoData\\GeoModeling\\FDS\\data11.fds")
    taskServer.subscribeTask(task)
    task.wait4Finish()
    print 'Suc'
else:
    print 'Error' 