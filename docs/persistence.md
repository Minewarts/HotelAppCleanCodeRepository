# 💾 Capa de Persistencia

En este proyecto, la persistencia se encarga de que los datos de tu hotel (habitaciones y reservas) no se borren al cerrar la terminal.

## 📂 Archivo de Almacenamiento (JSON)
La aplicación utiliza un archivo de texto en formato **JSON** (generalmente llamado `hotel_data.json`). Elegimos este formato porque es ligero, fácil de leer y permite ver los datos guardados sin necesidad de herramientas complejas.

### Estructura de los Datos
Los modelos de Python se guardan siguiendo una estructura de objetos. Así es como se ve el archivo por dentro:

```json
{
  "rooms": [
    {
      "number": 101,
      "type": "Suite",
      "price": 150.0,
      "is_available": true
    }
  ],
  "bookings": [
    {
      "id": "res-001",
      "room_number": 101,
      "guest_name": "Juan Perez"
    }
  ]
}