from fastapi import APIRouter, Depends
from controllers.auth_controller import create_user, authenticate_user
from models.user import User
from sqlalchemy.orm import Session
from database import get_db

# Define the router for auth-related routes
auth_router = APIRouter()

# Route for registering a user
@auth_router.post("/register")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    return create_user(db, username, password)

# Route for logging in a user
@auth_router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    return {"message": "Login successful", "user_id": user.id}
