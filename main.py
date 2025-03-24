from managerClass import Book_manager
from managerClass import Member_manager
from Database import Database
import configparser

# doc du lieu tu config file
config = configparser.ConfigParser()
config.read("Lab 2\\Bài 2\\.ini")
dbname = config["database"]["dbName"]
hostname = config["database"]["hostName"]
password = config["database"]["password"]
username = config["database"]["userName"]
port = config.getint("database", "port")


db = Database(dbname=dbname, user=username, password=password, host=hostname, port=port)
book_manager = Book_manager.Book_manager(db)
member_manager = Member_manager.Member_manager(db)


# bookName = "Su im lang cua bay cuu"
# author = "tac gia"
# pages = 100
# category = "Sach giao khoa"
# release_year = 2000
# book_status = 1
# desc = "Toan"

# lst = ["An", "bao", "tu", "tuan", "hung", "hung", "nam"]
# for _ in lst:
#     print(member_manager.addMember(_))

# print(member_manager.displayMember())
