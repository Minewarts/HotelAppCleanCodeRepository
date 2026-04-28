# API Reference

## Services

### UserServices
Servicio de gestión de usuarios del sistema.

**Métodos principales:**
- `create_user(user: User)` - Crea un nuevo usuario
- `get_user(user_id: int)` - Obtiene un usuario por ID
- `delete_user(user_id: int)` - Elimina un usuario del sistema

### HotelService
Servicio de gestión de reservas y habitaciones.

**Métodos principales:**
- `reserve_room(user: User, room: Room)` - Realiza una reserva
- `cancel_reservation(user: User, room: Room)` - Cancela una reserva

## Models

### User
Representa un huésped del hotel.

**Atributos:**
- `id: int` - Identificador único
- `name: str` - Nombre del huésped
- `email: str` - Correo electrónico
- `history: List[UserHistory]` - Historial de reservas

### Room
Representa una habitación del hotel.

**Atributos:**
- `room_number: int` - Número de habitación
- `room_type: str` - Tipo de habitación (Sencilla, Doble, Suite, etc.)
- `status: str` - Estado (available/occupied)

### UserHistory
Registro de una estancia del huésped.

**Atributos:**
- `user: User` - Usuario asociado
- `room: Room` - Habitación ocupada
- `check_in: datetime` - Fecha/hora de entrada
- `check_out: Optional[datetime]` - Fecha/hora de salida

### Hotel
Entidad central que gestiona habitaciones y huéspedes.

**Atributos:**
- `name: str` - Nombre del hotel
- `stars: Optional[int]` - Calificación de estrellas
- `rooms: List[Room]` - Habitaciones disponibles
- `clients: List[User]` - Huéspedes registrados