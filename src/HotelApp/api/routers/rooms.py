"""
API routes for room management.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from decimal import Decimal

from ...models import Room
from ...schemas import RoomCreate, RoomResponse, RoomUpdate
from ...storage import JSONStorage
from pathlib import Path

router = APIRouter(prefix="/rooms", tags=["rooms"])

# Initialize storage (in production, use dependency injection)
storage = JSONStorage(Path("data/database.json"))

# In-memory room storage (replace with database in production)
_rooms: List[Room] = []


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room_data: RoomCreate):
    """Create a new room."""
    try:
        room = Room(
            number_id=room_data.number_id,
            room_type=room_data.room_type,
            price_per_night=room_data.price_per_night,
        )
        _rooms.append(room)
        return room
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[RoomResponse])
def list_rooms():
    """Get all rooms."""
    return _rooms


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: str):
    """Get a room by ID."""
    for room in _rooms:
        if room.get_number_id() == room_id:
            return room
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")


@router.patch("/{room_id}", response_model=RoomResponse)
def update_room(room_id: str, room_data: RoomUpdate):
    """Update a room."""
    for room in _rooms:
        if room.get_number_id() == room_id:
            try:
                if room_data.number_id is not None:
                    room._number_id = room_data.number_id
                if room_data.room_type is not None:
                    room._room_type = room_data.room_type
                if room_data.price_per_night is not None:
                    room._price_per_night = room_data.price_per_night
                if room_data.status is not None:
                    room.set_status(room_data.status)
                return room
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: str):
    """Delete a room."""
    for i, room in enumerate(_rooms):
        if room.get_number_id() == room_id:
            _rooms.pop(i)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
