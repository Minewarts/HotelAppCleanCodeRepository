"""
API routes for user history management.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List

from ...models import UserHistory
from ...schemas import UserHistoryCreate, UserHistoryResponse
from ...services import HotelService
from ...storage import get_default_storage

router = APIRouter(prefix="/user-history", tags=["user-history"])

# Initialize storage and service (in production, use dependency injection)
storage = get_default_storage()
hotel_service = HotelService(storage)


@router.post("/", response_model=UserHistoryResponse, status_code=status.HTTP_201_CREATED)
def create_history(history_data: UserHistoryCreate):
    """Record a user action in history."""
    try:
        history = hotel_service.log_user_action(
            user_id=history_data.user_id,
            action=history_data.action,
            description=history_data.description,
        )
        return history
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=List[UserHistoryResponse])
def get_user_history(user_id: int):
    """Get all history records for a user."""
    try:
        history = hotel_service.get_user_history(user_id)
        return history
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
