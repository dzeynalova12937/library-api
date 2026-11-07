import book_repository, loan_repository, loan_service, report_repository, fines

def overdue_report():
    items = []
    for row in report_repository.list_open_loans_with_details():
        late = fines.days_late(row["due_date"])
        if late > 0:
            items.append({"loan_id": row["id"], "title": row["title"], "member": row["name"], "days_late": late, "fine": fines.money(fines.fine_for(row["due_date"]))})
    return {"items": items, "total_fines": fines.money(sum(i["fine"] for i in items))}
def summary_report():
    loans = loan_repository.list_loans()
    return {"total_books": book_repository.count_books(), "on_loan": loan_service.count_open_loans(loans), "fines_outstanding": fines.money(loan_service.total_owed(loans))}
