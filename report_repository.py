import db

def list_open_loans_with_details():
    with db.connect() as conn:
        return conn.execute("""SELECT loans.id, books.title, members.name, loans.due_date
        FROM loans JOIN books ON books.id = loans.book_id
        JOIN members ON members.id = loans.member_id WHERE loans.returned = 0""").fetchall()
