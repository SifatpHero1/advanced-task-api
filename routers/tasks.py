from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud, schemas

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db=db, task=task)

@router.get("/org/{org_id}", response_model=list[schemas.TaskResponse])
async def get_tasks_by_org(org_id: int, skip: int = 0, limit: int = 20, status: str = None, assignee_id: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_tasks(db, org_id=org_id, skip=skip, limit=limit, status=status, assignee_id=assignee_id)

@router.patch("/{task_id}", response_model=schemas.TaskResponse)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    db_task = await crud.update_task(db, task_id=task_id, task_update=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.post("/{task_id}/comments", response_model=schemas.CommentResponse, status_code=201)
async def add_comment(task_id: int, comment: schemas.CommentCreate, db: AsyncSession = Depends(get_db)):
    db_task = await crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await crud.create_comment(db, task_id=task_id, user_id=comment.user_id, content=comment.content)

@router.get("/{task_id}/comments", response_model=list[schemas.CommentResponse])
async def get_comments(task_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_task_comments(db, task_id)