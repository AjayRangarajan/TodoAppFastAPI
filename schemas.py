from pydantic import BaseModel

class CreateTask(BaseModel):
    task: str

class Todo(BaseModel):
    id: int
    task: str

    class Config:
        orm_mode = True