from flask import Blueprint, jsonify, request
import loan_service
bp = Blueprint("loans", __name__)
@bp.route("/loans", methods=["GET"])
def list_loans(): return jsonify(loan_service.list_loans(request.args.get("overdue") == "true"))
@bp.route("/loans/<int:loan_id>", methods=["GET"])
def get_loan(loan_id): return jsonify(loan_service.loan_json(loan_service.get_loan(loan_id), True))
@bp.route("/loans", methods=["POST"])
def create_loan(): return jsonify(loan_service.loan_json(loan_service.create_loan(request.get_json(silent=True) or {}))), 201
@bp.route("/loans/<int:loan_id>/return", methods=["POST"])
def return_book(loan_id): return jsonify(loan_service.loan_json(loan_service.return_book(loan_id)))
@bp.route("/loans/<int:loan_id>/renew", methods=["POST"])
def renew_loan(loan_id): return jsonify(loan_service.loan_json(loan_service.renew_loan(loan_id)))
@bp.route("/loans/<int:loan_id>/pay-fine", methods=["POST"])
def pay_fine(loan_id): return jsonify(loan_service.loan_json(loan_service.pay_fine(loan_id)))
