
from contextlib import asynccontextmanager
from sqlalchemy.orm import mapped_collection
from sqlalchemy.orm import mapped_column
from uuid import uuid4
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Mapped, DeclarativeBase


DATABASE_URL = 'postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres'
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__ = 'tasks'

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
       


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*']
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):#---------------------------
    title: str | None = None
    completed: bool | None = None

tasks: list[TaskSchema] = []

@app.get('/tasks')
def read_tasks() -> list[TaskSchema]:
    return tasks



@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    
    tasks.append(new_task)
    return new_task



@app.patch('/tasks/{task_id}')#---------------------------
def update_task(task_id : str, payload: TaskUpdate):
   for task in tasks:
    if task.id == task_id:
        if payload.title is not None:
            task.title = payload.title
        if payload.completed is not None:
            task.completed = payload.completed
        return task


@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)


#----------------------------------------------------------------------------------------------------------------------------------
class CategorySchema(BaseModel):
    id: str
    name: str
    
class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str | None = None

categories: list[CategorySchema] = []



@app.get('/categories')
def read_categories() -> list[CategorySchema]:
    return categories


@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate) -> CategorySchema:
    new_category = CategorySchema(id=str(uuid4()), name=payload.name)

    categories.append(new_category)
    return new_category


@app.patch('/categories/{category_id}')
def update_category(category_id : str, payload: CategoryUpdate):
    for category in categories:
        if category.id == category_id:
            if payload.name:
                category.name = payload.name
            return category

@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)