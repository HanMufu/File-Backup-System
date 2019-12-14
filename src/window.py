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
import Scanner

# 这三条是windows的一个配置信息，我觉得在mac跑可能不一定需要这三行
# dirname = os.path.dirname(PySide2.__file__)
# plugin_path = os.path.join(dirname, 'plugins', 'platforms')
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


def getlist(dir):
    return os.listdir(dir)

current_user: User = User('', '', '', '')
current_backup: Backup = ('', '', '')
current_folder: Item = Item('', '', '', '', '', '', '', '', '')
current_path: str = "/Users/hanmufu/Downloads/RUBackup_test_folder"  # 这里需要修改我用的是当前路径，应该要改成数据库内的虚拟的文件路径
# current_path = current_folder_item.filePath_Client
# 这里也要修改，我用的是os包自带的getlist方法，获取当前文件夹的每一条文件或文件夹信息，存到file_list这个list里面
file_item_list = []
file_list = getlist(current_path)
backup_list = []


# 这个list里面应该是每一个item都是一个我们定义的文件或文件夹实例
# 而且这里我是比较省事情就直接用了一个全局变量，所以你可能要import dbclass，然后每次点击那个下拉菜单里面的某一个条目的时候，需要把这个file_list刷新一下


class Ui_RU_Backup(object):
    def setupUi(self, RU_Backup):
        RU_Backup.setObjectName("RU_Backup")
        RU_Backup.resize(1210, 740)  # 420, 714
        # Doco.setFixedSize(420, 714)#
        # RU_Backup.setWindowFlags(QtCore.Qt.FramelessWindowHint)#隐藏默认窗口样式

        self.retranslateUi(RU_Backup)
        QtCore.QMetaObject.connectSlotsByName(RU_Backup)

        # self.login = QtWidgets.QPushButton(RU_Backup)
        # self.login.setGeometry(QtCore.QRect(0, 30, 50, 30))
        # self.login.setObjectName("Login")
        # self.login.setText("Login")

        self.tb = RU_Backup.addToolBar("Login")

        new = QAction(QIcon("./login.png"), "login", RU_Backup)
        new.triggered.connect(self.backpath_modify)
        self.tb.addAction(new)

        backup_start = QAction(QIcon("./back.png"),"Start Backup",RU_Backup)
        backup_start.triggered.connect(self.backup_start)
        self.tb.addAction(backup_start)

        self.dir_label = QLabel(RU_Backup)
        self.dir_label.setGeometry(QtCore.QRect(60, 100, 400, 30))

        
        #self.cb.addItem('2019/12/6 17:42')
        #self.cb.addItem('2019/12/8 20:11')
        # 这个函数是用来往下拉菜单添加item，每一个item应该都是一个时间戳，格式03/12/2019 17:19:03
        # 可以写一个for i in listoftimestamp: self.cb.addItem(i)
        # 然后下面还需要链接到一个clicked事件，比如clicked=Lambda:Refresh

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
        for n in range(0, len(file_item_list)):  # 这个地方就是对于file_list中的每个实例，创建一个小的Item，然后再Item中显示文件或文件夹名
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
        # 这个地方可以考虑用来作为用户更改备份文件夹路径的方法

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


    def selection_change(self):
        global current_path
        global current_backup
        global backup_list
        for i in backup_list:
            if i.backup_time == self.cb.currentText():
                current_backup = i
                current_path = i.backup_root_path_at_server #我不知道这个serverpath是不是string，你确认下
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
        self.name = QtWidgets.QLabel()  # 文件或文件夹名
        #self.file_path = current_path + file_list[self.n]
        self.type_label = QToolButton()
        if self.file_class.file_type == "folder":
            self.type_label.setIcon(QIcon("./dir.png"))
        else:
            self.type_label.setIcon(QIcon("./file.png"))
        self.play_btn = QtWidgets.QToolButton()
        self.play_btn.setIcon(QIcon("./download.png"))  # 这里需要一个def download方法，点击之后下载这个文件到本地
        self.play_btn.clicked.connect(self.download)
        self.info_btn = QtWidgets.QToolButton()  # 这里是显示文件信息的button，然后这个点击一下之后需要显示出来一个新窗口，在底下InfoQWidget
        self.info_btn.clicked.connect(self.info_pre.show)
        self.info_btn.setIcon(QIcon("./info.png"))
        self.textQHBoxLayout.addWidget(self.type_label)
        self.textQHBoxLayout.addWidget(self.name)
        self.textQHBoxLayout.addWidget(self.play_btn)
        self.textQHBoxLayout.addWidget(self.info_btn)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.allQHBoxLayout.addLayout(self.textQHBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

    def setName(self):
        self.name.setText(self.file_class.fileName)

    def mouseDoubleClickEvent(self, e):  # 双击事件，如果这个item是文件夹且被双击了，
        # 那么就进入这个文件夹里面，重新刷新一下路径表，这里使用的是os.path，但是我们应该要换成写出来的自己的path
        global current_path
        global file_list
        global file_item_list
        global current_backup
        global current_backup
        # print("clicked"+self.name.text())
        current_path = current_path + self.name.text() + "/"
        self.ui.dir_label.setText(current_path)
        
        if self.file_class.file_type == "folder":
            file_item_list = current_user.fetch_folder_content(self.file_class, current_backup)
            file_list = getlist(current_path)
            self.ui.music_list()  # 刷新路经表

    def download(self):
        print("download")
        #download(self.file_class)
        #这个位置插入吴越的download方法，self.file_class是一个文件类的对象，可以作为参数传入


class Event():
    def Pre(self):  # 这个方法就是返回上一级菜单，就是那个back按钮
        global current_path
        global file_list
        cache = current_path.split("/")
        le = len(cache[len(cache) - 2]) + 1
        current_path = current_path[:-le]
        file_list = getlist(current_path)
        self.dir_label.setText(current_path)
        self.music_list()  # 刷新路经表
        # print(file_list)


class infodialog(QDialog):  # 这个dialog是用来新打开一个窗口显示文件的各种信息的
    def __init__(self, file_class, *args, **kwargs):  # 这里需要传入一个自己定义的file_list里面的实例file_info
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

        # self.lineEdit_account.text()这里可以用这个 函数采集用户输入的username然后用后端函数操作

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
        # 这个path就是用户选择的path，这里要加上后端对于path处理的函数
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
