DATABASE_CONFIG = {
    'host': '35.223.248.16',
    'user': 'root',
    'password': 'CAMRYLOVESEDGE',
    'port': 3306
}

USER_CONFIG = {
    'user_name': '',

}

# 数据文件夹路径
DATA_DIR = "D:\data"


import raw_configs as config

assert config.DATABASE_CONFIG['host'] == 'localhost'
assert config.DATABASE_CONFIG['user'] == 'user'
assert config.DATABASE_CONFIG['password'] == 'password'
assert config.DATABASE_CONFIG['dbname'] == 'test'