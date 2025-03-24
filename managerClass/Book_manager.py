from Database import Database
import pandas as pd

columnsBook = (
    "BookID",
    "Title",
    "Author",
    "Pages",
    "Category",
    "ReleaseYear",
    "Status",
    "Description",
)


class Book_manager:
    def __init__(self, db: Database):
        self.db = db

    def checkID(self, book_id):
        query = "SELECT EXISTS(SELECT 1 FROM book WHERE book_id = %s)"
        values = (book_id,)
        checkPoint = self.db.fetch(query, values)
        return checkPoint[0][0] if checkPoint else False

    def setStatus(self, newStatus: int, book_id: int):
        query = "UPDATE book SET status = %s WHERE book_id = %s"
        values = (newStatus, book_id)
        return self.db.execute(query, values)

    # them 1 quyen sach vao thu vien
    def addBook(
        self, book_name, author, pages, category, release_year, status, description
    ):
        if not all([book_name, author, category, release_year, description]):
            return "ERROR: thieu thong tin sach"
        query = (
            "INSERT INTO book(book_name, author, pages, category, release_year, status, description) "
            "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        )
        values = (book_name, author, pages, category, release_year, status, description)
        self.db.execute(query, values)
        return "DONE! ADD BOOK "

    # khoa sach trong thu vien theo id
    def delBook(self, book_id: int):
        query = "DELETE FROM book WHERE book_id = %s"
        values = book_id
        self.db.execute(query, values)
        return "DONE! DEL BOOK"

    # hien thi tat ca cac sach dang co trong thu vien
    def displayAll(self):
        query = "SELECT * FROM book ORDER BY book_id"
        df = self.db.fetch(query)
        df = pd.DataFrame(df, columns=columnsBook)
        return df

    # chi hien cac sach hien tai dang co
    def displayHaveBook(self):
        query = "SELECT * FROM book WHERE status = 0 ORDER BY book_id"
        data = self.db.fetch(query)
        df = pd.DataFrame(data, columns=columnsBook)
        return df

    # search func
    def displayOneBook(self, book_id):
        if not self.checkID(book_id):
            return "khong tim thay"
        query = "SELECT * FROM book WHERE book_id = %s"
        values = (book_id,)
        return pd.DataFrame(self.db.fetch(query, values), columns=columnsBook)
