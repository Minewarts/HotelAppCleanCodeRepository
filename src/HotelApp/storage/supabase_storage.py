"""
Implementación de storage usando Supabase como base de datos.
"""

from typing import Literal, Optional
from supabase import Client

from ..core.supabase_client import get_supabase_client
from ..core.exceptions import UserNotFoundError


class SupabaseStorage:

    def __init__(self) -> None:
        self.client: Client = get_supabase_client()

    # ------------------------------------------------------------------ #
    #  Users                                                               #
    # ------------------------------------------------------------------ #

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

    def filter_rooms(
        self,
        room_type: Optional[str] = None,
        status: Optional[str] = None,
        max_price: Optional[float] = None,
        min_price: Optional[float] = None,
    ) -> list[dict]:
        """Filter rooms by type, status and/or price range."""
        query = self.client.table("rooms").select("*")
        if room_type:
            query = query.eq("room_type", room_type)
        if status:
            query = query.eq("status", status)
        if min_price is not None:
            query = query.gte("price_per_night", min_price)
        if max_price is not None:
            query = query.lte("price_per_night", max_price)
        response = query.execute()
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
