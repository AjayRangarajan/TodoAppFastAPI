from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine
from sqlalchemy.orm import Session
from typing import List
import schemas
import models
from database import SessionLocal

Base.metadata.create_all(engine)

app = FastAPI()

def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()

@app.get("/")
def hello():
    return "Hello"

@app.get("/tasks", response_model=List[schemas.Todo])
def tasks(session: Session = Depends(get_session)):
    todo_list = session.query(models.Todo).all()
    return todo_list

@app.post("/task", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_task(todo: schemas.CreateTask, session: Session = Depends(get_session)):
    todo_obj = models.Todo(task=todo.task)
    session.add(todo_obj)                               
    session.commit()
    session.refresh(todo_obj)
    return todo_obj

@app.get("/task/{id}")
def get_task(id: int, session: Session = Depends(get_session)):
    todo = session.query(models.Todo).get(id)
    if not todo:
        return HTTPException(status_code=404, detail=f"Todo item with id {id} not found")
    return todo

@app.put("/task/{id}")
def update_task(id: int, todo_new: schemas.CreateTask, session: Session = Depends(get_session)):
    todo = session.query(models.Todo).get(id)
    if not todo:
        return HTTPException(status_code=404, detail=f"Todo item with id {id} not found")
    todo.task = todo_new.task
    session.commit()
    return todo

@app.delete("/task/{id}")
def delete_task(id: int, session: Session = Depends(get_session)):
    todo = session.query(models.Todo).get(id)
    if not todo:
        return HTTPException(status_code=404, detail=f"Todo item with id {id} not found")
    session.delete(todo)
    session.commit()
    return f"Task {id} deleted successfully!"