"""
API routes for hotel configuration.
"""

from fastapi import APIRouter, HTTPException, status

from ...schemas import HotelUpdate

router = APIRouter(prefix="/hotel", tags=["hotel"])

# Global hotel instance (in production, use a database)
_hotel = {
    "name": "HOT TEL",
    "address": "123 Main St",
    "phone": "+1-555-0000",
}


@router.get("/")
def get_hotel():
    """Get hotel information."""
    return _hotel


@router.put("/")
def update_hotel(hotel_data: HotelUpdate):
    """Update hotel information."""
    try:
        if hotel_data.name is not None:
            _hotel["name"] = hotel_data.name
        if hotel_data.address is not None:
            _hotel["address"] = hotel_data.address
        if hotel_data.phone is not None:
            _hotel["phone"] = hotel_data.phone
        return _hotel
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))