from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import urllib

#  Database config using Windows Authentication
params = urllib.parse.quote_plus(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=HARSHAP;"             # ← Replace with your actual SSMS server name if different
    "Database=login_db;"          # ← Replace if your DB name is different
    "Trusted_Connection=yes;"
)

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

#  SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#  User table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

Base.metadata.create_all(bind=engine)

#  FastAPI app
app = FastAPI()

#  DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Request model
class UserRequest(BaseModel):
    username: str
    password: str

#  Register endpoint
@app.post("/register")
def register(request: UserRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(username=request.username, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

#  Login endpoint
@app.post("/login")
def login(request: UserRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == request.username, User.password == request.password
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", "user_id": user.id}