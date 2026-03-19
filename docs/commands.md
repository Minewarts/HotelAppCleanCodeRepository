
# 💻 Guía de Comandos (CLI)

La interfaz de línea de comandos permite gestionar el hotel de forma rápida.

## 🛠️ Ejemplos de Uso

### Registrar una Habitación

**Para añadir una habitación al sistema:**

uv run main.py add-room --number 101 --type "Suite" --price 150.0

**Listar habitaciones disponibles :**

uv run main.py list-rooms --status available

**Crear una Reserva:**

uv run main.py create-booking --room 101 --guest "Juan Perez"