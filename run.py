import socket
import threading
from app.routes.auth_socket import handle_auth_command
from app.routes.appointments import handle_appointment_command

HOST = "localhost"
PORT = 5000

def handle_client(conn, addr):
    print(f"\n[Conexión] Cliente conectado desde {addr}")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            print(f"[Recibido] {data}")
            command_parts = data.strip().split("|")
            command = command_parts[0]

            if command in ["REGISTER", "LOGIN"]:
                response = handle_auth_command(command_parts)
            elif command in [
                "CREATE_TURNO", "LIST_TURNOS", "LIST_ALL_TURNOS",
                "CANCEL_TURNO", "CONFIRM_TURNO"
            ]:
                response = handle_appointment_command(command_parts)
            else:
                response = "ERROR|Comando no reconocido"

            conn.send(response.encode())

        except Exception as e:
            print(f"[Error] {e}")
            try:
                conn.send(f"ERROR|{str(e)}".encode())
            except:
                pass
            break

    conn.close()
    print(f"[Desconexión] Cliente {addr} desconectado")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # evita WinError 10048
    server.bind((HOST, PORT))
    server.listen()
    print(f"[Servidor] Escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()