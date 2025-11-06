from flask import Blueprint, jsonify

appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Appointments funcionando"})