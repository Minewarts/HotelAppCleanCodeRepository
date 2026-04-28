# 💻 Guía de Comandos (CLI)

La interfaz de línea de comandos permite gestionar el hotel de forma rápida y eficiente.

## Comandos de Usuarios

### Crear un nuevo usuario

Registra un nuevo huésped en el sistema.

```bash
python main.py create-user --id 1 --name "Juan Pérez" --email "juan@example.com"
```

**Parámetros:**
- `--id` (int): Identificador único del usuario
- `--name` (str): Nombre del huésped
- `--email` (str): Correo electrónico válido

**Ejemplo exitoso:**
```
✓ Usuario Juan Pérez creado con éxito.
```

### Listar todos los usuarios

Muestra una tabla con todos los huéspedes registrados.

```bash
python main.py list-users
```

**Salida esperada:**
```
┏━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ ID  ┃ Nombre      ┃ Email             ┃
┡━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ 1   │ Juan Pérez  │ juan@example.com  │
└─────┴─────────────┴───────────────────┘
```

## Comandos de Reservas

### Reservar una habitación

Crea una reserva de una habitación para un usuario.

```bash
python main.py book --user-id 1 --room-number 101 --room-type "Suite"
```

**Parámetros:**
- `--user-id` (int): ID del usuario que realiza la reserva
- `--room-number` (int): Número de la habitación
- `--room-type` (str): Tipo de habitación (Sencilla, Doble, Suite, Estándar)

**Ejemplo exitoso:**
```
✓ Habitación 101 reservada para Juan Pérez.
```

### Cancelar una reserva

Cancela una reserva existente de un usuario.

```bash
python main.py cancel --user-id 1 --room-number 101
```

**Parámetros:**
- `--user-id` (int): ID del usuario
- `--room-number` (int): Número de la habitación a liberar

**Ejemplo exitoso:**
```
✓ Reserva de la habitación 101 cancelada.
```

## Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| User id must be positive | ID negativo o cero | Usa un ID positivo |
| Invalid Email | Email sin @ | Proporciona un email válido |
| Room number must be positive | Número de sala inválido | Usa un número positivo |
| Room already exists | Habitación duplicada | Usa otro número de habitación |