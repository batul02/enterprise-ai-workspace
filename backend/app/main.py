from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine
from app.api.v1.router import api_router

app = FastAPI(
    title="Enterprise AI Workspace",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Enterprise AI Workspace API"
    }

# @app.get("/db-test")
# def test_database():
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT version();"))
#         version = result.scalar()

#     return {
#         "status": "connected",
#         "postgres_version": version
#     }

app.include_router(
    api_router,
    prefix="/api/v1",
)