class BorrowBook:
    def __init__(
        self, borrow_id, member_id, book_id, borrow_date, due_date, return_date
    ):
        self.borrow_id = borrow_id
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date
