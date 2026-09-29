from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud, schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserResponse, status_code=201)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, user)

@router.get("/org/{org_id}", response_model=list[schemas.UserResponse])
async def get_users_by_org(org_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_users(db, org_id)