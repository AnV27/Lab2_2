import pandas as pd
from src.Database import Database

# Định nghĩa các cột của bảng sách
columnsBook = (
    "BookID",
    "Title",
    "Author",
    "Category",
    "ReleaseYear",
    "Status",
    "Description",
    "Pages",
)


# Lớp Book quản lý các chức năng liên quan đến sách
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
        # Khởi tạo các thuộc tính của đối tượng Book
        self.book_id = book_id  # ID của sách
        self.book_name = book_name  # Tên sách
        self.author = author  # Tác giả
        self.pages = pages  # Số trang
        self.category = category  # Thể loại
        self.release_year = release_year  # Năm phát hành
        self.status = status  # Trạng thái (0: có sẵn, 1: đã mượn, 2: khác)
        self.description = description  # Mô tả sách

    def checkIdBook(self, db: Database, book_id: int):
        # Kiểm tra xem book_id có tồn tại trong cơ sở dữ liệu hay không
        query = "SELECT EXISTS(SELECT 1 FROM book WHERE book_id = %s)"
        values = (book_id,)
        checkPoint = db.fetch(query, values)
        return bool(checkPoint[0][0]) if checkPoint else False

    def setStatus(self, db: Database, book_id, newStatus=2):
        # Cập nhật trạng thái của sách
        if self.checkIdBook(db, book_id):
            query = "UPDATE book SET status = %s WHERE book_id = %s"
            values = (newStatus, book_id)
            db.execute(query, values)
        return

    def getStatus(self, db: Database, book_id):
        # Lấy trạng thái hiện tại của sách
        if self.checkIdBook(db, book_id):
            query = "SELECT status FROM book WHERE book_id = %s"
            values = (book_id,)
            data = db.fetch(query, values)
            return int(data[0][0]) if data else None

    def addBook(self, db: Database):
        # Thêm sách mới vào cơ sở dữ liệu
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
        # Xóa sách khỏi cơ sở dữ liệu
        if self.checkIdBook(db, book_id):
            query = "DELETE FROM book WHERE book_id = %s"
            values = (book_id,)
            return db.execute(query, values)
        return False

    def displayAllBooks(self, db: Database):
        # Hiển thị tất cả sách trong cơ sở dữ liệu
        query = "SELECT * FROM book ORDER BY book_id"
        data = db.fetch(query)
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data, columns=columnsBook)
        return df

    def displayOneBook(self, db: Database, book_id: int):
        # Hiển thị thông tin của một cuốn sách cụ thể
        if not self.checkIdBook(db, book_id):
            return pd.DataFrame()
        query = "SELECT * FROM book WHERE book_id = %s"
        values = (book_id,)
        data = db.fetch(query, values)
        df = pd.DataFrame(data, columns=columnsBook)
        return df

    def displayAvailableBooks(self, db: Database):
        # Hiển thị danh sách các sách có sẵn để mượn
        query = "SELECT * FROM book WHERE status = 0 ORDER BY book_id"
        data = db.fetch(query, values=None)
        if not data:
            return pd.DataFrame()
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
        # Cập nhật thông tin sách
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
