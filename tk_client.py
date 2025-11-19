import tkinter as tk
from tkinter import messagebox
import socket

HOST = "localhost"
PORT = 5000

cliente_id = None  # se guarda después del login

def enviar_comando(comando):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(comando.encode())
            return s.recv(2048).decode()
    except Exception as e:
        return f"ERROR|{str(e)}"

def login():
    global cliente_id
    user = entry_user.get()
    password = entry_pass.get()
    respuesta = enviar_comando(f"LOGIN|{user}|{password}")
    if respuesta.startswith("OK"):
        cliente_id = respuesta.split("|")[1]
        if cliente_id == "admin":
            mostrar_panel_admin()
        else:
            messagebox.showinfo("Login exitoso", f"Bienvenido {user}")
            mostrar_menu_principal()
    else:
        messagebox.showerror("Error", respuesta)

def registrar():
    user = entry_user.get()
    password = entry_pass.get()
    respuesta = enviar_comando(f"REGISTER|{user}|{password}")
    if respuesta.startswith("OK"):
        messagebox.showinfo("Registro exitoso", "Ahora podés iniciar sesión")
    else:
        messagebox.showerror("Error", respuesta)

def crear_turno():
    fecha = entry_fecha.get()
    servicio = entry_servicio.get()
    if not fecha or not servicio:
        messagebox.showerror("Error", "Completá todos los campos")
        return
    comando = f"CREATE_TURNO|{cliente_id}|{fecha}|{servicio}"
    respuesta = enviar_comando(comando)
    messagebox.showinfo("Respuesta", respuesta)

def ver_turnos():
    respuesta = enviar_comando(f"LIST_TURNOS|{cliente_id}")
    messagebox.showinfo("Tus turnos", respuesta)

def mostrar_menu_principal():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="📅 Crear nuevo turno").pack()
    tk.Label(root, text="Fecha (YYYY-MM-DD HH:MM)").pack()
    global entry_fecha
    entry_fecha = tk.Entry(root)
    entry_fecha.pack()

    tk.Label(root, text="Servicio").pack()
    global entry_servicio
    entry_servicio = tk.Entry(root)
    entry_servicio.pack()

    tk.Button(root, text="Crear turno", command=crear_turno).pack(pady=5)
    tk.Button(root, text="Ver mis turnos", command=ver_turnos).pack(pady=5)
    
def mostrar_panel_admin():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="🔧 Panel del administrador").pack()

    respuesta = enviar_comando("LIST_ALL_TURNOS")
    if not respuesta.startswith("OK"):
        messagebox.showerror("Error", respuesta)
        return

    turnos = respuesta.split("\n")[1:]  # salteamos el "OK"
    for turno in turnos:
        frame = tk.Frame(root)
        frame.pack(pady=2, fill="x")

        tk.Label(frame, text=turno, anchor="w").pack(side="left", expand=True)

        turno_id = turno.split("#")[1].split(" ")[0]

        btn_confirmar = tk.Button(frame, text="✅", command=lambda tid=turno_id: actualizar_estado(tid, "CONFIRM_TURNO"))
        btn_confirmar.pack(side="right")

        btn_cancelar = tk.Button(frame, text="❌", command=lambda tid=turno_id: actualizar_estado(tid, "CANCEL_TURNO"))
        btn_cancelar.pack(side="right")

def actualizar_estado(turno_id, accion):
    comando = f"{accion}|{turno_id}|admin"
    respuesta = enviar_comando(comando)
    messagebox.showinfo("Estado actualizado", respuesta)
    mostrar_panel_admin()  # refresca la lista

def mostrar_login():
    tk.Label(root, text="👤 Usuario").pack()
    global entry_user
    entry_user = tk.Entry(root)
    entry_user.pack()

    tk.Label(root, text="🔒 Contraseña").pack()
    global entry_pass
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    tk.Button(root, text="Iniciar sesión", command=login).pack(pady=5)
    tk.Button(root, text="Registrarse", command=registrar).pack(pady=5)

# 🪟 Inicio
root = tk.Tk()
root.title("Peluquería - Sistema de turnos")
root.geometry("300x300")
mostrar_login()
root.mainloop()