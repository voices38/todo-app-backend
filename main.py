from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

tasks: list[TaskSchema] = []


@app.get('/tasks')
def read_tasks():
    return tasks



@app.post('/tasks')
def create_task(payload):
    new_task = TaskSchema(id=str(uuid4), title=payload.title, completed=False)
    
    tasks.append(new_task)