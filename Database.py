import psycopg2
import configparser

# doc du lieu tu config file
config = configparser.ConfigParser()
config.read("f:/Document/Tổng hợp các môn học/Python Programming/Lab/Lab 2/Bài 2/.ini")
dbname = config["database"]["dbName"]
hostname = config["database"]["hostName"]
password = config["database"]["password"]
username = config["database"]["userName"]
port = config.getint("database", "port")


class Database:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        # thuoc tinh self.conn de ket noi voi database
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        # con tro
        self.cur = self.conn.cursor()

    # phuong thuc cap nhat, chinh sua database
    def execute(self, query, values=None):
        try:
            # thuc hien lenh sql
            self.cur.execute(query, values or ())
            # commit cau lenh -> cap nhat table
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Database execution error: {e}")
            return False

    # lay du lieu tu truy van db
    def fetch(self, query, values=None):
        try:
            self.cur.execute(query, values or ())
            # tra du lieu
            return self.cur.fetchall()
        except Exception as e:
            print(f"Database fetch error: {e}")
            return []

    def close(self):
        self.cur.close()
        self.conn.close()
        return "Close done"
