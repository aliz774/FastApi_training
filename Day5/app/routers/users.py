from fastapi import APIRouter, HTTPException, Response
from pwdlib import PasswordHash

from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

password_hash = PasswordHash.recommended()

users = {}
next_id = 1


@router.post("", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate, response: Response):
    global next_id

    for user in users.values():
        if user["email"] == payload.email:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

    hashed_password = password_hash.hash(payload.password)

    new_user = {
        "id": next_id,
        "email": payload.email,
        "password_hash": hashed_password,
        "full_name": payload.full_name,
        "role": "user"
    }

    users[next_id] = new_user

    next_id += 1

    return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = users.get(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate):
    user = users.get(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    if "full_name" in updates and updates["full_name"] is None:
        raise HTTPException(
            status_code=422,
            detail="Full name cannot be null"
        )

    user.update(updates)

    return user