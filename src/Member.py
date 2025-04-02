import pandas as pd
from src.Database import Database


# Lớp Member quản lý các chức năng liên quan đến thành viên
class Member:
    def __init__(self, member_name, member_id=None):
        # Khởi tạo các thuộc tính của đối tượng Member
        self.member_id = member_id  # ID của thành viên
        self.member_name = member_name  # Tên thành viên

    def checkIdMember(self, db, member_id):
        # Kiểm tra xem member_id có tồn tại trong cơ sở dữ liệu hay không
        query = "SELECT EXISTS(SELECT 1 FROM member WHERE member_id = %s)"
        values = (member_id,)
        checkPoint = db.fetch(query, values)
        return bool(checkPoint[0][0]) if checkPoint else False

    def addMember(self, db):
        # Thêm thành viên mới vào cơ sở dữ liệu
        query = "INSERT INTO member(member_name) VALUES(%s)"
        values = (self.member_name,)
        return db.execute(query, values)

    def removeMember(self, db, member_id):
        # Xóa thành viên khỏi cơ sở dữ liệu
        if not self.checkIdMember(db, member_id):
            return False
        query = "DELETE FROM member WHERE member_id = %s"
        values = (member_id,)
        db.execute(query, values)
        return True

    def displayOneMember(self, db, member_id):
        # Hiển thị thông tin của một thành viên cụ thể
        if not self.checkIdMember(db, member_id):
            return pd.DataFrame()
        query = "SELECT * FROM member WHERE member_id = %s"
        values = (member_id,)
        data = db.fetch(query, values)
        df = pd.DataFrame(data, columns=["MemberID", "MemberName"])
        return df

    def displayAllMember(self, db):
        # Hiển thị danh sách tất cả thành viên, sắp xếp theo ID
        query = "SELECT * FROM member ORDER BY member_id"
        data = db.fetch(query)
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data, columns=["MemberID", "MemberName"])
        return df

    def updateMemberInfo(self, db, member_id, member_name=None):
        # Cập nhật thông tin thành viên
        if not self.checkIdMember(db, member_id):
            return False
        query = "UPDATE member SET "
        updates = []
        values = []
        if member_name:
            updates.append("member_name = %s")
            values.append(member_name)
        query += ", ".join(updates) + " WHERE member_id = %s"
        values.append(member_id)
        return db.execute(query, tuple(values))
