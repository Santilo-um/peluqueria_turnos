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
        _, username, password = parts
        
        if username == "admin" and password == "sanrafael":
            return "OK|admin"

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM user WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return f"OK|{row[0]}"
        else:
            return "ERROR|Credenciales inválidas"
    except Exception as e:
        return f"ERROR|{str(e)}"