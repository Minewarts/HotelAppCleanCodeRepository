from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from src.HotelApp.exceptions import AppError
from src.HotelApp.models import User, Room
from src.HotelApp.services import UserService, HotelService
from src.HotelApp.storage import JSONStorage

app = typer.Typer(help="HOT TEL - Sistema de Gestión de Reservas CLI")
console = Console()

# Inicialización
storage = JSONStorage(Path("data/database.json"))
user_service = UserService(storage)
hotel_service = HotelService(storage)


# ---------------- USER COMMANDS ----------------

@app.command(name="create-user")
def create_user(id: int, name: str, email: str):
    """Crea un nuevo usuario."""
    try:
        user = User(user_id=id, name=name, email=email)
        user_service.create_user(user)
        console.print(f"[green]✓ Usuario {name} creado con éxito.[/green]")
    except AppError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command(name="list-users")
def list_users():
    """Lista todos los usuarios."""
    try:
        users = storage.load()

        if not users:
            console.print("[yellow]No hay usuarios registrados.[/yellow]")
            return

        table = Table(title="Huéspedes Registrados")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Nombre", style="magenta")
        table.add_column("Email", style="green")

        for user in users:
            table.add_row(
                str(user.get_id()),
                user.get_name(),
                user.get_email()
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


# ---------------- RESERVATIONS ----------------

@app.command(name="book")
def book_room(user_id: int, room_number: int, room_type: str):
    """
    Reserva una habitación para un usuario.
    """
    try:
        user = user_service.get_user(user_id)

        # Creamos habitación dinámicamente
        room = Room(room_number=room_number, room_type=room_type)

        hotel_service.reserve_room(user, room)

        console.print(
            f"[green]✓ Habitación {room_number} reservada para {user.get_name()}.[/green]"
        )

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command(name="cancel")
def cancel_booking(user_id: int, room_number: int):
    """
    Cancela una reserva.
    """
    try:
        user = user_service.get_user(user_id)

        # Buscar habitación en historial del usuario
        room = next(
            (r for r in user.history if r.get_room_number() == room_number),
            None
        )

        if not room:
            raise Exception("Room not found in user's reservations")

        hotel_service.cancel_reservation(user, room)

        console.print(
            f"[yellow] Reserva de la habitación {room_number} cancelada.[/yellow]"
        )

    except Exception as e:
        console.print(f"[red] Error: {e}[/red]")


if __name__ == "__main__":
    app()