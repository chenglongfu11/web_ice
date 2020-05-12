import datetime
import sys
import traceback

import pymysql

import config


class DB():
    def __init__(self, host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER,
                 password=config.MYSQL_PASSWD, database='energy_report_consumption', charset='utf8'):
        # connect to db with name
        self.db = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset
        )
        # get a cursor
        self.cursor = self.db.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.db.close()

    def createDatabase(self):
        """因为创建数据库直接修改settings中的配置MYSQL_DBNAME即可，所以就不要传sql语句了"""
        conn = self.connectMysql()  # 连接数据库

        sql = "create database if not exists " + self.db
        cur = conn.cursor()
        cur.execute(sql)  # 执行sql语句
        cur.close()
        conn.close()

    # 创建表
    def createTable(self, sql):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def createTable(self):
        # Create table
        self.cursor.execute("DROP TABLE IF EXISTS Lighting,facility")
        sql = """CREATE TABLE Lighting,facility (
            ID INT AUTO_INCREMENT UNSIGNED,
            NAME  VARCHAR(50) NOT NULL,
            VALUE NUMBER,
            VALUE NUMBER, 
            VALUE NUMBER,
            VALUE NUMBER,
            VALUE NUMBER,
            VALUE NUMBER,
            VALUE NUMBER,
            VALUE NUMBER,
            VALUE NUMBER,
            VALUE NUMBER,
            VALUE NUMBER,
            VALUE NUMBER,  
            PARENT  TINYINT"""

        self.cursor.execute(sql)

    def insertBuil(self, building_name, table_name="`building_info`"):
        sql1 = "INSERT IGNORE INTO " + table_name + " (building_name) VALUES (%s)"
        value1 = (building_name,)
        self.cursor.execute(sql1, value1)

        try:
            self.cursor.execute(sql1, value1)
            self.db.commit()
            sqlq = "SELECT * FROM " + table_name + " WHERE `building_name` = %s"
            valq = (building_name,)
            self.cursor.execute(sqlq, valq)

            return self.cursor.fetchone()[0]

        except:
            # If error, rollback
            self.db.rollback()
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)
            return False

    # Unique building information in the table, when exist, no insert action.  The return value is bid
    def insertBuil2(self, building_name, table_name="`building_info`"):
        sql1 = "insert into " + table_name + " (id, building_name)\
                select null, %s from DUAL\
                where not exists (select id from building_info where building_name = %s)"
        value1 = (building_name, building_name)
        self.cursor.execute(sql1, value1)

        try:
            self.cursor.execute(sql1, value1)
            self.db.commit()
            sqlq = "SELECT * FROM " + table_name + " WHERE `building_name` = %s"
            valq = (building_name,)
            self.cursor.execute(sqlq, valq)

            return self.cursor.fetchone()[0]

        except:
            # 如果发生错误则回滚
            self.db.rollback()
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)
            return False

    def insertSimu(self, bid, simu_opt="Make some changes", table_name="simulation_info"):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        sql1 = "INSERT INTO " + table_name + " (bid,simulation_option,simu_time) VALUES (%s,%s,%s)"
        value1 = (bid, simu_opt, formatted_date)
        try:
            self.cursor.execute(sql1, value1)
            self.db.commit()
            sid = self.cursor.lastrowid
            return sid
        except:
            self.db.rollback()
            return False

    # table name: consump_electric_cooling        consump_equipment_tenant         consump_fuel_heating
    # consump_hvac consump_lighting_facility    consump_domestic_hot_water
    def insertEle(self, check, sid, bid, val,
                  table_name="`consump_domestic_hot_water`"):  # fisrt non-defalut argument, then default argument

        # insert into consumption table 12 months

        if check == 1:
            if len(val) < 12:
                lenth = len(val)
                for i in range(12 - lenth):
                    x = 0
                    val.append(x)

            sql2 = "INSERT INTO " + table_name + " (sid,bid, month1, month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12) \
                        VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            value = (
            sid, bid, val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], val[9], val[10], val[11])

        # insert into peak power table
        # table name: pk_power_hvac pk_power_fuel_heating pk_power_equipment_tenant pk_power_electric_cooling
        # pk_power_domestic_hot_water pk_power_hvac pk_power_lighting_facility
        else:
            sql2 = "INSERT INTO " + table_name + " (sid, bid, pk_power) VALUES (%s, %s, %s)"
            value = (sid, bid, val)

        try:
            # 执行sql语句
            self.cursor.execute(sql2, value)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

    def delete(self, sql, *params):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()


# unit test
class TestDBHelper():
    def __init__(self):
        self.db = DB()

    # test insertBuil function
    def testInsertBuil2(self):
        return self.db.insertBuil("by")

    # test insertSimu function
    def testInsertSimu(self):
        bid = self.testInsertBuil2()
        if bid != False:
            return bid, self.db.insertSimu(bid)
        else:
            print('-' * 20)

    # test insertEle function- consumption 12 months
    def testInsertEle(self):
        bid, sid = self.testInsertSimu()
        if bid and sid:
            self.db.insertEle(sid, bid, [9, 9, 9, 9, 9, 9])

    # test insertEle function - pk-power
    def testInsertEle2(self):
        bid, sid = self.testInsertSimu()
        if bid and sid:
            self.db.insertEle(sid, bid, 11.1, 'pk_power_hvac')

    # -------------below are examples-------------

    def testCreateTable(self):
        sql = "create table testtable(id int primary key auto_increment,name varchar(50),url varchar(200))"
        self.dbHelper.createTable(sql)

    # 测试插入
    def testInsert(self):
        sql = "insert into testtable(name,url) values(%s,%s)"
        params = ("test", "test")
        self.dbHelper.insert(sql, *params)  # *表示拆分元组，调用insert（*params）会重组成元组

    def testUpdate(self):
        sql = "update testtable set name=%s,url=%s where id=%s"
        params = ("update", "update", "1")
        self.dbHelper.update(sql, *params)

    def testDelete(self):
        sql = "delete from testtable where id=%s"
        params = ("1")
        self.dbHelper.delete(sql, *params)


if __name__ == "__main__":
    testDBHelper = TestDBHelper()
    testDBHelper.testInsertEle2()
