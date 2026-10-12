
from collections.abc import Callable
from fastapi import Depends
from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Mapped, DeclarativeBase, mapped_column, mapped_collection, Session


DATABASE_URL = 'postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres'
engine = create_engine(DATABASE_URL)
Sessionlocal: Callable = sessionmaker(
    bind=engine
)


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

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)


@app.get('/tasks')
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    task_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in task_from_db]



@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()


    return task_orm_to_model(new_task)



@app.patch('/tasks/{task_id}')#---------------------------
def update_task(task_id : str, payload: TaskUpdate, db: Session = Depends(get_db)) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed:
        task_for_update.completed = payload.completed

    db.commit()
    return task_for_update
    


@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id, db: Session = Depends(get_db)):
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()

#----------------------------------------------------------------------------------------------------------------------------------
class CategorySchema(BaseModel):
    id: str
    name: str
    
class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str | None = None




class CategoryORM(Base):
    __tablename__ = 'categories'


categories: list[CategorySchema] = []



@app.get('/categories')
def read_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    return categories


@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategorySchema(id=str(uuid4()), name=payload.name)

    categories.append(new_category)
    return new_category


@app.patch('/categories/{category_id}')
def update_category(category_id : str, payload: CategoryUpdate, db: Session = Depends(get_db)):
    for category in categories:
        if category.id == category_id:
            if payload.name:
                category.name = payload.name
            return category

@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id, db: Session = Depends(get_db)):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)