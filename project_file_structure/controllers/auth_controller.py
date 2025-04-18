from models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException

# Function to create a new user
def create_user(db: Session, username: str, password: str):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Function to authenticate a user
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user
