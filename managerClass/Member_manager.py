import pandas as pd


class Member_manager:
    def __init__(self, db):
        self.db = db

    def checkID(self, member_id):
        query = "SELECT EXISTS(SELECT 1 FROM member WHERE member_id = %s)"
        values = (member_id,)
        checkPoint = self.db.fetch(query, values)
        return checkPoint[0][0] if checkPoint else False

    def addMember(self, member_name):
        if not all(member_name):
            return "ERROR: thie du lieu ten thanh vien"
        query = "INSERT INTO member(member_name) VALUES(%s)"
        values = (member_name,)
        self.db.execute(query, values)
        return "DONE"

    def delMember(self, member_id):
        query = "DELETE FROM member WHERE member_id = %s"
        values = (member_id,)
        self.db.execute(query, values)
        return "Done"

    def displayMember(self):
        query = "SELECT * FROM member ORDER BY member_id"
        data = self.db.fetch(query)
        df = pd.DataFrame(data, columns=["MemberID", "MemberName"])
        return df
