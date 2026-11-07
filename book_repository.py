import db

def list_books(only_available=False):
    with db.connect() as conn:
        return conn.execute("SELECT * FROM books WHERE available = 1" if only_available else "SELECT * FROM books").fetchall()
def get_book(book_id):
    with db.connect() as conn: return conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
def create_book(title, author, isbn):
    with db.connect() as conn:
        cur = conn.execute("INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, 1)", (title, author, isbn))
        return conn.execute("SELECT * FROM books WHERE id = ?", (cur.lastrowid,)).fetchone()
def delete_book(book_id):
    with db.connect() as conn: conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
def set_availability(book_id, available):
    with db.connect() as conn: conn.execute("UPDATE books SET available = ? WHERE id = ?", (int(available), book_id))
def count_books():
    with db.connect() as conn: return conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
