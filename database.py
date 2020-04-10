import pymysql

class DB():
    def __init__(self, host='localhost', port=3306, user='root', passoword='password',database='building',charset='utf8'):
        self.db =pymysql.connect(
            host = host,
            port =port,
            user=user,
            passoword=passoword,
            database = database,
            charset = charset
        )
        # 获取一个光标
        self.cursor = self.db.cursor()


    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.db.close()

    def createTable(self):
    #Create table
        self.cursor.execute("DROP TABLE IF EXISTS BUILDING3")
        sql = """CREATE TABLE BUILDING3 (
            ID INT AUTO_INCREMENT UNSIGNED,
            NAME  VARCHAR(50) NOT NULL,
            VALUE INT,
            TYPE VARCHAR(50),
            PARENT  TINYINT"""

        self.cursor.execute(sql)

    def insertEle(self, name, value, type, parent):
        sql2 = "INSERT INTO BUILDING3(NAME, VALUE, TYPE, PARENT) \
                    VALUES (%s, %s, %s, %s)" \
               %(name, value, type, parent)

        try:
            # 执行sql语句
            self.cursor.execute(sql2)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()



if __name__ == '__main__':
    db =DB(database="building")
    db.insertEle()
