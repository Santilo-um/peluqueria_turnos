from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import db, Turno, User
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

# Crear turno (solo cliente)
@appointments_bp.route('/turnos', methods=['POST'])
@jwt_required()
def crear_turno():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != 'cliente':
        return jsonify({'msg': 'Solo clientes pueden crear turnos'}), 403

    data = request.json
    try:
        fecha = datetime.fromisoformat(data['fecha'])
    except ValueError:
        return jsonify({'msg': 'Formato de fecha inválido'}), 400

    nuevo_turno = Turno(
        cliente_id=user.id,
        fecha=fecha,
        servicio=data['servicio']
    )
    db.session.add(nuevo_turno)
    db.session.commit()
    return jsonify({'msg': 'Turno creado', 'turno_id': nuevo_turno.id}), 201

# Ver turnos (cliente ve los suyos, peluquero/admin ve todos)
@appointments_bp.route('/turnos', methods=['GET'])
@jwt_required()
def ver_turnos():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role in ['admin', 'peluquero']:
        turnos = Turno.query.all()
    else:
        turnos = Turno.query.filter_by(cliente_id=user.id).all()

    return jsonify([
        {
            'id': t.id,
            'fecha': t.fecha.isoformat(),
            'servicio': t.servicio,
            'estado': t.estado,
            'cliente': t.cliente.username
        } for t in turnos
    ])

# Modificar estado del turno (solo peluquero/admin)
@appointments_bp.route('/turnos/<int:turno_id>', methods=['PUT'])
@jwt_required()
def modificar_turno(turno_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role not in ['admin', 'peluquero']:
        return jsonify({'msg': 'No autorizado'}), 403

    turno = Turno.query.get_or_404(turno_id)
    data = request.json
    nuevo_estado = data.get('estado')

    if nuevo_estado not in ['pendiente', 'confirmado', 'cancelado']:
        return jsonify({'msg': 'Estado inválido'}), 400

    turno.estado = nuevo_estado
    db.session.commit()
    return jsonify({'msg': 'Turno actualizado'})