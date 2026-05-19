"""
API routes for user history management.

All data is persisted in Supabase via SupabaseStorage.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status

from ...schemas import UserHistoryCreate, UserHistoryResponse
from ...storage.supabase_storage import SupabaseStorage

router = APIRouter(prefix="/user-history", tags=["user-history"])

storage = SupabaseStorage()


@router.post("/", response_model=UserHistoryResponse, status_code=status.HTTP_201_CREATED)
def create_history(history_data: UserHistoryCreate):
    """Record a user action in history."""
    try:
        user = storage.get_user_by_id(history_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {history_data.user_id} not found",
            )
        payload = history_data.model_dump()
        result = storage.create_history(payload)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=List[UserHistoryResponse])
def get_user_history(user_id: int):
    """Get all history records for a user."""
    try:
        user = storage.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )
        return storage.get_history_by_user(user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(history_id: int):
    """Delete a history record by its ID."""
    try:
        storage.delete_history(history_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))