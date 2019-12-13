import os
import hashlib
import time
import DAO
import FTP
# Mention: One SEVERE PROBLEM, once the scanning and upload are interrupted, due to the absence of last record.
# Files are uploaded again even they are already on server
class Scanner:

    def __init__(self, path, db, user, pwd, ftp_user, ftp_pwd, port):
        global table_id
        # Create a table id, which is also version_id
        # If not convert table_id into string, it's gonna export error
        id = time.strftime("%Y%m%d%H%M%S", time.localtime())
        table_id = '%s' % id
        # father_path=os.path.abspath(os.path.dirname(os.getcwd())+os.path.sep+".")
        # data -> 'md5',[filename, server_path]
        data = dict()


        # Check version
        if os.path.exists(os.getcwd()+"/version"):
            txt = open(os.getcwd()+"/version", 'r')
            last_version = txt.readline()
            txt.close()
            try:
                fobj = open(os.getcwd()+"/version", 'w')
                fobj.write(table_id)
                fobj.close()
            except IOError:
                print('*** version file open error:')
        else:
            try:
                fobj = open(os.getcwd()+"/version", 'w')
                fobj.write(table_id)
                fobj.close()
                last_version = "null"
            except IOError:
                print('*** version file open error:')

        dao = DAO.DAO(db, user, pwd)
        dao.create_table(table_id)
        ftp = FTP.FTP(ftp_user, ftp_pwd, port)

        # Create new folder for this version
        # version_path = '/home/dataspace/%s/%s/' % (ftp_user, table_id)
        # Test
        version_path = '/home/dataspace/user/%s/' % table_id
        ftp.create_new_folder(version_path)
        # Don't care the warning on last_version, that's bullshit
        # Whether is the first time
        dao.execute_sql('Begin')
        if last_version is "null":
            print('Start scanning')
            file_scanner_initial(path, version_path, dao, ftp)
            print('Scanner completed')
        else:
            res = dao.request_data(last_version)
            if len(res) < 1:
                print('Start scanning')
                file_scanner_initial(path, version_path, dao, ftp)
                print('Scanner completed')
            else:
                for row in res:
                    md = row[0]
                    filename_serverpath=[row[1], row[2]]
                    data[md] = filename_serverpath
                print('Start scanning')
                file_scanner(path, version_path, data, dao, ftp)
                print('Scanner completed')

        dao.execute_sql('Commit')
        dao.disconnect()

def file_scanner(path, server_path, data, dao, ftp):
    print(os.path.abspath(os.path.dirname(path) + os.path.sep + "."))
    if not os.path.exists(path):
        raise FileNotFoundError('Path %s not exist' % path)
    if os.path.isfile(path):
        file_md5 = calMD5ForFile(path)
        if file_md5 in data:
            temp = data[file_md5]
            # If exists
            if os.path.basename(path) == temp[0]:
                dao.upload_data(table_id, os.path.abspath(os.path.dirname(path) + os.path.sep + "."),
                                temp[1], os.path.getsize(path), 'File',
                                os.path.basename(path), file_md5, 'True')
                dao.update_Bp_completed(table_id, temp[1])
            # If names don't match but md5 match, it's probably md5 coincidence, or mostly name modification
            else:
                dao.upload_data(table_id, os.path.abspath(os.path.dirname(path) + os.path.sep + "."),
                                server_path+os.path.basename(path), os.path.getsize(path), 'File',
                                os.path.basename(path), file_md5, 'False')
                ftp.uploader(path,  server_path+os.path.basename(path))
                dao.update_Bp_completed(table_id, server_path + os.path.basename(path))
                # Then update this by isBp_completed = True
        else:
            # When it's a new or modified file
            # server path generator()
            dao.upload_data(table_id, os.path.abspath(os.path.dirname(path) + os.path.sep + "."),
                            server_path+os.path.basename(path), os.path.getsize(path), 'File',
                            os.path.basename(path), file_md5, 'False')
            ftp.uploader(path, server_path + os.path.basename(path))
            dao.update_Bp_completed(table_id, server_path + os.path.basename(path))
            # Then update this by isBp_completed = True
    elif os.path.isdir(path):
        # Check gen
        # server path generator
        folder_path = server_path + os.path.basename(path) + "/"
        dao.upload_data(table_id, os.path.abspath(os.path.dirname(path) + os.path.sep + "."),
                        folder_path, os.path.getsize(path), 'Folder',
                        os.path.basename(path), 'null', 'False')
        ftp.create_new_folder(folder_path)
        dao.update_Bp_completed(table_id, folder_path)
        # Then update this by isBp_completed
        for it in os.scandir(path):
            file_scanner(it, folder_path, data, dao, ftp)


def file_scanner_initial(path, server_path, dao, ftp):
    print(os.path.abspath(os.path.dirname(path) + os.path.sep + "."))
    if not os.path.exists(path):
        raise FileNotFoundError('Path %s not exist' % path)
    if os.path.isfile(path):
        file_md5 = calMD5ForFile(path)
        # server path generator
        dao.upload_data(table_id, os.path.abspath(os.path.dirname(path) + os.path.sep + "."),
                        server_path+os.path.basename(path), os.path.getsize(path), 'File',
                        os.path.basename(path), file_md5, 'False')
        ftp.uploader(path, server_path + os.path.basename(path))
        dao.update_Bp_completed(table_id, server_path+os.path.basename(path))
        # Update is
    elif os.path.isdir(path):
        # server path generator
        folder_path = server_path + os.path.basename(path) + "/"
        dao.upload_data(table_id, os.path.abspath(os.path.dirname(path) + os.path.sep + "."),
                        folder_path, os.path.getsize(path), 'Folder',
                        os.path.basename(path), 'null', 'False')
        ftp.create_new_folder(folder_path)
        dao.update_Bp_completed(table_id, folder_path)
        # Then update this by isBp_completed
        for it in os.scandir(path):
            file_scanner_initial(it, folder_path, dao, ftp)

# Dir cannot be input md5


def calMD5ForFile(path):
    statinfo = os.stat(path)
    if int(statinfo.st_size)/(1024*1024) >= 1000 :
        print ("File size > 1000, move to big file...")
        return calMD5ForBigFile(path)
    m = hashlib.md5()
    f = open(path, 'rb')
    m.update(f.read())
    f.close()
    return m.hexdigest()


def calMD5ForBigFile(path):
    m = hashlib.md5()
    f = open(path, 'rb')
    buffer = 8192    # why is 8192 | 8192 is fast than 2048
    while 1:
        chunk = f.read(buffer)
        if not chunk : break
        m.update(chunk)
    f.close()
    return m.hexdigest()

