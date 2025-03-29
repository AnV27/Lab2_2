from tkinter import N
import pandas as pd
import Database


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
        self.borrow_id = borrow_id
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date

    def checkIdBorrow(self, db, borrow_id):

        query = "SELECT EXISTS(SELECT 1 FROM borrow_book WHERE borrow_id = %s)"
        values = (borrow_id,)
        checkPoint = db.fetch(query, values)
        return bool(checkPoint[0][0]) if checkPoint else False

    def borrow(self, db: Database, book_id: int, member_id: int):
        query = (
            "INSERT INTO borrow_book(book_id,member_id,return_date) VALUES(%s,%s,NULL)"
        )
        values = (book_id, member_id)
        return db.execute(query, values)

    def returnBook(self, db: Database, borrow_id: int):
        if not self.checkIdBorrow(db, borrow_id):
            return False
        # sửa lỗi chính tả trong câu truy vấn SQL
        query = "UPDATE borrow_book SET return_date = CURRENT_DATE WHERE borrow_id = %s"
        values = (borrow_id,)
        db.execute(query, values)
        return True

    def displayOverDueBorrow(self, db: Database):
        # truy van thong tin muon sach va thanh vien + ngay qua han
        query = "SELECT\
                    bb.borrow_id,\
                    bb.book_id,\
                    m.member_id,\
                    m.member_name,\
                    bb.borrow_date,\
                    bb.due_date,\
                    bb.return_date,\
                    AGE(CURRENT_DATE, bb.due_date) AS over_due\
                FROM borrow_book AS bb\
                JOIN member AS m USING (member_id)\
                WHERE bb.return_date IS NULL\
                ORDER BY bb.borrow_id;"
        data = db.fetch(query, values=None)
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
