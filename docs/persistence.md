# 💾 Capa de Persistencia

En este proyecto, la persistencia se encarga de que los datos de tu hotel (habitaciones y reservas) no se borren al cerrar la terminal.

## 📂 Archivo de Almacenamiento (JSON)
La aplicación utiliza un archivo JSON por defecto en `data/database.json`, gestionado por la clase `JSONStorage` en `src/HotelApp/storage.py`.

### Estructura de los Datos
Internamente `JSONStorage` serializa una lista de usuarios. Cada usuario tiene la forma:

```json
[
  {
    "id": 1,
    "name": "Juan Perez",
    "email": "juan@example.com",
    "history": [
      {
        "room_number": 101,
        "room_type": "Suite",
        "status": "occupied"
      }
    ]
  }
]
```

Si necesitas un esquema distinto para integraciones, implementa un adaptador en la capa `storage`.
