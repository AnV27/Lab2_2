from ast import main
from src import Book, Member, BorrowBook
import Database

# doi tuong ket noi voi db
db = Database.Database(
    dbname=Database.dbname,
    user=Database.username,
    password=Database.password,
    host=Database.hostname,
    port=Database.port,
)

mainBook = Book.Book(
    book_id=None,
    book_name="",
    author="",
    pages=0,
    category="",
    release_year=1000,
    status=0,
    description="",
)

mainMember = Member.Member(None, "")

mainBorrowBook = BorrowBook.BorrowBook(
    borrow_id=None,
    book_id=None,
    member_id=None,
    borrow_date="",
    due_date="",
    return_date="",
)

while True:
    print("\n=== Hệ thống thư viện ===")
    print("1. Thêm sách")
    print("2. Xoá sách")
    print("3. Hiển thị tất cả sách có thể mượn")
    print("4. Tìm kiếm sách")

    print("5. Đăng ký thành viên")
    print("6. Xóa thành viên")
    print("7. Hiển thị danh sách thành viên")
    print("8. Tìm kiếm thành viên")

    print("9. Mượn sách")
    print("10. Trả sách")
    print("11. Hiển thị các sách trả quá hạn trả")

    print("12. Sửa thông tin sách")
    print("13. Sửa thông thành viên")

    print("0. Thoát")

    choice = input("Nhập lựa chọn: ")

    match choice:
        # Book
        case "1":  # test thành công
            # ID kiểu dữ liệu là SERIAL nên không cần inpput
            book_name = input("Nhập tên sách thêm vào: ")
            author = input("Nhập tên tác giả: ")
            pages = int(input("Nhập tổng số trang sách: "))
            category = input("Nhập thể loại sách: ")
            release_year = int(input("Nhập năm phát hành sách: "))
            status = int(
                input(
                    "Nhập trạng thái sách (0: có sẵn, 1: đã mượn, 2: trạng thái khác): "
                )
            )
            description = input("Nhập mô tả sách: ")
            newBook = Book.Book(
                book_name=book_name,
                author=author,
                pages=pages,
                category=category,
                release_year=release_year,
                status=status,
                description=description,
            )
            result = newBook.addBook(db)
            if result:
                print("Đã thêm sách vào thư viện thành công!")
            else:
                print("ERROR: Thêm sách mới thất bại")

        case "2":
            book_id = int(input("Nhập id sách muốn xoá: "))

            if mainBook.removeBook(db, book_id):
                print(f"Xóa sách {book_id} thành công!")
            else:
                print(f"ERROR: Book_id {book_id} không tồn tại")

        case "3":
            result = mainBook.displayAvailableBooks(db)
            if result.empty:
                print("Không còn sách để có thể mượn")
            else:
                print(result)
                print("Đã hiện thị danh sách thành công!")

        case "4":
            book_id = int(input("Nhập id sách cần tìm: "))
            result = mainBook.displayOneBook(db, book_id)
            if result.empty:
                print("Không tìm thấy sách")
            else:
                print(result)
                print("Đã tìm thấy sách thành công!")

        # Member
        case "5":
            # ID kiểu dữ liệu là SERIAL nên không cần inpput
            member_name = input("Nhập tên thành viên muốn thêm vào: ")
            newMember = Member.Member(member_name=member_name)
            if newMember.addMember(db):
                print("Đã thêm thành viên mới thành công!")
            else:
                print("ERROR: Thêm thành viên mới thất bại")

        case "6":
            member_id = int(input("Nhập id thành viên muốn xóa: "))
            if mainMember.removeMember(db, member_id):
                print(f"Xóa thành viên {member_id} thành công!")
            else:
                print(f"ERROR: Member_id {member_id} không tồn tại")

        case "7":
            result = mainMember.displayAllMember(db)
            if result.empty:
                print("Không có thành viên nào trong danh sách")
            else:
                print(result)
                print("Đã hiển thị danh sách thành viên thành công!")

        case "8":
            member_id = int(input("Nhập id thành viên cần tìm: "))
            result = mainMember.displayOneMember(db, member_id)
            if result.empty:
                print("Không tìm thấy thành viên")
            else:
                print(result)
                print("Đã hiển thị thành viên cần tìm thành công!")

        case "9":
            book_id = int(input("Nhập id sách muốn mượn: "))
            member_id = int(input("Nhập id thành viên mượn sách: "))
            if mainBook.checkIdBook(db, book_id) and mainMember.checkIdMember(
                db, member_id
            ):
                mainBorrowBook.borrow(db, book_id, member_id)
                mainBook.setStatus(db, book_id, 1)  # cập nhật trạng thái sách
                print("Đã cập nhật trạng thái sách thành công!")
                print("Mượn sách thành công!")
            else:
                print("ERROR: Mượn sách thất bại")

        case "10":
            borrow_id = int(input("Nhập id mượn sách để trả: "))
            if mainBorrowBook.returnBook(db, borrow_id):
                mainBook.setStatus(db, borrow_id, 0)  # cập nhật trạng thái sách
                print("Đã cập nhật trạng thái sách thành công!")
                print("Trả sách thành công!")
            else:
                print("ERROR: Trả sách thất bại")

        case "11":
            result = mainBorrowBook.displayOverDueBorrow(db)
            if not result.empty:
                print(result)
            else:
                print("Không có sách trả quá hạn")

        case "12":
            book_id = int(input("Nhập id sách cần sửa thông tin: "))
            if mainBook.checkIdBook(db, book_id):
                book_name = input("Nhập tên sách mới (để trống nếu không đổi): ")
                author = input("Nhập tên tác giả mới (để trống nếu không đổi): ")
                pages = input("Nhập tổng số trang mới (để trống nếu không đổi): ")
                category = input("Nhập thể loại mới (để trống nếu không đổi): ")
                release_year = input(
                    "Nhập năm phát hành mới (để trống nếu không đổi): "
                )
                status = input("Nhập trạng thái mới (để trống nếu không đổi): ")
                description = input("Nhập mô tả mới (để trống nếu không đổi): ")
                if mainBook.updateBookInfo(
                    db,
                    book_id,
                    book_name,
                    author,
                    pages,
                    category,
                    release_year,
                    status,
                    description,
                ):
                    print("Cập nhật thông tin sách thành công!")
                else:
                    print("ERROR: Cập nhật thông tin sách thất bại")
            else:
                print("Không tìm thấy sách")

        case "13":
            member_id = int(input("Nhập id thành viên cần sửa thông tin: "))
            if mainMember.checkIdMember(db, member_id):
                member_name = input(
                    "Nhập tên thành viên mới (để trống nếu không đổi): "
                )
                if mainMember.updateMemberInfo(db, member_id, member_name):
                    print("Cập nhật thông tin thành viên thành công!")
                else:
                    print("ERROR: Cập nhật thông tin thành viên thất bại")
            else:
                print("Không tìm thấy thành viên")

        case "0":
            db.close()
            print("Thoát chương trình!")
            break
        case _:
            print("Lựa chọn không hợp lệ, vui lòng nhập lại!")
