"""
Pydantic schemas for API request/response validation.

This module contains Pydantic BaseModel classes for validating
and serializing data in the HotelApp API.
"""

from .hotel import HotelBase, HotelUpdate
from .room import RoomBase, RoomCreate, RoomResponse, RoomUpdate
from .user import UserBase, UserCreate, UserResponse, UserUpdate
from .user_history import UserHistoryBase, UserHistoryCreate, UserHistoryResponse

__all__ = [
    # Hotel schemas
    "HotelBase",
    "HotelUpdate",
    # Room schemas
    "RoomBase",
    "RoomCreate",
    "RoomResponse",
    "RoomUpdate",
    # User schemas
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserUpdate",
    # UserHistory schemas
    "UserHistoryBase",
    "UserHistoryCreate",
    "UserHistoryResponse",
]