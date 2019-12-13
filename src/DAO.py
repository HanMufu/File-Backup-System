import pymysql


class DAO:
    def __init__(self, db, user, pwd):
        global database
        global conn
        database = db
        try:
            global cur
            #conn = pymysql.connect(host='35.223.248.16', user='cqh', passwd='CAMRYLOVESEDGE', db=database, port=3306)
            conn = pymysql.connect(host='35.223.248.16', user=user, passwd=pwd, db=database, port=3306)
            cur = conn.cursor()
        except:
            print("Fail to connect database")

        #sql = "select * from test.20191204220814"
        #cur.execute(sql)
        # rows = cur.fetchall()
        # print(rows)

    def disconnect(self):
        cur.close()
        conn.close()
        return

    def create_table(self, table_id):
        sql = "CREATE TABLE test."+table_id+\
              "(ID INT PRIMARY KEY AUTO_INCREMENT, " \
              "filePath_Client VARCHAR(200), " \
              "filePath_Server VARCHAR(200), " \
              "fileSize VARCHAR(50), " \
              "fileType VARCHAR(30), " \
              "fileName VARCHAR(100), " \
              "MD5 VARCHAR(200), " \
              "isExist_LastB boolean, " \
              "isBp_Complete boolean )"

        # print(sql)
        try:
            cur.execute(sql)
        except:
            print("Couldn't create a new version")

        print("Create table successfully")
        return

    def request_data(self, last_version):
        try:
            # sql = "select MD5, fileName, filePath_Server from test."+last_version
            sql = "select * from %s.%s" % (database, last_version)
            cur.execute(sql)
            res = cur.fetchall()
            #print(res)
        except:
            print("Couldn't request record from server")
            return

        return res

    def upload_data(self, table_id, file_path_client, file_path_server, file_size, file_type, filename, md5_code, is_exist):
        sql = "INSERT INTO %s.%s VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', %s, %s)"\
            % (database, table_id, pymysql.escape_string(str(file_path_client)), pymysql.escape_string(str(file_path_server)),
               str(file_size), file_type, pymysql.escape_string(str(filename)), md5_code, is_exist, 'False')
        cur.execute(sql)
        #print(sql)
        return

    def execute_sql(self, sql):
        cur.execute(sql)

    def getDatabase(self):
        return database

    def update_Bp_completed(self, table_id, server_path):
        sql = "Update %s.%s SET isBp_Complete=True WHERE filePath_Server='%s'" % (database, table_id, pymysql.escape_string(str(server_path)))
        cur.execute(sql)
        return

