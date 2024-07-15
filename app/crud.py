from sqlalchemy.orm import Session
from . import models, schemas

def get_todo_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ToDoItem).offset(skip).limit(limit).all()

def create_todo_item(db: Session, todo_item: schemas.TodoItemCreate):
    db_todo_item = models.ToDoItem(**todo_item.dict())
    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

def get_todo_item(db: Session, todo_item_id: int):
    return db.query(models.TodoItem).filter(models.TodoItem.id == todo_item_id).first()

def update_todo_item(db: Session, todo_item_id: int, todo_item: schemas.TodoItemCreate):
    db_todo_item = get_todo_item(db, todo_item_id)
    if db_todo_item:
        db_todo_item.title = todo_item.title
        db_todo_item.description = todo_item.description
        db.commit()
        db.refresh(db_todo_item)
    return db_todo_item

def delete_todo_item(db: Session, todo_item_id: int):
    db_todo_item = get_todo_item(db, todo_item_id)
    if db_todo_item:
        db.delete(db_todo_item)
        db.commit()
    return db_todo_item
