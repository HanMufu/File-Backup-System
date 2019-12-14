# This Python file uses the following encoding: utf-8
import sys
# from PySide2.QtWidgets import QApplication
import PySide2
import os
import sys
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from PyQt5.QtWebEngineWidgets import *
import qdarkstyle
import model
from model import User, Item, Backup
import DAO
import Scanner, Download_SFTP

# This is the plugin information for using in Windows OS devices
#dirname = os.path.dirname(PySide2.__file__)
#plugin_path = os.path.join(dirname, 'plugins', 'platforms')
#os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


def getlist(dir):
    res_list = []
    for i in file_item_list:
        res_list.append(i.file_name)
    return res_list

current_user: User = User('', '', '', '')
current_backup: Backup = ('', '', '')
current_folder: Item = Item('', '', '', '', '', '', '', '', '')

# current_path: str = "/Users/hanmufu/Downloads/RUBackup_test_folder"
current_path = ""
# current_path = current_folder_item.filePath_Client

file_item_list = []
# file_list = getlist(current_path)
file_list = []
backup_list = []

class Ui_RU_Backup(object):
    def setupUi(self, RU_Backup):
        RU_Backup.setObjectName("RU_Backup")
        RU_Backup.resize(1210, 740)  # 420, 714
        # Doco.setFixedSize(420, 714)#
        # RU_Backup.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.retranslateUi(RU_Backup)
        QtCore.QMetaObject.connectSlotsByName(RU_Backup)

        # self.login = QtWidgets.QPushButton(RU_Backup)
        # self.login.setGeometry(QtCore.QRect(0, 30, 50, 30))
        # self.login.setObjectName("Login")
        # self.login.setText("Login")

        self.tb = RU_Backup.addToolBar("Login")

        new = QAction(QIcon("./icons/login.png"), "login", RU_Backup)
        new.triggered.connect(self.backpath_modify)
        self.tb.addAction(new)

        backup_start = QAction(QIcon("./icons/back.png"),"Start Backup",RU_Backup)
        backup_start.triggered.connect(self.backup_start)
        self.tb.addAction(backup_start)

        self.dir_label = QLabel(RU_Backup)
        self.dir_label.setGeometry(QtCore.QRect(60, 100, 700, 30))

        self.pushButton_pre = QtWidgets.QPushButton(RU_Backup, clicked=lambda: Event.Pre(self))
        self.pushButton_pre.setGeometry(QtCore.QRect(0, 100, 50, 30))
        self.pushButton_pre.setObjectName("pushButton_pre")
        self.pushButton_pre.setText("Back")

        self.listWidget = QtWidgets.QListWidget(RU_Backup)
        self.listWidget.setGeometry(QtCore.QRect(0, 130, 1200, 600))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget.verticalScrollBar().setSingleStep(1)  # set step
        # self.listWidget.setAlternatingRowColors(True);
        # self.listWidget.setVisible(False)

        self.cb = QComboBox(RU_Backup)
        self.cb.setGeometry(QtCore.QRect(0, 50, 1200, 50))
        global backup_list
        for i in backup_list:
            self.cb.addItem(i.backup_time)
        self.cb.activated.connect(self.selection_change)

        self.music_list()

    def retranslateUi(self, RU_Backup):
        _translate = QtCore.QCoreApplication.translate
        RU_Backup.setWindowTitle(_translate("RU_Backup", "RU_Backup"))
        # self.label_name.setText(_translate("RU_Backup", ""))
        # self.label_time.setText(_translate("RU_Backup", ""))

    def music_list(self):
        self.listWidget.clear()  # clear list
        # print(len(file_list))
        for n in range(0, len(file_item_list)):  # Creat Item for each file class in the file_item_list
            # Create QCustomQWidget
            myItemQWidget = ItemQWidget(n, self)
            myItemQWidget.setName()
            # myItemQWidget.setPlay()
            # myItemQWidget.setEvent(self.listWidget)
            # Create QListWidgetItem
            item = QtWidgets.QListWidgetItem(self.listWidget)
            # Set size hint
            item.setSizeHint(myItemQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, myItemQWidget)

    def backpath_modify(self, a):
        print("a")
        # TODO: modify the backpath

    def backup_start(self):
        #这里加入后端的开始备份的代码
        current_user.insert_backup_history()
        path = current_user.user_root_path_at_client
        #path = "/Users/hanmufu/Downloads/RUBackup_test_folder"
        user = 'root'
        pwd = 'CAMRYLOVESEDGE'
        ftp_user = 'root'
        ftp_pwd = 'CAMRYLOVESEDGE'
        port = 22
        # db = 'tommy'
        db = current_user.user_name
        s = Scanner.Scanner(path, db, user, pwd, ftp_user, ftp_pwd, port, current_user.user_name)
        print("scan completed, return to window")
        # 这里要刷新backup list下拉菜单 // TODO
        global backup_list
        backup_list = current_user.get_backup_list()
        for i in backup_list:
            self.cb.addItem(i.backup_time)


    def selection_change(self):
        global current_path
        global current_backup
        global backup_list
        for i in backup_list:
            if i.backup_time == self.cb.currentText():
                current_backup = i
                current_path = i.backup_root_path_at_server
        self.music_list()



class ItemQWidget(QtWidgets.QWidget):
    def __init__(self, n, ui, parent=None):
        super(ItemQWidget, self).__init__(parent)
        global current_path
        global file_item_list
        self.n = n
        self.file_class = file_item_list[self.n]
        self.ui = ui
        self.info_pre = infodialog(self.file_class)
        self.textQHBoxLayout = QtWidgets.QHBoxLayout()
        self.name = QtWidgets.QLabel()  
        #self.file_path = current_path + file_list[self.n]
        self.type_label = QToolButton()
        if self.file_class.file_type == "Folder":
            self.type_label.setIcon(QIcon("./icons/dir.png"))
        else:
            self.type_label.setIcon(QIcon("./icons/file.png"))
        self.play_btn = QtWidgets.QToolButton()
        self.play_btn.setIcon(QIcon("./icons/download.png"))  
        self.play_btn.clicked.connect(self.download)
        self.info_btn = QtWidgets.QToolButton()  
        self.info_btn.clicked.connect(self.info_pre.show)
        self.info_btn.setIcon(QIcon("./icons/info.png"))
        self.textQHBoxLayout.addWidget(self.type_label)
        self.textQHBoxLayout.addWidget(self.name)
        self.textQHBoxLayout.addWidget(self.play_btn)
        self.textQHBoxLayout.addWidget(self.info_btn)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.allQHBoxLayout.addLayout(self.textQHBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

    def setName(self):
        self.name.setText(self.file_class.file_name)

    def mouseDoubleClickEvent(self, e):  # Click two times of the folder and get into it
        global current_path
        global file_list
        global file_item_list
        global current_backup
        global current_backup
        # print("clicked"+self.name.text())
        current_path = current_path + '/' + self.name.text()
        self.ui.dir_label.setText(current_path)
        
        if self.file_class.file_type == "Folder":
            file_item_list = current_user.fetch_folder_content(self.file_class, current_backup)
            file_list = getlist(current_path)
            self.ui.music_list()  

    def download(self):
        print("start download")
        Download_SFTP.downloadhelper(self.file_class)
        print('download successful')


class Event():
    def Pre(self):  # This method is used for going back to the parent path
        global current_path
        global file_item_list
        global file_list
        global current_backup
        global current_user
        cache = current_path.split("/")
        le = len(cache[len(cache) - 1]) + 1
        current_path = current_path[:-le]
        #file_item_list = current_user.fetch_folder_content(self.file_class, current_backup)
        print(current_path)
        print(current_backup)

        file_item_list = current_user.fetch_root_folder_content(current_backup, current_path)
        #for i in file_item_list:
            #print(i.file_name)
        file_list = getlist(current_path)
        self.dir_label.setText(current_path)
        self.music_list()  # Refresh the path table
        # print(file_list)


class infodialog(QDialog):  # This dialog is used for presenting the information of files or folders
    def __init__(self, file_class, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.setWindowTitle('info')
        self.file_class = file_class
        # self.resize(600,300)
        # self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.file_size = QLabel(self)
        self.file_size.setText("File Size")

        self.file_size_pre = QLabel(self)
        self.file_size_pre.setText(self.file_class.file_size)

        self.file_type = QLabel(self)
        self.file_type.setText("File Type")

        self.file_type_pre = QLabel(self)
        self.file_type_pre.setText(self.file_class.file_type)

        self.file_MD5 = QLabel(self)
        self.file_MD5.setText("MD5")

        self.file_MD5_pre = QLabel(self)
        self.file_MD5_pre.setText(self.file_class.MD5)

        self.main_layout = QGridLayout(self)
        self.main_layout.addWidget(self.file_size)
        self.main_layout.addWidget(self.file_size_pre)
        self.main_layout.addWidget(self.file_type)
        self.main_layout.addWidget(self.file_type_pre)
        self.main_layout.addWidget(self.file_MD5)
        self.main_layout.addWidget(self.file_MD5_pre)


class logindialog(QDialog):  # This is the class for the login dialog
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Login')
        self.resize(400, 300)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.signup_dialog = signupdialog(self)

        self.frame = QFrame(self)
        self.frame.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self.frame)

        self.label_account = QtWidgets.QLabel()
        self.label_account.setText("Username")
        self.label_account.setFixedSize(400, 20)
        self.verticalLayout.addWidget(self.label_account)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setFixedSize(370, 30)
        # self.lineEdit_account.setPlaceholderText("Username")
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.label_password = QLabel()
        self.label_password.setText("Password")
        self.label_password.setFixedSize(400, 20)
        self.verticalLayout.addWidget(self.label_password)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setFixedSize(370, 30)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.lineEdit_password.setPlaceholderText("Password")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("Login")
        self.verticalLayout.addWidget(self.pushButton_enter)

        self.pushButton_signup = QPushButton()
        self.pushButton_signup.setText("Sign Up")
        self.verticalLayout.addWidget(self.pushButton_signup)
        self.pushButton_signup.clicked.connect(self.signup_show)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("Cancel")
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)

    def signup_show(self):
        self.close()

        self.signup_dialog.show()
        self.signup_dialog.exec_()

    # login control
    def on_pushButton_enter_clicked(self):
        global current_user
        res = current_user.login(self.lineEdit_account.text(), self.lineEdit_password.text())
        if res[0] == False:
            return
        else:
            current_user = res[1]
            current_user.print_all()
            global current_path
            current_path = current_user.user_root_path_at_client
            print(current_path)
            global backup_list
            backup_list = current_user.get_backup_list()
            global current_backup
            if len(backup_list) > 0:
                current_backup = backup_list[0]
                current_backup.print_all()
            else:
                print('no available backup')
                current_backup = Backup('', '', '/Users/Desktop')
            global file_item_list
            file_item_list = current_user.fetch_root_folder_content(current_backup, current_path)
            self.accept()
        return


class signupdialog(QDialog):
    def __init__(self, ui, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Sign Up')
        self.resize(400, 310)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.ui = ui
        self.frame = QFrame(self)
        self.frame.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self.frame)

        self.label_account = QtWidgets.QLabel()
        self.label_account.setText("Username")
        self.label_account.setFixedSize(400, 20)
        self.verticalLayout.addWidget(self.label_account)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setFixedSize(370, 30)
        # self.lineEdit_account.setPlaceholderText("Username")
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.label_password = QLabel()
        self.label_password.setText("Password")
        self.label_password.setFixedSize(400, 20)
        self.verticalLayout.addWidget(self.label_password)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setFixedSize(370, 30)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.lineEdit_password.setPlaceholderText("Password")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.path_show = QLabel()
        self.path_show.setFixedSize(400, 20)
        self.verticalLayout.addWidget(self.path_show)
        self.path_show.setText("Path")

        self.lineEdit_path = QLineEdit()
        self.lineEdit_path.setFixedSize(370, 30)
        self.verticalLayout.addWidget(self.lineEdit_path)

        self.pushButton_choose = QPushButton()
        self.pushButton_choose.setText("Set Path")
        self.verticalLayout.addWidget(self.pushButton_choose)
        self.pushButton_choose.clicked.connect(self.setpath)

        self.pushButton_signup = QPushButton()
        self.pushButton_signup.setText("Sign Up")
        self.verticalLayout.addWidget(self.pushButton_signup)
        self.pushButton_signup.clicked.connect(self.enter_main_frame)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("Cancel")
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.warning = QLabel()
        self.warning.setFixedSize(400, 20)
        self.verticalLayout.addWidget(self.warning)

        # self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)

    def enter_main_frame(self):
        global current_user
        res = current_user.signup(self.lineEdit_account.text(), self.lineEdit_password.text(), self.lineEdit_path.text())
        if res[0] == False:
            self.warning.setText("Sign up failed")
        else:
            current_user = res[1]
            current_user.print_all()
            current_user.create_folder_on_server()
            self.close()
            self.ui.accept()

        # self.ui.show()
        # self.ui.exec_()

    def setpath(self):
        path = QFileDialog.getExistingDirectory(self, 'Choose Backup Directory', './')

        # print(path)
        # print(type(path))
        self.lineEdit_path.setText(path)
        return path


app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
dialog = logindialog()
if dialog.exec_() == QDialog.Accepted:
    Form = QMainWindow()
    ui = Ui_RU_Backup()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
