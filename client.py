import socket

HOST = "localhost"
PORT = 5000

while True:
    comando = input(">> ")
    if comando.lower() in ["exit", "salir"]:
        break

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(comando.encode())
        respuesta = s.recv(1024).decode()
        print(f"[Servidor] {respuesta}")