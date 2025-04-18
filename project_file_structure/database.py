from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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

#  Function to create a session (to be used for DB transactions)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
