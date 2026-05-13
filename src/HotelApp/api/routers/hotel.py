"""
API routes for hotel configuration.
"""

from fastapi import APIRouter, HTTPException, status

from ...models import Hotel
from ...schemas import HotelUpdate

router = APIRouter(prefix="/hotel", tags=["hotel"])

# Global hotel instance (in production, use a database)
_hotel = Hotel(name="HOT TEL", address="123 Main St", phone="+1-555-0000")


@router.get("/")
def get_hotel():
    """Get hotel information."""
    return {
        "name": _hotel.get_name(),
        "address": _hotel.get_address(),
        "phone": _hotel.get_phone(),
    }


@router.put("/")
def update_hotel(hotel_data: HotelUpdate):
    """Update hotel information."""
    try:
        if hotel_data.name is not None:
            _hotel.set_name(hotel_data.name)
        if hotel_data.address is not None:
            _hotel.set_address(hotel_data.address)
        if hotel_data.phone is not None:
            _hotel.set_phone(hotel_data.phone)

        return {
            "name": _hotel.get_name(),
            "address": _hotel.get_address(),
            "phone": _hotel.get_phone(),
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
