from datetime import timedelta
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine
from sqlalchemy.orm import Session
from typing import List
import schemas
import models
from database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from utils import *


Base.metadata.create_all(engine)

app = FastAPI()

def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), session: SessionLocal = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = session.query(models.User).filter(models.User.username==username).first()
    if user is None:
        raise credentials_exception
    return user


# User APIs

@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: schemas.CreateUser, session: SessionLocal = Depends(get_session)):
    """
    User API to signup the user in the application.
    Schema Used: CreateUser
    """
    new_user = models.User(username=user.username, password=get_password_hash(user.password))
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except Exception as exception:
        return HTTPException(status_code=404, detail=exception)
    return f"Successfully created User {new_user.username} with id {new_user.id}."

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: SessionLocal = Depends(get_session)):
    """
    API to login the user.
    Required form fields: username, password
    On Success: JWT access token will be returned.
    """
    username = form_data.username
    password = form_data.password
    if authenticate_user(username, password, session):
        access_token = create_access_token(
            data = {"sub": username},
            expire_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

# Index API

@app.get("/")
def index(token: str = Depends(oauth2_scheme), session: SessionLocal = Depends(get_session)):
    current_user = get_current_user(token, session)
    return {"current_user": current_user.username, "token": token}


# Task APIs

@app.get("/tasks", response_model=List[schemas.Todo])
def tasks(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """
    Returns list of all the Tasks of the User.
    User Login required.
    """
    user = get_current_user(token, session)
    todo_list = session.query(models.Todo).filter(models.Todo.user==user).all()
    return todo_list

@app.post("/task", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_task(todo: schemas.TodoTask, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """
    API to create Task.
    User Login required.
    Creates Task with the logged in user.
    On Success: Returns the task.
    """
    todo_obj = models.Todo(task=todo.task)
    user = get_current_user(token, session)
    todo_obj.user_id = user.id
    todo_obj.user = user
    session.add(todo_obj)                               
    session.commit()
    session.refresh(todo_obj)
    return todo_obj

@app.get("/task/{id}", response_model=schemas.TodoTask)
def get_task(id: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """
    API endpoint to return a task of the user.
    Required parameter: Task Id.
    User Login required.
    On Success: Returns the task.
    """
    todo = session.query(models.Todo).get(id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo item with id {id} not found")
    user = get_current_user(token, session)
    if todo.user != user:
        raise HTTPException(status_code=401, detail=f"The user doesn't have access to this task.")
    return todo

@app.put("/task/{id}", response_model=schemas.TodoTask)
def update_task(id: int, todo_new: schemas.TodoTask, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """
    API endpoint to update a task.
    Required parameter: Task Id.
    Schema Used: TodoTask
    User Login required.
    On Success: Returns the updated Task.
    """
    todo = session.query(models.Todo).get(id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo item with id {id} not found")
    user = get_current_user(token, session)
    if todo.user != user:
        raise HTTPException(status_code=401, detail=f"The user doesn't have access to this task.")
    todo.task = todo_new.task
    session.commit()
    return todo

@app.delete("/task/{id}")
def delete_task(id: int, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """
    API endpoint to delete a task.
    Required parameter: Task Id.
    User Login required.
    On Success: Returns Success message.
    """
    todo = session.query(models.Todo).get(id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo item with id {id} not found")
    user = get_current_user(token, session)
    if todo.user != user:
        raise HTTPException(status_code=401, detail=f"The user doesn't have access to this task.")
    session.delete(todo)
    session.commit()
    return f"Task {id} deleted successfully!"