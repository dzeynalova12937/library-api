import db

def list_members():
    with db.connect() as conn: return conn.execute("SELECT * FROM members").fetchall()
def get_member(member_id):
    with db.connect() as conn: return conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
def get_member_by_email(email):
    with db.connect() as conn: return conn.execute("SELECT * FROM members WHERE email = ?", (email,)).fetchone()
def create_member(name, email, member_type):
    with db.connect() as conn:
        cur = conn.execute("INSERT INTO members (name, email, type) VALUES (?, ?, ?)", (name, email, member_type))
        return conn.execute("SELECT * FROM members WHERE id = ?", (cur.lastrowid,)).fetchone()
