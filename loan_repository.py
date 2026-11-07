import db

def list_loans():
    with db.connect() as conn: return conn.execute("SELECT * FROM loans").fetchall()
def list_loans_for_member(member_id):
    with db.connect() as conn: return conn.execute("SELECT * FROM loans WHERE member_id = ?", (member_id,)).fetchall()
def get_loan(loan_id):
    with db.connect() as conn: return conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
def create_loan(book_id, member_id, due_date, checked_out):
    with db.connect() as conn:
        cur = conn.execute("INSERT INTO loans (book_id, member_id, due_date, checked_out) VALUES (?, ?, ?, ?)", (book_id, member_id, due_date, checked_out))
        conn.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
        return conn.execute("SELECT * FROM loans WHERE id = ?", (cur.lastrowid,)).fetchone()
def mark_returned(loan_id, book_id, fine):
    with db.connect() as conn:
        conn.execute("UPDATE loans SET returned = 1, fine = ? WHERE id = ?", (fine, loan_id))
        conn.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
        return conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
def extend_loan(loan_id, new_due_date):
    with db.connect() as conn:
        conn.execute("UPDATE loans SET due_date = ?, renewals = renewals + 1 WHERE id = ?", (new_due_date, loan_id))
        return conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
def mark_fine_paid(loan_id):
    with db.connect() as conn:
        conn.execute("UPDATE loans SET fine_paid = 1 WHERE id = ?", (loan_id,))
        return conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
