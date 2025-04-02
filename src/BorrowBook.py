import pandas as pd
from src.Database import Database


# Lớp BorrowBook quản lý các chức năng liên quan đến việc mượn và trả sách
class BorrowBook:
    def __init__(
        self,
        borrow_id,
        book_id,
        member_id,
        borrow_date,
        due_date,
        return_date,
    ):
        # Khởi tạo các thuộc tính của đối tượng BorrowBook
        self.borrow_id = borrow_id  # ID của giao dịch mượn sách
        self.member_id = member_id  # ID của thành viên mượn sách
        self.book_id = book_id  # ID của sách được mượn
        self.borrow_date = borrow_date  # Ngày mượn sách
        self.due_date = due_date  # Ngày phải trả sách
        self.return_date = return_date  # Ngày trả sách

    def checkIdBorrow(self, db, borrow_id):
        # Kiểm tra xem borrow_id có tồn tại trong cơ sở dữ liệu hay không
        query = "SELECT EXISTS(SELECT 1 FROM borrow_book WHERE borrow_id = %s)"
        values = (borrow_id,)
        checkPoint = db.fetch(query, values)
        return bool(checkPoint[0][0]) if checkPoint else False

    def borrow(self, db: Database, book_id: int, member_id: int):
        # Thêm giao dịch mượn sách vào cơ sở dữ liệu
        query = (
            "INSERT INTO borrow_book(book_id,member_id,return_date) VALUES(%s,%s,NULL)"
        )
        values = (book_id, member_id)
        return db.execute(query, values)

    def returnBook(self, db: Database, borrow_id: int):
        # Xử lý trả sách, cập nhật ngày trả sách trong cơ sở dữ liệu
        if not self.checkIdBorrow(db, borrow_id):
            return False
        query = "UPDATE borrow_book SET return_date = CURRENT_DATE WHERE borrow_id = %s"
        values = (borrow_id,)
        db.execute(query, values)
        return True

    def displayOverDueBorrow(self, db: Database):
        # Hiển thị danh sách các giao dịch mượn sách quá hạn
        query = "SELECT \
                    bb.borrow_id,\
                    bb.book_id,\
                    mb.member_id,\
                    mb.member_name,\
                    bb.borrow_date,\
                    bb.due_date,\
                    bb.return_date,\
                    (bb.return_date - bb.due_date) * INTERVAL '1 day' AS over_due\
                FROM \
                    borrow_book AS bb\
                INNER JOIN \
                    member AS mb USING (member_id)\
                WHERE \
                    bb.return_date IS NOT NULL \
                    AND (\
                        bb.return_date > bb.borrow_date \
                        OR CURRENT_DATE > bb.due_date\
                    )\
                    AND (bb.return_date - bb.due_date) * INTERVAL '1 day' >= INTERVAL '1 day';"
        data = db.fetch(query, values=None)
        # Chuyển dữ liệu thành DataFrame để dễ dàng xử lý và hiển thị
        df = pd.DataFrame(
            data,
            columns=[
                "borrowID",
                "bookID",
                "memberID",
                "member_name",
                "borrow_date",
                "due_date",
                "return_date",
                "over_due",
            ],
        )
        return df
