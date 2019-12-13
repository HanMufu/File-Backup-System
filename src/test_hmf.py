import model
from model import User
import pymysql
import importlib
importlib.reload(model)

'''登陆测试'''
# a = User('', '', '', '')
# b = a.login('alice', 'alice')
# print(len(b))
# curr = b[1]
# curr.print_all()

'''注册测试'''
a = User('', '', '', '')
res = a.signup('tommy', 'tommy', '/Users/hanmufu/Downloads')
print(len(res))
bob = res[1]
bob.print_all()


# user_name = "alice"
# password_md5 = "alice"
# try:
#     login_connection = pymysql.connect(host='35.223.248.16', user='root', passwd='CAMRYLOVESEDGE', db="RUBackup",
#                                        port=3306)
#     cursor = login_connection.cursor()
# except:
#     print("Fail to connect database")
# user_name_for_sql = "'" + user_name + "'"
# sql = "select * from user_RUBackup where user_name = %s " % user_name_for_sql
#
# print(sql)