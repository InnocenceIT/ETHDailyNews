import pymysql
import time

HOST = "10.10.10.222"
DB = "mydb"
USER = "root"
PASSWORD = "ly7211123"


class DBUtil:
    @classmethod
    def getConnect(cls) -> pymysql.Connect:
        return pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DB, charset="utf8")

    @classmethod
    def inserr(cls, sql: str, parms: list):
        conn = DBUtil.getConnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.executemany(sql, parms)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def select(cls, sql: str):
        conn = DBUtil.getConnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @classmethod
    def update(cls, sql: str):
        conn = DBUtil.getConnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        conn.commit()
        conn.rollback()

    @classmethod
    def dict_2_str(cls, dic: dict):
        """将字典变成，key='value',key='value' 的形式"""
        tmplist = []
        for k, v in dic.items():
            if type(v) is time:
                vStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(v))
            else:
                vStr = str(v)
            tmp = "%s='%s'" % (str(k), vStr)
            tmplist.append(' ' + tmp + ' ')
        return ','.join(tmplist)


def main():
    sql = """SELECT * FROM `T_Proxy` WHERE `host`='q'"""
    dailiList = DBUtil.select(sql)
    for dic in dailiList:
        print(dic)


if __name__ == '__main__':
    main()
