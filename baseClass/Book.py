class Book:
    def __init__(
        self,
        book_id,
        book_name,
        author,
        pages,
        category,
        release_year,
        status,
        description,
    ):
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.pages = pages
        self.category = category
        self.release_year = release_year
        self.status = status
        self.description = description
