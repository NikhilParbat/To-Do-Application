from pydantic import BaseModel

class TodoItemBase(BaseModel):
    title: str
    description: str

class TodoItemCreate(TodoItemBase):
    pass

class TodoItem(TodoItemBase):
    id: int
    completed: bool

    class Config:
        from_attributes = True
