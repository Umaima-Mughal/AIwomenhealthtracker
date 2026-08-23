from fastapi import FastAPI
from sqlalchemy import text
from backend.app.api.auth import router as auth_router
from backend.app.api.health import router as health_router
from backend.app.core.config import settings
from backend.app.core.database import Base, engine
from backend.app.api.tracking import router as tracking_router
from backend.app.api.history import router as history_router
from backend.app.api import pcos
from backend.app.api import chat
from backend.app.api import pregnancy
from backend.app.api import symptoms
from backend.app.api import cycle
from backend.app.api.doctor import router as doctor_router
from backend.app.db_models import (
    User,
    Tracking,
    ChatMessage,
    Insight,
    Notification,
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(tracking_router)
app.include_router(chat.router)
app.include_router(pcos.router)
app.include_router(pregnancy.router)
app.include_router(symptoms.router)
app.include_router(cycle.router)
app.include_router(history_router)
app.include_router(doctor_router)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} API is running"
    }


@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))

            return {
                "database": "connected",
                "result": result.scalar()
            }

    except Exception as e:
        return {
            "database": "connection failed",
            "error": str(e)
        }