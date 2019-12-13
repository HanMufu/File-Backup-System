import pymysql

class Item:
    ID = None
    filePath_Client = None
    filePath_Server = None
    fileSize = None
    fileType = None
    fileName = None
    MD5 = None
    isExist_LastB = None
    isBp_Complete = None

    def __init__(self, ID, filePath_Client, filePath_Server, fileSize, fileType, fileName, MD5, isExist_LastB,
                 isBp_Complete):
        self.ID = ID
        self.filePath_Client = filePath_Client
        self.filePath_Server = filePath_Server
        self.fileSize = fileSize
        self.fileType = fileType
        self.fileName = fileName
        self.MD5 = MD5
        self.isExist_LastB = isExist_LastB
        self.isBp_Complete = isBp_Complete

    def print_all(obj):
        print(obj.__dict__)

# fileA = Item("001", "/desktop", "/20191204220814/desktop/readme.txt", "1206", "txt", "readme.txt", "qwertyuiopasdfghjkl", False, True)
# fileA.print()
# folderA = Item("002", "/desktop", "/20191204220814/desktop/folderA", "25374", "folder", "folderA", "mnbvcxzlkjhgfdsa", False, True)
# folderA.print()


class User:
    userID = None
    userName = None
    passwordMD5 = None
    useRootPathAtServer = None

    def __init__(self, userID, userName, passwordMD5, useRootPathAtServer):
        self.userID = userID
        self.userName = userName
        self.passwordMD5 = passwordMD5
        self.useRootPathAtServer = useRootPathAtServer

    def create_user_database(self):
        connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE', port=3306)
        cursor = connection.cursor()
        sql3 = "create database %s" % self.userName
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
                    return [True, curr_user]
                else:
                    print('wrong password')
                    login_connection.close()
                    return [False, None]
        except:
            print("Error: unable to fetch data")
        login_connection.close()
        return [False, None]

    def print_all(obj):
        print(obj.__dict__)

# curr_user = User("Alice_qwertyu", "Alice", "aldskfj23lkhagd", "/home/dataspace/Alice_qwertyu", "Alice_qwertyu")


class Backup:
    backupID = None
    backupTime = None
    backupFolderName = None
    backupDBTableName = None

    def __init__(self, backupID, backupTime, backupFolderName, backupDBTableName):
        self.backupID = backupID
        self.backupTime = backupTime
        self.backupFolderName = backupFolderName
        self.backupDBTableName = backupDBTableName


class DatabaseController:
    def __init__(self):
        pass

    def connect_database(self):
        try:
            global connection
            '''有问题 db指定的不对'''
            connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE',
                                         db=curr_user.userName, port=3306)
            cursor = connection.cursor()
        except:
            print("Fail to connect database")
        return cursor

    def disconnect_database(self):
        connection.close()






