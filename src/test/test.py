import DAO
import FTP
import os
ftp_user = 'root'
ftp_pwd = 'CAMRYLOVESEDGE'
host_name = "35.223.248.16"
print("1")
ftp = FTP.FTP(ftp_user, ftp_pwd, 22)
path = "/home/parallels/Pictures"
name = '1.jpg'
sp = "/home/dataspace/Alice"
sp=os.path.join(sp,name)
path=os.path.join(path, name)
print(sp)
print(path)
ftp.uploader(path, sp)
ftp.disconnect()