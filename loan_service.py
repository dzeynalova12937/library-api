from datetime import date, timedelta
import book_repository, member_repository, loan_repository, fines, validation, notifications
from errors import bad_request, conflict, not_found
LOAN_DAYS = 14
STUDENT_LIMIT = 3
STAFF_LIMIT = 5
MAX_RENEWALS = 1

def amount_owed(loan):
    if not loan["returned"]: return fines.fine_for(loan["due_date"])
    return 0 if loan["fine_paid"] else loan["fine"]
def total_owed(loans): return sum(amount_owed(loan) for loan in loans)
def count_open_loans(loans): return sum(not loan["returned"] for loan in loans)
def current_fine(loan): return fines.fine_for(loan["due_date"]) if not loan["returned"] else loan["fine"]
def is_overdue(loan): return not loan["returned"] and fines.days_late(loan["due_date"]) > 0
def loan_json(loan, include_current=False):
    result = {"id": loan["id"], "book_id": loan["book_id"], "member_id": loan["member_id"], "due_date": loan["due_date"], "returned": bool(loan["returned"]), "fine": fines.money(loan["fine"]), "fine_paid": bool(loan["fine_paid"]), "renewals": loan["renewals"], "checked_out": loan["checked_out"]}
    if include_current: result["current_fine"] = fines.money(current_fine(loan))
    return result
def list_loans(only_overdue=False): return [loan_json(l, True) for l in loan_repository.list_loans() if not only_overdue or is_overdue(l)]
def get_loan(loan_id):
    loan = loan_repository.get_loan(loan_id)
    if loan is None: raise not_found("loan not found")
    return loan
def create_loan(data):
    if not data.get("book_id") or not data.get("member_id"): raise bad_request("book_id and member_id are required")
    if data.get("due_date") and not validation.is_valid_date(data["due_date"]): raise bad_request("invalid due_date")
    book = book_repository.get_book(data["book_id"])
    if book is None: raise not_found("book not found")
    member = member_repository.get_member(data["member_id"])
    if member is None: raise not_found("member not found")
    if not book["available"]: raise conflict("book is not available")
    loans = loan_repository.list_loans_for_member(member["id"])
    if total_owed(loans) > 0: raise conflict("member has unpaid fines")
    limit = STAFF_LIMIT if member["type"] == "staff" else STUDENT_LIMIT
    if count_open_loans(loans) >= limit: raise conflict("loan limit reached")
    today = date.today()
    due_date = data.get("due_date") or (today + timedelta(days=LOAN_DAYS)).isoformat()
    loan = loan_repository.create_loan(book["id"], member["id"], due_date, today.isoformat())
    notifications.send_email(member["email"], "Book checked out", "You checked out " + book["title"])
    return loan
def return_book(loan_id):
    loan = get_loan(loan_id)
    if loan["returned"]: raise conflict("loan already returned")
    updated = loan_repository.mark_returned(loan_id, loan["book_id"], fines.fine_for(loan["due_date"]))
    member = member_repository.get_member(loan["member_id"])
    book = book_repository.get_book(loan["book_id"])
    notifications.send_email(member["email"], "Book returned", "You returned " + book["title"] + ". Fine: $" + str(fines.money(updated["fine"])))
    return updated
def renew_loan(loan_id):
    loan = get_loan(loan_id)
    if loan["returned"]: raise conflict("loan already returned")
    if date.fromisoformat(loan["due_date"]) < date.today(): raise conflict("overdue loans cannot be renewed")
    if loan["renewals"] >= MAX_RENEWALS: raise conflict("loan was already renewed")
    new_due = (date.fromisoformat(loan["due_date"]) + timedelta(days=LOAN_DAYS)).isoformat()
    updated = loan_repository.extend_loan(loan_id, new_due)
    member = member_repository.get_member(loan["member_id"])
    book = book_repository.get_book(loan["book_id"])
    notifications.send_email(member["email"], "Loan renewed", "You renewed " + book["title"])
    return updated
def pay_fine(loan_id):
    loan = get_loan(loan_id)
    if not loan["returned"]: raise conflict("return the book before paying")
    if loan["fine"] <= 0 or loan["fine_paid"]: raise conflict("no fine to pay")
    updated = loan_repository.mark_fine_paid(loan_id)
    member = member_repository.get_member(loan["member_id"])
    notifications.send_email(member["email"], "Fine paid", "We received $" + str(fines.money(loan["fine"])))
    return updated
