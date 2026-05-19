"""
Implementación de storage usando Supabase como base de datos.

Esta clase implementa el protocolo `Storage` y reemplaza a `JSONStorage`
cuando las variables de entorno de Supabase están configuradas.

Tablas requeridas en Supabase (ver docs/getting-started.md):
    - users
    - rooms
    - user_history
"""

from typing import List

from supabase import Client

from ..core.supabase_client import get_supabase_client
from ..core.exceptions import UserNotFoundError
from ..models import User, UserHistory


class SupabaseStorage:
    """
    Storage implementation backed by Supabase (PostgreSQL).

    Implements the Storage protocol so it can be used as a drop-in
    replacement for JSONStorage without changing any service logic.
    """

    def __init__(self) -> None:
        """Initializes the storage and establishes the Supabase connection."""
        self.client: Client = get_supabase_client()

    # ------------------------------------------------------------------ #
    #  Users                                                               #
    # ------------------------------------------------------------------ #

    def load(self) -> List[User]:
        response = (
            self.client.table("users")
            .select("*, user_history(*)")
            .execute()
        )
        users: List[User] = []
        for row in response.data:
            user = User(
                user_id=row["id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
            )
            for h in row.get("user_history", []):
                user.history.append(
                    UserHistory(
                        user_id=h["user_id"],
                        action=h["action"],
                        description=h.get("description"),
                        timestamp=h.get("timestamp"),
                    )
                )
            users.append(user)
        return users

    def save(self, users: List[User]) -> None:
        for user in users:
            self.client.table("users").upsert(
                {
                    "id": user.get_id(),
                    "first_name": user.get_first_name(),
                    "last_name": user.get_last_name(),
                    "email": user.get_email(),
                }
            ).execute()

    def get_all_users(self) -> list[dict]:
        response = self.client.table("users").select("*").execute()
        return response.data

    def get_user_by_id(self, user_id: int) -> dict | None:
        response = (
            self.client.table("users")
            .select("*")
            .eq("id", user_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def create_user(self, data: dict) -> dict:
        response = self.client.table("users").insert(data).execute()
        return response.data[0]

    def update_user(self, user_id: int, data: dict) -> dict:
        response = (
            self.client.table("users")
            .update(data)
            .eq("id", user_id)
            .execute()
        )
        if not response.data:
            raise UserNotFoundError(user_id)
        return response.data[0]

    def delete_user(self, user_id: int) -> None:
        existing = self.get_user_by_id(user_id)
        if not existing:
            raise UserNotFoundError(user_id)
        self.client.table("users").delete().eq("id", user_id).execute()

    # ------------------------------------------------------------------ #
    #  Rooms                                                               #
    # ------------------------------------------------------------------ #

    def get_all_rooms(self) -> list[dict]:
        response = self.client.table("rooms").select("*").execute()
        return response.data

    def get_room_by_id(self, room_id: str) -> dict | None:
        response = (
            self.client.table("rooms")
            .select("*")
            .eq("number_id", room_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def create_room(self, data: dict) -> dict:
        response = self.client.table("rooms").insert(data).execute()
        return response.data[0]

    def update_room(self, room_id: str, data: dict) -> dict:
        response = (
            self.client.table("rooms")
            .update(data)
            .eq("number_id", room_id)
            .execute()
        )
        if not response.data:
            raise Exception(f"Room '{room_id}' not found")
        return response.data[0]

    def delete_room(self, room_id: str) -> None:
        existing = self.get_room_by_id(room_id)
        if not existing:
            raise Exception(f"Room '{room_id}' not found")
        self.client.table("rooms").delete().eq("number_id", room_id).execute()

    # ------------------------------------------------------------------ #
    #  User History                                                        #
    # ------------------------------------------------------------------ #

    def get_history_by_user(self, user_id: int) -> list[dict]:
        response = (
            self.client.table("user_history")
            .select("*")
            .eq("user_id", user_id)
            .order("timestamp", desc=True)
            .execute()
        )
        return response.data

    def create_history(self, data: dict) -> dict:
        response = self.client.table("user_history").insert(data).execute()
        return response.data[0]

    def delete_history(self, history_id: int) -> None:
        response = (
            self.client.table("user_history")
            .select("id")
            .eq("id", history_id)
            .execute()
        )
        if not response.data:
            raise Exception(f"History record {history_id} not found")
        self.client.table("user_history").delete().eq("id", history_id).execute()