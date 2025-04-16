from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import urllib
import sqlalchemy.exc

#  Database config using Windows Authentication
params = urllib.parse.quote_plus(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=HARSHAP;"
    "Database=login_db;"
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
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#  Request model
class UserRequest(BaseModel):
    username: str
    password: str

#  Register endpoint with exception handling
@app.post("/register")
def register(request: UserRequest, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.username == request.username).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

        new_user = User(username=request.username, password=request.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully", "user_id": new_user.id}

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error during registration: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error: {str(e)}")

#  Login endpoint with exception handling
@app.post("/login")
def login(request: UserRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(
            User.username == request.username, User.password == request.password
        ).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

        return {"message": "Login successful", "user_id": user.id}

    except sqlalchemy.exc.SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error during login: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error: {str(e)}")
