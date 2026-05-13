"""API routers for HotelApp."""

from .users import router as users_router
from .rooms import router as rooms_router
from .user_history import router as user_history_router
from .hotel import router as hotel_router

__all__ = ["users_router", "rooms_router", "user_history_router", "hotel_router"]
