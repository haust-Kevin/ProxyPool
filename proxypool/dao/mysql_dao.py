import pymysql as pymysql

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'password'
MYSQL_DB = 'proxy'


# CREATE DATABASE proxy
# CREATE TABLE allowed_user(
# 	NAME VARCHAR(10) UNIQUE PRIMARY KEY,
# 	PASSWORD VARCHAR(20) NOT NULL
# );


class MysqlConn:
    def __init__(self):
        self.conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
        self.cursor = self.conn.cursor()

    def exist(self, name, pwd):
        sql = 'select * from allowed_user where name=%s and password=%s'
        self.cursor.execute(sql, (name, pwd))
        if self.cursor.fetchone() is None:
            return False
        return True

    def __del__(self):
        self.cursor.close()
        self.conn.close()
