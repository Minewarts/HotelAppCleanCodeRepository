"""
API routes for room management.

All data is persisted in Supabase via SupabaseStorage.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status

from ...schemas import RoomCreate, RoomResponse, RoomUpdate
from ...storage.supabase_storage import SupabaseStorage

router = APIRouter(prefix="/rooms", tags=["rooms"])

storage = SupabaseStorage()


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room_data: RoomCreate):
    """Create a new room."""
    try:
        payload = room_data.model_dump()
        payload["price_per_night"] = float(payload["price_per_night"])
        result = storage.create_room(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[RoomResponse])
def list_rooms():
    """Get all rooms."""
    try:
        return storage.get_all_rooms()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: str):
    """Get a room by its number_id."""
    room = storage.get_room_by_id(room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Room '{room_id}' not found"
        )
    return room


@router.patch("/{room_id}", response_model=RoomResponse)
def update_room(room_id: str, room_data: RoomUpdate):
    """Partially update a room (only provided fields are changed)."""
    try:
        payload = room_data.model_dump(exclude_none=True)
        if "price_per_night" in payload:
            payload["price_per_night"] = float(payload["price_per_night"])
        return storage.update_room(room_id, payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: str):
    """Delete a room."""
    try:
        storage.delete_room(room_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))