# 🚀 Guía de Inicio Rápido

Sigue estos pasos para configurar el proyecto y ejecutar la aplicación.

## 📋 Requisitos Previos

Asegúrate de tener instalado:
- **Python 3.10+**
- **Git**
- **pip** (gestor de paquetes de Python)

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Minewarts/HotelAppCleanCodeRepository.git
cd HotelAppCleanCodeRepository
```

### 2. Crear un entorno virtual

```bash
# En Windows:
python -m venv venv
.\venv\Scripts\activate

# En Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🎮 Primeros Pasos

### Ver comandos disponibles

```bash
python main.py --help
```

### Crear un usuario

```bash
python main.py create-user --id 1 --name "Juan Pérez" --email "juan@example.com"
```

### Listar usuarios

```bash
python main.py list-users
```

### Realizar una reserva

```bash
python main.py book --user-id 1 --room-number 101 --room-type "Suite"
```

## 🧪 Ejecutar Tests

```bash
pytest tests/
```

## 📖 Documentación

- [Comandos disponibles](commands.md)
- [API Reference](api.md)
- [Arquitectura](architecture.md)
- [Persistencia de Datos](persistence.md)

## 🐛 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'HotelApp'`
**Solución:** Asegúrate de estar en la carpeta raíz del proyecto y que el entorno virtual esté activado.

### Error: `No such file or directory: 'data/database.json'`
**Solución:** Crea la carpeta `data/`:
```bash
mkdir data
```

## ✅ Verificación de Instalación

Para verificar que todo está correctamente instalado:

```bash
python -c "from src.HotelApp.models import User; print('✓ Importación exitosa')"
```