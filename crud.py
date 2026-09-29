from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Organization, User, Team, Task, Comment, team_members
from schemas import OrgCreate, UserCreate, TeamCreate, TaskCreate, TaskUpdate

async def create_org(db: AsyncSession, org: OrgCreate):
    db_org = Organization(**org.model_dump())
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org

async def get_orgs(db: AsyncSession):
    result = await db.execute(select(Organization))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession, org_id: int):
    result = await db.execute(select(User).where(User.org_id == org_id))
    return result.scalars().all()

async def create_team(db: AsyncSession, team: TeamCreate):
    db_team = Team(name=team.name, org_id=team.org_id)
    db.add(db_team)
    await db.flush()
    if team.member_ids:
        for user_id in team.member_ids:
            await db.execute(team_members.insert().values(team_id=db_team.id, user_id=user_id))
    await db.commit()
    await db.refresh(db_team)
    return db_team

async def create_task(db: AsyncSession, task: TaskCreate):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_tasks(db: AsyncSession, org_id: int, skip: int = 0, limit: int = 20, status: str = None, assignee_id: int = None):
    query = select(Task).where(Task.org_id == org_id)
    if status:
        query = query.where(Task.status == status)
    if assignee_id:
        query = query.where(Task.assignee_id == assignee_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()

async def update_task(db: AsyncSession, task_id: int, task_update: TaskUpdate):
    db_task = await get_task(db, task_id)
    if not db_task: return None
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def create_comment(db: AsyncSession, task_id: int, user_id: int, content: str):
    db_comment = Comment(task_id=task_id, user_id=user_id, content=content)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def get_task_comments(db: AsyncSession, task_id: int):
    result = await db.execute(select(Comment).where(Comment.task_id == task_id).order_by(Comment.created_at.desc()))
    return result.scalars().all()