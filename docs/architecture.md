# 🏗️ Arquitectura del Proyecto

## Visión General

HotelApp sigue los principios de **Clean Architecture** (Arquitectura Limpia), lo que permite:
- ✅ Independencia de frameworks
- ✅ Fácil testabilidad
- ✅ Mantenibilidad a largo plazo
- ✅ Separación clara de responsabilidades

## Estructura en Capas

```
┌─────────────────────────────────────────┐
│   Frameworks & Drivers (CLI, DB)        │
├─────────────────────────────────────────┤
│   Interface Adapters (Controllers)      │
├─────────────────────────────────────────┤
│   Application Business Rules (Services) │
├─────────────────────────────────────────┤
│   Enterprise Business Rules (Models)    │
└─────────────────────────────────────────┘
```

### 1. Entities / Models (`src/HotelApp/models/`)

La capa más interna contiene los modelos de dominio que representan las reglas de negocio fundamentales:

- **`User.py`** - Representa un huésped del hotel
  - Valida IDs positivos
  - Valida formato de email
  - Mantiene historial de estancias

- **`Room.py`** - Representa una habitación
  - Valida número de habitación positivo
  - Gestiona estados (available/occupied)
  - Define tipos de habitación

- **`Hotel.py`** - Entidad central del sistema
  - Gestiona colecciones de habitaciones
  - Gestiona colecciones de huéspedes
  - Busca habitaciones y huéspedes por ID

- **`UserHistory.py`** - Registro de estancias
  - Vincula usuarios con habitaciones
  - Registra check-in y check-out
  - Valida transiciones de estado

### 2. Use Cases / Services (`src/HotelApp/services/`)

Define los casos de uso de la aplicación:

- **`UserServices.py`** - Lógica de gestión de usuarios
  - Crear usuarios con validación
  - Recuperar usuarios
  - Gestionar iteraciones de usuario

- **`HotelService.py`** - Lógica de reservas
  - Reservar habitaciones
  - Cancelar reservas
  - Validar disponibilidad

### 3. Interface Adapters (`src/HotelApp/storage/`)

Convierte datos entre formatos:

- **`JSONStorage.py`** - Persistencia en JSON
  - Carga y guarda datos
  - Serializa objetos a JSON
  - Implementa el protocol StorageProtocol

- **`StorageProtocol.py`** - Define interfaz de almacenamiento
  - Abstracción para diferentes backends
  - Facilita testing con mocks

### 4. Exceptions (`src/HotelApp/exceptions/`)

Excepciones personalizadas del dominio:

- **`AppError.py`** - Excepción base
- **`InvalidUserDataError.py`** - Datos de usuario inválidos
- **`UserAlreadyExistsError.py`** - Usuario duplicado
- **`UserNotFoundError.py`** - Usuario no encontrado
- **`UserError.py`** - Errores generales de usuario

### 5. Frameworks & Drivers

#### CLI (`main.py`)
- Implementa interfaz de línea de comandos con Typer
- Comandos: crear usuario, listar usuarios, reservar, cancelar

#### Storage Layer
- Actualmente: JSON (dev/testing)
- Preparado para: Supabase, PostgreSQL, etc.

## Diagrama de Dependencias

```
main.py (CLI)
    ↓
Services (UserServices, HotelService)
    ↓
Models (User, Room, Hotel, UserHistory)
    ↓
Exceptions
```

**Nota:** Las dependencias apuntan hacia adentro. Las capas externas dependen de las internas, nunca al revés.

## Patrones Utilizados

### 1. **Protocol Pattern** (Storage)
Define contratos sin herencia rígida.
```python
class StorageProtocol(Protocol):
    def load(self) -> List[User]: ...
    def save(self, users: List[User]) -> None: ...
```

### 2. **Repository Pattern** (Services)
Abstrae el acceso a datos.
```python
class UserServices:
    def __init__(self, storage: StorageProtocol):
        self.storage = storage
```

### 3. **Value Object Pattern** (Models)
Encapsula validaciones en el modelo.
```python
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self._validate_id(user_id)
        self._validate_email(email)
```

## Testing

Gracias a la arquitectura limpia:

```python
# Tests pueden usar mocks de Storage
class MockStorage(StorageProtocol):
    def load(self): return []
    
# Tests de servicios no conocen JSON o Supabase
service = UserServices(MockStorage())
```

## Ventajas

| Aspecto | Beneficio |
|--------|-----------|
| Independencia de BD | Cambiar de JSON a Supabase sin afectar lógica |
| Testabilidad | 100% de código con tests unitarios |
| Claridad | Responsabilidades bien definidas |
| Escalabilidad | Fácil agregar nuevas features |
| Mantenibilidad | Código autodocumentado |
