"""
Schemas Pydantic para la entidad UserHistory.

Reglas de negocio validadas aqui:
- action debe describir que hizo el usuario en el hotel (ej. Reserva, Check-in).
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class UserHistoryBase(BaseModel):
    """Campos comunes a todas las representaciones de UserHistory."""

    user_id: int = Field(
        ...,
        description="ID del usuario asociado a la accion.",
    )
    room_id: str | None = Field(
        default=None,
        min_length=1,
        description="ID de la habitacion asociada a la accion.",
        examples=["101"],
    )
    action: Literal["Check-in", "Check-out", "Reserva", "Cancelacion de reserva"] = Field(
        ...,
        description="Accion realizada por o para el cliente.",
        examples=["Check-in", "Cancelacion de reserva"],
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Detalles adicionales de la accion.",
    )
    check_in_date: datetime | None = Field(
        default=None,
        description="Fecha y hora del check-in.",
    )
    check_out_date: datetime | None = Field(
        default=None,
        description="Fecha y hora del check-out.",
    )


class UserHistoryCreate(UserHistoryBase):
    """Payload para registrar un evento en el historial (POST /user-history)."""


class UserHistoryResponse(UserHistoryBase):
    """Representacion de un registro de historial devuelto por la API."""

    id: int = Field(..., description="Identificador del registro.")
    timestamp: datetime = Field(..., description="Fecha y hora del registro.")

    model_config = {"from_attributes": True}