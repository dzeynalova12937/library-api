import member_repository as repo
import loan_repository, loan_service, validation, fines
from errors import bad_request, conflict, not_found

def list_members(): return repo.list_members()
def get_member(member_id):
    member = repo.get_member(member_id)
    if member is None: raise not_found("member not found")
    return member
def create_member(data):
    if not data.get("name"): raise bad_request("name is required")
    if not validation.is_valid_email(data.get("email")): raise bad_request("invalid email")
    member_type = data.get("type", "student")
    if not validation.is_valid_member_type(member_type): raise bad_request("type must be student or staff")
    if repo.get_member_by_email(data["email"]) is not None: raise conflict("email already registered")
    return repo.create_member(data["name"], data["email"], member_type)
def member_account(member_id):
    member = get_member(member_id)
    loans = loan_repository.list_loans_for_member(member_id)
    items = [{"id": l["id"], "book_id": l["book_id"], "due_date": l["due_date"], "returned": bool(l["returned"]), "fine": fines.money(l["fine"]), "fine_paid": bool(l["fine_paid"])} for l in loans]
    limit = loan_service.STAFF_LIMIT if member["type"] == "staff" else loan_service.STUDENT_LIMIT
    return {"loans": items, "total_owed": fines.money(loan_service.total_owed(loans)), "loans_remaining": limit - loan_service.count_open_loans(loans)}
