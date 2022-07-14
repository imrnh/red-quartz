from fastapi import FastAPI
from routes.autheticationRoute import authRouter

app = FastAPI()
app.include_router(authRouter, prefix="/auth", tags = ["Authentication"])