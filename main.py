from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
from routers import organizations, users, teams, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Advanced Task Management API",
    description="Relational Task API with Comments & Filtering",
    version="2.0.0",
    lifespan=lifespan
)

app.include_router(organizations.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(teams.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Advanced Async Task Management API"}