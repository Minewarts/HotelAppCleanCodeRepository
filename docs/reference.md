# 📖 Referencia Técnica

## Estructura de Carpetas

```
src/HotelApp/
├── __init__.py
├── api/               # FastAPI app and routers
├── app/               # CLI application (Typer)
├── exceptions.py      # Excepciones personalizadas
├── models.py          # Entidades del dominio (User, Room, Hotel, ...)
├── services.py        # Lógica de aplicación (UserService, HotelService)
└── storage/           # Persistencia de datos
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
user.get_id()      -> int
user.get_name()    -> str
user.get_email()   -> str
```

### Room
```python
from src.HotelApp.models import Room

# Creación
room = Room(room_number=101, room_type="Suite")

# Getters
room.get_room_number()  -> int
room.get_room_type()    -> str
room.get_status()       -> str
room.set_status(status: str) -> None
```

### UserHistory
En esta implementación el historial se maneja como registros asociados a usuarios; ver `src/HotelApp/schemas` y `api/routers/user_history.py` para los modelos y endpoints.

### Hotel
```python
from src.HotelApp.models import Hotel

# Creación
hotel = Hotel(name="Gran Hotel", stars=5)

# Métodos
hotel.add_room(room: Room) -> None
hotel.add_client(user: User) -> None
hotel.get_room_by_number(num: int) -> Optional[Room]
hotel.get_client_by_id(id: int) -> Optional[User]
```

## Servicios

### `UserService`
```python
from src.HotelApp.services import UserService
from src.HotelApp.storage import JSONStorage
from pathlib import Path

storage = JSONStorage(Path("data/database.json"))
service = UserService(storage)

# Métodos
service.create_user(user_or_id, name=None, email=None) -> None
service.get_user(user_id: int) -> User
service.get_user_by_id(user_id) -> User
```

### HotelService
```python
from src.HotelApp.services import HotelService

# Métodos
service.reserve_room(user: User, room: Room) -> None
service.cancel_reservation(user: User, room: Room) -> None
service.add_room(room_number, room_type) -> None
service.get_room(room_number) -> Room | None
service.book_room(room_number) -> Room
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