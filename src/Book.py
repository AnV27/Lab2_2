import pandas as pd
from Database import Database

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


class Book:
    def __init__(
        self,
        book_name,
        author,
        pages,
        category,
        release_year,
        status,
        description,
        book_id=None,
    ):
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.pages = pages
        self.category = category
        self.release_year = release_year
        self.status = status
        self.description = description

    def checkIdBook(self, db: Database, book_id: int):
        query = "SELECT EXISTS(SELECT 1 FROM book WHERE book_id = %s)"
        values = (book_id,)
        checkPoint = db.fetch(query, values)
        return bool(checkPoint[0][0]) if checkPoint else False

    # truyen tham so muon thay doi trang thai cua sach, khong truyen thi se tu dong cap nhat la "trang thai khac"
    def setStatus(self, db: Database, book_id, newStatus=2):
        if self.checkIdBook(db, book_id):
            query = "UPDATE book SET status = %s WHERE book_id = %s"
            values = (newStatus, book_id)

            db.execute(query, values)
        return

    def addBook(self, db: Database):
        # them thong tin sach (khong can tham so book_id vi book_id: SERIAL)
        query = (
            "INSERT INTO book(book_name, author, pages, category, release_year, status, description) "
            "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        )
        values = (
            self.book_name,
            self.author,
            self.pages,
            self.category,
            self.release_year,
            self.status,
            self.description,
        )
        return db.execute(query, values)

    def removeBook(self, db: Database, book_id: int):
        if self.checkIdBook(db, book_id):
            query = "DELETE FROM book WHERE book_id = %s"
            values = (book_id,)
            return db.execute(query, values)
        return False

    def displayAllBooks(self, db: Database):
        query = "SELECT * FROM book ORDER BY book_id"
        data = db.fetch(query)
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data, columns=columnsBook)
        return df

    def displayOneBook(self, db: Database, book_id: int):
        if not self.checkIdBook(db, book_id):
            return pd.DataFrame()

        query = "SELECT * FROM book WHERE book_id = %s"
        values = (book_id,)
        data = db.fetch(query, values)

        df = pd.DataFrame(data, columns=columnsBook)
        return df

    def displayAvailableBooks(self, db: Database):
        query = "SELECT * FROM book WHERE status = 0 ORDER BY book_id"
        data = db.fetch(query, values=None)
        if not data:
            return pd.DataFrame()
        # kiem tra xem co sach nao co trang thai = 0 hay khong
        df = pd.DataFrame(data, columns=columnsBook)
        return df

    def updateBookInfo(
        self,
        db: Database,
        book_id,
        book_name=None,
        author=None,
        pages=None,
        category=None,
        release_year=None,
        status=None,
        description=None,
    ):
        if not self.checkIdBook(db, book_id):
            return False

        query = "UPDATE book SET "
        updates = []
        values = []

        if book_name:
            updates.append("book_name = %s")
            values.append(book_name)
        if author:
            updates.append("author = %s")
            values.append(author)
        if pages:
            updates.append("pages = %s")
            values.append(pages)
        if category:
            updates.append("category = %s")
            values.append(category)
        if release_year:
            updates.append("release_year = %s")
            values.append(release_year)
        if status:
            updates.append("status = %s")
            values.append(status)
        if description:
            updates.append("description = %s")
            values.append(description)

        query += ", ".join(updates) + " WHERE book_id = %s"
        values.append(book_id)

        return db.execute(query, tuple(values))
