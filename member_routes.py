from flask import Blueprint, jsonify, request
import member_service
bp = Blueprint("members", __name__)
def member_json(m): return {"id": m["id"], "name": m["name"], "email": m["email"], "type": m["type"]}
@bp.route("/members", methods=["GET"])
def list_members(): return jsonify([member_json(m) for m in member_service.list_members()])
@bp.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id): return jsonify(member_json(member_service.get_member(member_id)))
@bp.route("/members", methods=["POST"])
def create_member(): return jsonify(member_json(member_service.create_member(request.get_json(silent=True) or {}))), 201
@bp.route("/members/<int:member_id>/loans", methods=["GET"])
def member_loans(member_id): return jsonify(member_service.member_account(member_id))
