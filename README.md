💇‍♂️ PELUQUERIA_TURNOS
Sistema de gestión de turnos para peluquería, desarrollado en Python con arquitectura modular, comunicación por sockets, y cliente gráfico en Tkinter. Permite a usuarios registrarse, iniciar sesión, solicitar turnos y visualizar su estado, mientras que el administrador puede confirmar o cancelar solicitudes.

🚀 Características principales
- Registro y login de usuarios con hash seguro (Scrypt)
- Asignación de turnos con fecha, hora y servicio
- Panel de administración para confirmar/cancelar turnos
- Cliente gráfico en Tkinter para usuarios finales
- Comunicación cliente-servidor vía sockets
- Persistencia con SQLite y migraciones
- Dockerización completa para despliegue rápido

🧱 Estructura del proyecto
PELUQUERIA_TURNOS/
├── app/
│   ├── models/
│   │   └── models_socket.py
│   ├── routes/
│   │   ├── appointments.py
│   │   ├── auth_socket.py
│   │   ├── root.py
│   │   └── socket.py
│   ├── utils/
│   │   └── jwt_service.py
├── instance/
│   └── db.sqlite3
├── migrations/
├── run.py              # Servidor principal
├── tk_client.py        # Cliente gráfico en Tkinter
├── inspect_db.py       # Herramienta para inspeccionar la base
├── config.py           # Configuración general
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

🔧 Instalación y ejecución
1. Clonar el repositorio
git clone https://github.com/tu_usuario/PELUQUERIA_TURNOS.git
cd PELUQUERIA_TURNOS

2. Construir y levantar con Docker
docker-compose up --build

3. Ejecutar el cliente Tkinter
python tk_client.py

🧪 Comandos por consola (modo texto)
- Registrar usuario: REGISTER|username|password
- Iniciar sesión: LOGIN|username|password
- Solicitar turno: CREATE_TURNO|id|time|service

🛠 Tecnologías utilizadas
• 	Python 3.11
• 	Tkinter
• 	SQLite
• 	Sockets TCP
• 	Docker & Docker Compose
• 	SQLAlchemy (opcional)
• 	Scrypt (hash seguro)

📌 TODOs y mejoras futuras
• 	Exportar turnos a CSV
• 	Notificaciones por email
• 	Interfaz web con Flask o React
• 	Confirmación visual y filtros por estado
• 	Multiusuario con roles extendidos