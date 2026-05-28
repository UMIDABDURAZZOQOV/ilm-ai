from fastapi import APIRouter
from pydantic import BaseModel
import hashlib
import json
import os

router = APIRouter(prefix="/auth", tags=["auth"])

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@router.post("/signup")
def signup(data: SignupRequest):
    users = load_users()
    if any(u["email"] == data.email for u in users):
        return {"error": "Gmail aready exists"}
    user = {
        "id": len(users) + 1,
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password)
    }
    users.append(user)
    save_users(users)
    return {"message": "You registered successfully", "user_id": user["id"]}

@router.post("/login")
def login(data: LoginRequest):
    users = load_users()
    user = next((u for u in users if u["email"] == data.email and u["password"] == hash_password(data.password)), None)
    if not user:
        return {"error": "Invalid email or password"}
    return {"message": "Login successful", "user_id": user["id"], "name": user["name"]}