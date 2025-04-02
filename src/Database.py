import psycopg2
import configparser

# Đọc dữ liệu cấu hình từ file .ini
config = configparser.ConfigParser()
config.read("Lab2\Bài 2\.ini")

try:
    # Lấy thông tin cấu hình cơ sở dữ liệu
    dbname = config["database"]["dbName"]
    username = config["database"]["userName"]
    password = config["database"]["password"]
    hostname = config["database"]["hostName"]
    port = config.getint("database", "port")
except KeyError as e:
    raise KeyError(f"Missing required configuration key: {e}")


# Lớp Database quản lý kết nối và thao tác với cơ sở dữ liệu
class Database:
    def __init__(
        self,
        dbname=dbname,
        user=username,
        password=password,
        host="localhost",
        port="5432",
    ):
        # Kết nối với cơ sở dữ liệu
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self.cur = self.conn.cursor()  # Con trỏ để thực hiện truy vấn

    def execute(self, query, values=None):
        # Thực hiện câu lệnh SQL (INSERT, UPDATE, DELETE)
        try:
            self.cur.execute(query, values or ())
            self.conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
            return True
        except Exception as e:
            print(f"Database execution error: {e}")
            return False

    def fetch(self, query, values=None):
        # Lấy dữ liệu từ cơ sở dữ liệu (SELECT)
        try:
            self.cur.execute(query, values or ())
            return self.cur.fetchall()  # Trả về tất cả kết quả
        except Exception as e:
            print(f"Database fetch error: {e}")
            return []

    def close(self):
        # Đóng kết nối với cơ sở dữ liệu
        self.cur.close()
        self.conn.close()
        return "Close done"
