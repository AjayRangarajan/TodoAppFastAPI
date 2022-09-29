from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        
class TodoTask(BaseModel):
    task: str

    class Config:
        orm_mode = True

class Todo(BaseModel):
    id: int
    task: str

    class Config:
        orm_mode = True