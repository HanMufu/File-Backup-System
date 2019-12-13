from model import Item, User, Backup

global curr_user
curr_user = User("1", "Alice", "aldskfj23lkhagd", "/home/dataspace/Alice_qwertyu")

fileA = Item("001", "/desktop", "/20191204220814/desktop/readme.txt", "1206", "txt", "readme.txt", "qwertyuiopasdfghjkl", False, True)

def fetch_folder_content(parent_folder, curr_backup):
    # connect to DB
    cursor = DatabaseController.connect_database()
    # select * from curr_backup.backupDBTableName where filePath_Client = parent_folder.filePath_Client + parent_folder.fileName
    parent_folder_path = "'" + parent_folder.filePath_Client + parent_folder.fileName + "'"
    db_table_path = curr_user.userDatabaseName + "." + curr_backup.backupDBTableName
    sql = "select * from %s where filePath_Client = %s" % db_table_path, parent_folder_path
    res_file_list = []
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            curr_file = Item(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            res_file_list.append(curr_file)
            curr_file.print_all()
    except:
        print("Error: unable to fetch data")
    DatabaseController.disconnect()
    return res_file_list
