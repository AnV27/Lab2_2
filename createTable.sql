CREATE TABLE book (
    book_id SERIAL PRIMARY KEY,
    book_name VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    category VARCHAR(255),
    release_year INTEGER CHECK (release_year BETWEEN 1000 AND 3000),
    status SMALLINT DEFAULT 2,
    description VARCHAR(255)
);

CREATE TABLE member (
    member_id SERIAL PRIMARY KEY,
    member_name VARCHAR(255) NOT NULL
);

CREATE TABLE borrow_book (
    borrow_id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    borrow_date DATE DEFAULT CURRENT_DATE,
    -- Hạn trả sách là 14 ngày kể từ ngày mượn
    due_date DATE GENERATED ALWAYS AS (borrow_date + INTERVAL '14 days') STORED,
    return_date DATE DEFAULT NULL,
    
    -- Khoá phụ
    CONSTRAINT fk_borrow_book FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE,
    CONSTRAINT fk_borrow_member FOREIGN KEY (member_id) REFERENCES member(member_id) ON DELETE CASCADE
);
-- Thêm thuộc tính cho bảng book, quên thêm ở lệnh CREATE table
ALTER TABLE student ADD COLUMMNS pages INT;