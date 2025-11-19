import sqlite3
from datetime import datetime

DB_PATH = "instance/db.sqlite3"

def handle_appointment_command(parts):
    command = parts[0]

    if command == "CREATE_TURNO":
        return create_turno(parts)
    elif command == "LIST_TURNOS":
        return list_turnos(parts)
    elif command == "LIST_ALL_TURNOS":
        return list_all_turnos()
    elif command == "CANCEL_TURNO":
        return update_estado(parts, "cancelado")
    elif command == "CONFIRM_TURNO":
        return update_estado(parts, "confirmado")
    else:
        return "ERROR|Comando de turnos inválido"
    
def update_estado(parts, nuevo_estado):
    try:
        _, turno_id, solicitante = parts  # solicitante puede ser "admin" o un ID

        if solicitante != "admin":
            return "ERROR|Solo el administrador puede modificar el estado de turnos"

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE turno SET estado = ? WHERE id = ?", (nuevo_estado, turno_id))
        conn.commit()
        conn.close()

        return f"OK|Turno #{turno_id} marcado como {nuevo_estado}"
    except Exception as e:
        return f"ERROR|{str(e)}"

    

def create_turno(parts):
    try:
        _, cliente_id, fecha_str, servicio = parts
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO turno (cliente_id, fecha, servicio, estado)
            VALUES (?, ?, ?, ?)
        """, (cliente_id, fecha.isoformat(), servicio, "pendiente"))
        conn.commit()
        conn.close()

        return "OK|Turno creado correctamente"
    except Exception as e:
        return f"ERROR|{str(e)}"

def list_turnos(parts):
    try:
        _, cliente_id = parts

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, fecha, servicio, estado
            FROM turno
            WHERE cliente_id = ?
            ORDER BY fecha ASC
        """, (cliente_id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "OK|No hay turnos registrados"

        response = "OK"
        for row in rows:
            turno_id, fecha, servicio, estado = row
            response += f"\nTurno #{turno_id} | {fecha} | {servicio} | Estado: {estado}"
        return response
    except Exception as e:
        return f"ERROR|{str(e)}"
    

def list_all_turnos():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, u.username, t.fecha, t.servicio, t.estado
            FROM turno t
            JOIN user u ON t.cliente_id = u.id
            ORDER BY t.fecha ASC
        """)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "OK|No hay turnos registrados"

        response = "OK"
        for row in rows:
            turno_id, username, fecha, servicio, estado = row
            response += f"\nTurno #{turno_id} | {fecha} | {servicio} | Cliente: {username} | Estado: {estado}"
        return response
    except Exception as e:
        return f"ERROR|{str(e)}"