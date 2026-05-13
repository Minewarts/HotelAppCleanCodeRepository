"""
API routes for user management.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List

from ...models import User
from ...schemas import UserCreate, UserResponse, UserUpdate
from ...services import UserServices
from ...storage import JSONStorage
from pathlib import Path

router = APIRouter(prefix="/users", tags=["users"])

# Initialize storage and service (in production, use dependency injection)
storage = JSONStorage(Path("data/database.json"))
user_service = UserServices(storage)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    """Create a new user."""
    try:
        user = User(
            user_id=len(storage.load()) + 1,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
        )
        user_service.create_user(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[UserResponse])
def list_users():
    """Get all users."""
    try:
        users = storage.load()
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get a user by ID."""
    try:
        user = user_service.get_user(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate):
    """Update a user."""
    try:
        updated_user = user_service.update_user(
            user_id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
        )
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Delete a user."""
    try:
        user_service.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
