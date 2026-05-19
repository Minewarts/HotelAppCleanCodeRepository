# HOTTEL
## SISTEMA DE GESTIÓN DE RESERVAS 

---

### Integrantes
- Sanet Correa Castaño
- Cristian Escobar Taborda
- Nicolas Peña Ibarguen

---

### Descripción
Aplicación desarrollada como entregable para el proyecto de **Código Limpio**. El proyecto ha sido desarrollado bajo los estándares de **Clean Code** y **Arquitectura de Capas**, priorizando la legibilidad, el desacoplamiento de componentes y la facilidad de mantenimiento.

---

### Objetivos
Implementar las buenas prácticas y conocimientos vistos a lo largo de las clases de código limpio, mejorando la legibilidad, el mantenimiento y la presentación del código para crear un producto profesional orientado al entorno laboral.

---

### Requisitos

- Python 3.12+
- Cuenta en [Supabase](https://supabase.com)

---

### Instalación y ejecución

**1. Clona el repositorio**
```bash
git clone https://github.com/Minewarts/HotelAppCleanCodeRepository.git
cd HotelAppCleanCodeRepository
```

**2. Instala las dependencias**
```bash
pip install -e .
```

**3. Configura las variables de entorno**
```bash
cp .env.example .env
```
Abre el archivo `.env` y rellena tus credenciales de Supabase:
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
USE_SUPABASE=true
```
> Encuéntralas en tu proyecto de Supabase → **Settings → API**

**4. Inicia la API**
```bash
uvicorn src.HotelApp.api.main:app --reload
```

**5. Accede a la documentación**

| Interfaz | URL |
|---|---|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

### Endpoints disponibles

| Entidad | Método | Ruta |
|---|---|---|
| Usuarios | GET | `/users/` |
| Usuarios | POST | `/users/` |
| Usuarios | PATCH | `/users/{id}` |
| Usuarios | DELETE | `/users/{id}` |
| Habitaciones | GET | `/rooms/` |
| Habitaciones | POST | `/rooms/` |
| Habitaciones | PATCH | `/rooms/{id}` |
| Habitaciones | DELETE | `/rooms/{id}` |
| Historial | GET | `/user-history/{user_id}` |
| Historial | POST | `/user-history/` |
| Historial | DELETE | `/user-history/{id}` |
| Hotel | GET | `/hotel/` |
| Hotel | PUT | `/hotel/` |

---

### Funciones

#### 1. Gestión de Huéspedes
* **Registro de Usuarios:** Alta de nuevos clientes.
* **Consulta de Perfiles:** Visualización de información.
* **Bajas de Usuario:** Gestión de retiro de usuarios.

#### 2. Gestión de Habitaciones
* **Control de Disponibilidad:** Monitoreo en tiempo real.
* **Búsqueda Especializada:** Filtros avanzados.

#### 3. Sistema de Reservas
* **Creación de Reservas:** Flujo de registro de estancia.
* **Cancelación de Reservas:** Gestión de anulaciones.
* **Historial de Estancia:** Registro detallado de visitas.

---