"""
API routes for reservation management.

A reservation links a user to a room, updates room status,
and automatically records the action in user_history.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ...storage.supabase_storage import SupabaseStorage

router = APIRouter(prefix="/reservations", tags=["reservations"])

storage = SupabaseStorage()


class ReservationCreate(BaseModel):
    user_id: int
    room_id: str


class ReservationCancel(BaseModel):
    user_id: int
    room_id: str


class CheckoutRequest(BaseModel):
    user_id: int
    room_id: str


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_reservation(data: ReservationCreate):
    """Reserve a room for a user. Sets room to 'Ocupada' and logs Check-in."""
    # Validate user exists
    user = storage.get_user_by_id(data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {data.user_id} not found")

    # Validate room exists and is available
    room = storage.get_room_by_id(data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room '{data.room_id}' not found")
    if room["status"] != "Disponible":
        raise HTTPException(
            status_code=400,
            detail=f"Room '{data.room_id}' is not available (current status: {room['status']})",
        )

    # Update room status
    storage.update_room(data.room_id, {"status": "Ocupada"})

    # Log history
    history = storage.create_history({
        "user_id": data.user_id,
        "room_id": data.room_id,
        "action": "Check-in",
        "description": f"Reserva creada para habitación {data.room_id}",
    })

    return {
        "message": "Reservation created successfully",
        "user_id": data.user_id,
        "room_id": data.room_id,
        "history_id": history["id"],
    }


@router.post("/cancel", status_code=status.HTTP_200_OK)
def cancel_reservation(data: ReservationCancel):
    """Cancel a reservation. Sets room back to 'Disponible' and logs cancellation."""
    user = storage.get_user_by_id(data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {data.user_id} not found")

    room = storage.get_room_by_id(data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room '{data.room_id}' not found")
    if room["status"] != "Ocupada":
        raise HTTPException(
            status_code=400,
            detail=f"Room '{data.room_id}' is not currently occupied",
        )

    # Free the room
    storage.update_room(data.room_id, {"status": "Disponible"})

    # Log history
    history = storage.create_history({
        "user_id": data.user_id,
        "room_id": data.room_id,
        "action": "Cancelacion de reserva",
        "description": f"Reserva cancelada para habitación {data.room_id}",
    })

    return {
        "message": "Reservation cancelled successfully",
        "user_id": data.user_id,
        "room_id": data.room_id,
        "history_id": history["id"],
    }


@router.post("/checkout", status_code=status.HTTP_200_OK)
def checkout(data: CheckoutRequest):
    """Check out a user from a room. Sets room to 'Disponible' and logs Check-out."""
    user = storage.get_user_by_id(data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {data.user_id} not found")

    room = storage.get_room_by_id(data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room '{data.room_id}' not found")
    if room["status"] != "Ocupada":
        raise HTTPException(
            status_code=400,
            detail=f"Room '{data.room_id}' is not currently occupied",
        )

    # Free the room
    storage.update_room(data.room_id, {"status": "Disponible"})

    # Log history
    history = storage.create_history({
        "user_id": data.user_id,
        "room_id": data.room_id,
        "action": "Check-out",
        "description": f"Check-out realizado para habitación {data.room_id}",
    })

    return {
        "message": "Check-out successful",
        "user_id": data.user_id,
        "room_id": data.room_id,
        "history_id": history["id"],
    }
