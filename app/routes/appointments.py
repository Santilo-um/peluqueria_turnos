import sqlite3
from datetime import datetime

DB_PATH = "instance/db.sqlite3"

def handle_appointment_command(parts):
    command = parts[0]

    if command == "CREATE_TURNO":
        return create_turno(parts)
    elif command == "LIST_TURNOS":
        return list_turnos(parts)
    else:
        return "ERROR|Comando de turnos inválido"

def create_turno(parts):
    try:
        _, cliente_id, fecha_str, servicio = parts
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO turno (cliente_id, fecha, servicio)
            VALUES (?, ?, ?)
        """, (cliente_id, fecha.isoformat(), servicio))
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
            response += f"|{row[0]}:{row[1]}:{row[2]}:{row[3]}"
        return response
    except Exception as e:
        return f"ERROR|{str(e)}"