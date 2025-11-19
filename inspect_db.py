import sqlite3

DB_PATH = "instance/db.sqlite3"

def mostrar_usuarios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, created_at FROM user")
    rows = cursor.fetchall()
    conn.close()

    print("\n📋 Usuarios registrados:")
    for row in rows:
        print(f"  ID: {row[0]} | Usuario: {row[1]} | Rol: {row[2]} | Creado: {row[3]}")

def mostrar_turnos():
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

    print("\n📅 Turnos registrados:")
    for row in rows:
        print(f"  Turno #{row[0]} | Cliente: {row[1]} | Fecha: {row[2]} | Servicio: {row[3]} | Estado: {row[4]}")

if __name__ == "__main__":
    print("🔍 Explorando base de datos SQLite...")
    mostrar_usuarios()
    mostrar_turnos()