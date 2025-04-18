from fastapi import FastAPI
from routes.auth_routes import auth_router  # This should match the name defined in auth_routes.py

app = FastAPI()

# Include the auth routes (login/register)
app.include_router(auth_router)
