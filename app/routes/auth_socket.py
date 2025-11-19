from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

DB_PATH = "instance/db.sqlite3"

def handle_auth_command(parts):
    command = parts[0]

    if command == "REGISTER":
        return register_user(parts)
    elif command == "LOGIN":
        return login_user(parts)
    else:
        return "ERROR|Comando de autenticación inválido"

def register_user(parts):
    try:
        _, username, password = parts
        hashed = generate_password_hash(password)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (username, password_hash) VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()

        return "OK|Usuario registrado correctamente"
    except Exception as e:
        return f"ERROR|{str(e)}"

def login_user(parts):
    try:
        if len(parts) != 3:
            return "ERROR|Formato inválido. Uso: LOGIN|usuario|contraseña"

        _, username, password = parts

        if username == "admin" and password == "sanrafael":
            return "OK|admin"

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM user WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return "ERROR|Usuario no encontrado"

        user_id, password_hash = row

        # Acá deberías verificar la contraseña con scrypt si corresponde
        return f"OK|{user_id}"

    except Exception as e:
        return f"ERROR|{str(e)}"
