"""
HOTEL - Sistema de Gestión de Reservas CLI
Aplicación de línea de comandos para gestionar el hotel.
"""

from pathlib import Path
from decimal import Decimal
from dotenv import load_dotenv
import typer
from rich.console import Console
from rich.table import Table

from src.HotelApp.models import User, UserHistory
from src.HotelApp.services import UserServices, HotelService
from src.HotelApp.storage import JSONStorage
from src.HotelApp.core.exceptions import AppError

# Load environment variables
load_dotenv()

# Initialize application
app = typer.Typer(help="HOT TEL - Sistema de Gestión de Reservas CLI")
console = Console()
storage = JSONStorage(Path("data/database.json"))
user_service = UserServices(storage)
hotel_service = HotelService(storage)


# ==================== USER COMMANDS ====================

@app.command(name="create-user")
def create_user(
    user_id: int = typer.Argument(..., help="User ID"),
    first_name: str = typer.Argument(..., help="First name"),
    last_name: str = typer.Argument(..., help="Last name"),
    email: str = typer.Argument(..., help="Email address"),
):
    """Create a new user."""
    try:
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, email=email)
        user_service.create_user(user)
        console.print(f"[green]✓ User {first_name} {last_name} created successfully.[/green]")
    except AppError as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command(name="list-users")
def list_users():
    """List all registered users."""
    try:
        users = storage.load()

        if not users:
            console.print("[yellow]No registered users.[/yellow]")
            return

        table = Table(title="Registered Users")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("First Name", style="magenta")
        table.add_column("Last Name", style="magenta")
        table.add_column("Email", style="green")

        for user in users:
            table.add_row(
                str(user.get_id()),
                user.get_first_name(),
                user.get_last_name(),
                user.get_email()
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command(name="get-user")
def get_user(user_id: int = typer.Argument(..., help="User ID")):
    """Get user details by ID."""
    try:
        user = user_service.get_user(user_id)
        console.print(f"[cyan]User ID:[/cyan] {user.get_id()}")
        console.print(f"[cyan]First Name:[/cyan] {user.get_first_name()}")
        console.print(f"[cyan]Last Name:[/cyan] {user.get_last_name()}")
        console.print(f"[cyan]Email:[/cyan] {user.get_email()}")
        console.print(f"[cyan]History Records:[/cyan] {len(user.history)}")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command(name="delete-user")
def delete_user(user_id: int = typer.Argument(..., help="User ID")):
    """Delete a user."""
    try:
        user_service.delete_user(user_id)
        console.print(f"[green]✓ User {user_id} deleted successfully.[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


# ==================== HISTORY COMMANDS ====================

@app.command(name="log-action")
def log_action(
    user_id: int = typer.Argument(..., help="User ID"),
    action: str = typer.Argument(..., help="Action performed (e.g., Check-in, Reservation)"),
    description: str = typer.Option(None, help="Additional description"),
):
    """Record a user action in history."""
    try:
        history = hotel_service.log_user_action(
            user_id=user_id,
            action=action,
            description=description
        )
        console.print(f"[green]✓ Action '{action}' recorded for user {user_id}.[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command(name="view-history")
def view_history(user_id: int = typer.Argument(..., help="User ID")):
    """View user action history."""
    try:
        history = hotel_service.get_user_history(user_id)

        if not history:
            console.print(f"[yellow]No history records for user {user_id}.[/yellow]")
            return

        table = Table(title=f"History for User {user_id}")
        table.add_column("Action", style="magenta")
        table.add_column("Description", style="cyan")
        table.add_column("Timestamp", style="green")

        for record in history:
            table.add_row(
                record.get_action(),
                record.get_description() or "-",
                str(record.get_timestamp())
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


# ==================== UTILITY COMMANDS ====================

@app.command(name="api")
def start_api():
    """Start the FastAPI server."""
    import subprocess
    import sys

    console.print("[cyan]Starting FastAPI server...[/cyan]")
    try:
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "src.HotelApp.api.main:app", "--reload"],
            cwd=Path.cwd()
        )
    except KeyboardInterrupt:
        console.print("[yellow]Server stopped.[/yellow]")


if __name__ == "__main__":
    app()

# Inicialización
storage = JSONStorage(Path("data/database.json"))
user_service = UserServices(storage)
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

        # Buscar habitación en historial del usuario (activa)
        active_history = None
        for history in user.history:
            if history.get_room().get_room_number() == room_number and history.is_active():
                active_history = history
                break

        if not active_history:
            raise Exception("Room not found in user's active reservations")

        hotel_service.cancel_reservation(user, active_history.get_room())

        console.print(
            f"[yellow] Reserva de la habitación {room_number} cancelada.[/yellow]"
        )

    except Exception as e:
        console.print(f"[red] Error: {e}[/red]")


if __name__ == "__main__":
    app()
    try:
        poblar_base_de_datos()
    except Exception as e:
        print(f"Error al poblar los datos: {e}")