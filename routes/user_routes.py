# routes/user_route.py
from fastapi import APIRouter, HTTPException
from crud.user_crud import create_user, get_users, get_user_by_phone, update_user, delete_user
from models.user import User

router = APIRouter()

@router.post("/users/")
async def create_new_user(user: User):
    return await create_user(user)

@router.get("/users/")
async def get_all_users():
    return await get_users()

@router.get("/users/{phone}")
async def get_user(phone: str):
    user = await get_user_by_phone(phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{id}")
async def update_user_data(id: str, user: User):
    await update_user(id, user)
    return {"message": "User updated"}

@router.delete("/users/{id}")
async def delete_user_data(id: str):
    await delete_user(id)
    return {"message": "User deleted"}
