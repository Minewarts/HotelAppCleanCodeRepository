# 📖 Referencia Técnica

## Estructura de Carpetas

```
src/HotelApp/
├── __init__.py
├── exceptions/        # Excepciones personalizadas
├── models/           # Entidades del dominio
│   ├── __init__.py
│   ├── hotel.py
│   ├── room.py
│   ├── user.py
│   └── user_history.py
├── services/         # Lógica de aplicación
│   ├── __init__.py
│   ├── hotel_service.py
│   └── user_services.py
└── storage/          # Persistencia de datos
    ├── __init__.py
    ├── json_storage.py
    └── storage_protocol.py
```

## Modelos del Dominio

### User
```python
from src.HotelApp.models import User

# Creación
user = User(user_id=1, name="Juan", email="juan@example.com")

# Getters
user.get_id()      → int
user.get_name()    → str
user.get_email()   → str
```

### Room
```python
from src.HotelApp.models import Room

# Creación
room = Room(room_number=101, room_type="Suite")

# Getters
room.get_room_number()  → int
room.get_room_type()    → str
room.get_status()       → str
room.set_status(status: str) → None
```

### UserHistory
```python
from src.HotelApp.models import UserHistory
from datetime import datetime

# Creación
history = UserHistory(user, room)

# Métodos
history.get_user()         → User
history.get_room()         → Room
history.get_check_in()     → datetime
history.get_check_out()    → Optional[datetime]
history.is_active()        → bool
history.check_out()        → None
```

### Hotel
```python
from src.HotelApp.models import Hotel

# Creación
hotel = Hotel(name="Gran Hotel", stars=5)

# Métodos
hotel.add_room(room: Room) → None
hotel.add_client(user: User) → None
hotel.get_room_by_number(num: int) → Optional[Room]
hotel.get_client_by_id(id: int) → Optional[User]
```

## Servicios

### UserServices
```python
from src.HotelApp.services import UserServices
from src.HotelApp.storage import JSONStorage
from pathlib import Path

storage = JSONStorage(Path("data/database.json"))
service = UserServices(storage)

# Métodos
service.create_user(user: User) → None
service.get_user(user_id: int) → User
```

### HotelService
```python
from src.HotelApp.services import HotelService

# Métodos
service.reserve_room(user: User, room: Room) → None
service.cancel_reservation(user: User, room: Room) → None
```

## Excepciones

```python
from src.HotelApp.exceptions import (
    AppError,
    InvalidUserDataError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserError
)

try:
    user = User(-1, "Juan", "juan@example.com")
except InvalidUserDataError as e:
    print(f"Error: {e}")
```

## Almacenamiento

### JSONStorage
```python
from src.HotelApp.storage import JSONStorage
from pathlib import Path

# Inicializar
storage = JSONStorage(Path("data/database.json"))

# Cargar datos
users = storage.load()  → List[User]

# Guardar datos
storage.save(users)     → None
```

## Ejemplo Completo: Crear Usuario y Reservar

```python
from src.HotelApp.models import User, Room
from src.HotelApp.services import UserServices, HotelService
from src.HotelApp.storage import JSONStorage
from pathlib import Path

# Inicializar
storage = JSONStorage(Path("data/database.json"))
user_service = UserServices(storage)
hotel_service = HotelService(storage)

# Crear usuario
user = User(user_id=1, name="Juan", email="juan@example.com")
user_service.create_user(user)

# Crear habitación
room = Room(room_number=101, room_type="Suite")

# Reservar
hotel_service.reserve_room(user, room)
```