import pymysql
import time
import paramiko

class Item:
    ID = None
    file_path_at_client = None
    file_path_at_server = None
    file_size = None
    file_type = None
    file_name = None
    MD5 = None
    is_existed_at_last_backup = None
    is_backup_completed = None

    def __init__(self, ID, filePath_Client, filePath_Server, fileSize, fileType, fileName, MD5, isExist_LastB,
                 isBp_Complete):
        self.ID = ID
        self.file_path_at_client = filePath_Client
        self.file_path_at_server = filePath_Server
        self.file_size = fileSize
        self.file_type = fileType
        self.file_name = fileName
        self.MD5 = MD5
        self.is_existed_at_last_backup = isExist_LastB
        self.is_backup_completed = isBp_Complete

    def print_all(obj):
        print(obj.__dict__)

# fileA = Item("001", "/desktop", "/20191204220814/desktop/readme.txt", "1206", "txt", "readme.txt", "qwertyuiopasdfghjkl", False, True)
# fileA.print()
# folderA = Item("002", "/desktop", "/20191204220814/desktop/folderA", "25374", "folder", "folderA", "mnbvcxzlkjhgfdsa", False, True)
# folderA.print()

class Backup:
    backup_id = None
    backup_time = None
    backup_root_path_at_server = None

    def __init__(self, backupID, backupTime, backupFolderName):
        self.backup_id = backupID
        self.backup_time = backupTime
        self.backup_root_path_at_server = backupFolderName

    def print_all(obj):
        print(obj.__dict__)

class User:
    user_id = None
    user_name = None
    password_md5 = None
    user_root_path_at_client = None

    def __init__(self, userID, userName, passwordMD5, useRootPathAtClient):
        self.user_id = userID
        self.user_name = userName
        self.password_md5 = passwordMD5
        self.user_root_path_at_client = useRootPathAtClient

    def create_user_database(self):
        connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE', port=3306)
        cursor = connection.cursor()
        sql3 = "create database %s" % self.user_name
        cursor.execute(sql3)
        connection.close()


    def signup(self, user_name, password_md5, rootpath):
        try:
            signup_connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE', db="RUBackup", port=3306)
            cursor = signup_connection.cursor()
        except:
            print("Fail to connect database")
            return [False, None]
        user_name_for_sql = "'" + user_name + "'"
        sql = "select * from user_RUBackup where user_name = %s " % user_name_for_sql
        cursor.execute(sql)
        results = cursor.fetchall()
        if(len(results) != 0):
            print('user already existed')
            return [False, None]
        else:
            password_for_sql = "'" + password_md5 + "'"
            rootpath_for_sql = "'" + rootpath + "'"
            sql2 = "insert into user_RUBackup (user_id, user_name, password_md5, backup_root_path_at_client) values (null, %s, %s, %s)" % (user_name_for_sql, password_for_sql, rootpath_for_sql)
            try:
                cursor.execute(sql2)
                signup_connection.commit()
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    curr_user = User(row[0], row[1], row[2], row[3])
                    curr_user.create_user_database()
                    signup_connection.close()
                    print("signup successful")
                    return [True, curr_user]
            except:
                signup_connection.rollback()
                print("falied to insert data into database")
                return [False, None]

    def login(self, user_name, password_md5):
        try:
            login_connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE', db="RUBackup", port=3306)
            cursor = login_connection.cursor()
        except:
            print("Fail to connect database")
            return [False, None]
        user_name_for_sql = "'" + user_name + "'"
        sql = "select * from user_RUBackup where user_name = %s " % user_name_for_sql
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                if row[2] == password_md5:
                    curr_user = User(row[0], row[1], row[2], row[3])
                    login_connection.close()
                    print("login successful")
                    return [True, curr_user]
                else:
                    print('wrong password')
                    login_connection.close()
                    return [False, None]
        except:
            print("Error: unable to fetch data")
        login_connection.close()
        return [False, None]

    def get_backup_list(self):
        connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE', db="RUBackup", port=3306)
        cursor = connection.cursor()
        sql = "select * from user_backup_history where user_id = " + str(self.user_id)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            backup_history_list = []
            for row in results:
                tmp_backup = Backup(row[0], row[2], row[3])
                backup_history_list.append(tmp_backup)
            print("get backup list successful, len of list is " + str(len(backup_history_list)))
        except:
            print("Error: unable to fetch data")
        connection.close()
        return backup_history_list

    def insert_backup_history(self):
        connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE', db="RUBackup", port=3306)
        cursor = connection.cursor()
        curr_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        backup_time_for_sql = "'" + curr_time + "'"
        user_id_for_sql = "'" + str(self.user_id) + "'"
        backup_path = '/home/dataspace/' + self.user_name + '/' + curr_time + '/'
        backup_path_for_sql = "'" + backup_path + "'"
        sql = "insert into user_backup_history (backup_id, user_id, backup_time, backup_root_path_at_server) values (null, %s, %s, %s)" % (user_id_for_sql, backup_time_for_sql, backup_path_for_sql)
        print(sql)
        try:
            cursor.execute(sql)
            connection.commit()
            connection.close()
            print("insert backup history successful")
            return True
        except:
            print("insert backup history failed")
            connection.rollback()
            connection.close()
            return False

    def fetch_folder_content(self, parent_folder: Item, curr_backup: Backup):
        # connect to DB
        connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE', db=self.user_name, port=3306)
        cursor = connection.cursor()
        # select * from curr_backup.backupDBTableName where filePath_Client = parent_folder.filePath_Client + parent_folder.fileName
        parent_folder_path = "'" + parent_folder.file_path_at_client + "/" + parent_folder.file_name + "'"
        sql = "select * from %s.%s where filePath_Client = %s" % (self.user_name, curr_backup.backup_time, parent_folder_path)
        res_file_list = []
        try:
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                curr_file = Item(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                res_file_list.append(curr_file)
                curr_file.print_all()
            print("fetch folder content successful, len of content is " + str(len(res_file_list)))
        except:
            print("Error: unable to fetch data in fetch_folder_content")
            connection.close()
        return res_file_list

    # def get_folder_info(self, folder_path: str, curr_backup: Backup):
    #     connection = pymysql.connect(host='35.223.248.16', user='root', db=self.user_name, passwd='CAMRYLOVESEDGE', port=3306)
    #     cursor = connection.cursor()
    #     backup_table_name_for_sql = "'" + curr_backup.backup_time + "'"
    #     folder_path_for_sql = "'" + folder_path + "'"
    #     sql = "select * from %s where filePath_Client = %s" % (backup_table_name_for_sql, folder_path_for_sql)
    #     try:
    #         cursor.execute(sql)
    #         # 获取所有记录列表
    #         results = cursor.fetchall()
    #         for row in results:
    #             curr_file = Item(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    #             res_file_list.append(curr_file)
    #             curr_file.print_all()
    #     except:
    #         print("Error: unable to fetch data")
    #         connection.disconnect()
    #     connection.close()

    def fetch_root_folder_content(self, curr_backup: Backup, file_path: str):
        # connect to DB
        connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE', db=self.user_name, port=3306)
        cursor = connection.cursor()
        # select * from curr_backup.backupDBTableName where filePath_Client = parent_folder.filePath_Client + parent_folder.fileName
        parent_folder_path = "'" + file_path + "'"
        sql = "select * from %s.%s where filePath_Client = %s" % (self.user_name, curr_backup.backup_time, parent_folder_path)
        res_file_list = []
        print(sql)
        try:
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                curr_file = Item(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                res_file_list.append(curr_file)
                curr_file.print_all()
            print("get folder content successful, this is an action triggered by login or signup")
        except:
            print("Error: unable to fetch data in fetch_root_folder_content")
            connection.close()
        return res_file_list

    def create_folder_on_server(self):
        host_name = "35.223.248.16"
        user_name = 'root'
        password = 'CAMRYLOVESEDGE'
        port = 22
        '''connect to remote server'''
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host_name, port=port, username=user_name, password=password)
            # stdin, stdout, stderr = ssh.exec_command("cd /home/dataspace/")
            # stdin, stdout, stderr = ssh.exec_command('mkdir %s' % (self.user_name))
            stdin, stdout, stderr = ssh.exec_command("cd /home/dataspace/;mkdir %s" % self.user_name)
            ssh.close()
            print("create user dataspace successful")
        except:
            print("create folder on server failed")


    def print_all(obj):
        print(obj.__dict__)

# curr_user = User("Alice_qwertyu", "Alice", "aldskfj23lkhagd", "/home/dataspace/Alice_qwertyu", "Alice_qwertyu")



# class DatabaseController:
#     def __init__(self):
#         pass
#
#     def connect_database(self):
#         try:
#             global connection
#             '''有问题 db指定的不对'''
#             connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE',
#                                          db=curr_user.userName, port=3306)
#             cursor = connection.cursor()
#         except:
#             print("Fail to connect database")
#         return cursor
#
#     def disconnect_database(self):
#         connection.close()






