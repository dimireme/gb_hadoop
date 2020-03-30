from hdfs3 import HDFileSystem
hdfs=HDFileSystem(host='manager.novalocal',port=8020)


hdfs.ls('/user/instructor')
