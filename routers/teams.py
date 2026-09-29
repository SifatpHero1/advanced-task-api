from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud, schemas

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/", response_model=schemas.TeamResponse, status_code=201)
async def create_team(team: schemas.TeamCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_team(db, team)