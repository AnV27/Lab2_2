import pandas as pd


class borrow_manager:
    def __init__(self, db):
        self.db = db

    def borrow(self, book_id, member_id):
        if not all(book_id, member_id):
            return "ERROR: thieu du lieu"
        query = (
            "INSERT INTO borrow_book(book_id,member_id,return_date) VALUES(%s,%s,NULL)"
        )
        values = (book_id, member_id)
        return self.db.execute(query, values)
