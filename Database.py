import psycopg2


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
        # thuc hien lenh sql
        self.cur.execute(query, values or ())
        # commit cau lenh -> cap nhat table
        self.conn.commit()

    # lay du lieu tu truy van db
    def fetch(self, query, values=None):
        self.cur.execute(query, values or ())
        # tra du lieu
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
        return "Close done"
