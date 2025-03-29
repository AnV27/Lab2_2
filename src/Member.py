import pandas as pd


class Member:
    def __init__(self, member_name, member_id=None):
        self.member_id = member_id
        self.member_name = member_name

    def checkIdMember(self, db, member_id):
        query = "SELECT EXISTS(SELECT 1 FROM member WHERE member_id = %s)"
        values = (member_id,)
        checkPoint = db.fetch(query, values)

        return bool(checkPoint[0][0]) if checkPoint else False

    def addMember(self, db):
        query = "INSERT INTO member(member_name) VALUES(%s)"
        values = (self.member_name,)

        return db.execute(query, values)

    def removeMember(self, db, member_id):
        if not self.checkIdMember(db, member_id):
            return False

        query = "DELETE FROM member WHERE member_id = %s"
        values = (member_id,)

        db.execute(query, values)
        return True

    def displayOneMember(self, db, member_id):

        if not self.checkIdMember(db, member_id):
            return pd.DataFrame()

        query = "SELECT * FROM member WHERE member_id = %s"
        values = (member_id,)

        data = db.fetch(query, values)
        df = pd.DataFrame(data, columns=["MemberID", "MemberName"])
        return df

    def displayAllMember(self, db):
        # thuc hien truy van va hien thi danh sach sap xep theo ID
        query = "SELECT * FROM member ORDER BY member_id"
        data = db.fetch(query)

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data, columns=["MemberID", "MemberName"])
        return df

    def updateMemberInfo(self, db, member_id, member_name=None):
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
