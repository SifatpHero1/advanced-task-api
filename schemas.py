from pydantic import BaseModel, ConfigDict
from datetime import datetime
from models import TaskStatus

class OrgCreate(BaseModel):
    name: str

class OrgResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    name: str
    email: str
    org_id: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    org_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TeamCreate(BaseModel):
    name: str
    org_id: int
    member_ids: list[int] = []

class TeamResponse(BaseModel):
    id: int
    name: str
    org_id: int
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    org_id: int
    creator_id: int
    assignee_id: int | None = None
    team_id: int | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    assignee_id: int | None = None
    team_id: int | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    org_id: int
    creator_id: int
    assignee_id: int | None
    team_id: int | None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CommentCreate(BaseModel):
    user_id: int
    content: str

class CommentResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)