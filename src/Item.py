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

    def print(obj):
        "打印对象的所有属性"
        print(obj.__dict__)

fileA = Item("001", "/desktop", "/20191204220814/desktop/readme.txt", "1206", "txt", "readme.txt", "qwertyuiopasdfghjkl", False, True)
fileA.print()
folderA = Item("002", "/desktop", "/20191204220814/desktop/folderA", "25374", "folder", "folderA", "mnbvcxzlkjhgfdsa", False, True)
folderA.print()
