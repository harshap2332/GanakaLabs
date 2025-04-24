from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database setup
DATABASE_URL = "postgresql://postgres:ASDasd%40234@localhost:5432/employee_management"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow the frontend to access the API
origins = [
    "http://localhost:3000",  # URL of your React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from React app
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (e.g., GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

# FastAPI routes and models
class EmployeeEquipment(Base):
    __tablename__ = "employee_equipment"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, index=True)
    laptop_id = Column(String)
    adapter_id = Column(String)
    charger_id = Column(String)
    mouse_id = Column(String)
    date_of_receiving = Column(Date)
    date_of_returning = Column(Date)

class EmployeeProfile(BaseModel):
    employee_name: str
    laptop_id: str
    adapter_id: str
    charger_id: str
    mouse_id: str
    date_of_receiving: str
    date_of_returning: str

Base.metadata.create_all(bind=engine)

@app.post("/create-profile/")
def create_profile(profile: EmployeeProfile):
    db = SessionLocal()
    db_profile = EmployeeEquipment(
        employee_name=profile.employee_name,
        laptop_id=profile.laptop_id,
        adapter_id=profile.adapter_id,
        charger_id=profile.charger_id,
        mouse_id=profile.mouse_id,
        date_of_receiving=profile.date_of_receiving,
        date_of_returning=profile.date_of_returning
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    db.close()
    return db_profile

@app.get("/search-profile/{employee_name}")
def search_profile(employee_name: str):
    db = SessionLocal()
    db_profile = db.query(EmployeeEquipment).filter(EmployeeEquipment.employee_name == employee_name).first()
    db.close()
    if db_profile:
        return db_profile
    raise HTTPException(status_code=404, detail="Employee not found")
