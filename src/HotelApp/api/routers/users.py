"""
API routes for user management.

All data is persisted in Supabase. The router delegates
raw DB access to SupabaseStorage.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status

from ...schemas import UserCreate, UserResponse, UserUpdate
from ...storage.supabase_storage import SupabaseStorage

router = APIRouter(prefix="/users", tags=["users"])

storage = SupabaseStorage()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    """Create a new user."""
    try:
        result = storage.create_user(user_data.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[UserResponse])
def list_users():
    """Get all registered users."""
    try:
        return storage.get_all_users()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get a user by ID."""
    user = storage.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found"
        )
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate):
    """Partially update a user (only provided fields are changed)."""
    try:
        payload = user_data.model_dump(exclude_none=True)
        return storage.update_user(user_id, payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Delete a user."""
    try:
        storage.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
