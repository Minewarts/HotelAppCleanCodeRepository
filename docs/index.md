# Bienvenido a HotelApp - Clean Code

Esta es la documentación oficial de la aplicación de gestión hotelera, diseñada bajo los principios de **Clean Architecture** (Arquitectura Limpia) y desarrollada íntegramente en Python.

## 🏨 Sobre el Proyecto
El objetivo principal es ofrecer un sistema robusto para la gestión de habitaciones y reservas, manteniendo una separación clara entre la lógica de negocio y los detalles de implementación (como la persistencia o la interfaz de usuario).

## 🧩 Estructura de Capas
El proyecto se organiza siguiendo el esquema de cebolla:

1. **Entities (Entidades):** Reglas de negocio globales (Habitaciones, Huéspedes).
2. **Use Cases (Casos de Uso):** Reglas específicas de la aplicación (Realizar Reserva, Cancelar Reserva).
3. **Interface Adapters:** Controladores y presentadores que convierten datos.
4. **Frameworks & Drivers:** Herramientas externas como la base de datos o la CLI.

## 🛠️ Tecnologías Principales
* **Python 3.10+**
* **MkDocs** (Documentación)
* **Pytest** (Pruebas unitarias)