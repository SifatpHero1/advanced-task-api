from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud, schemas

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.post("/", response_model=schemas.OrgResponse, status_code=201)
async def create_org(org: schemas.OrgCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_org(db, org)

@router.get("/", response_model=list[schemas.OrgResponse])
async def get_orgs(db: AsyncSession = Depends(get_db)):
    return await crud.get_orgs(db)