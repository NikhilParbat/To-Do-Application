from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todo-items/", response_model=schemas.TodoItem)
def create_todo_item(todo_item: schemas.TodoItemCreate, db: Session = Depends(get_db)):
    db_todo_item = models.TodoItem(**todo_item.dict())
    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

@app.get("/todo-items/", response_model=list[schemas.TodoItem])
def read_todo_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todo_items = crud.get_todo_item(db, skip = skip, limit = limit)
    return todo_items

@app.get("/todo-items/{todo_item_id}", response_model=schemas.TodoItem)
def read_todo_item(todo_item_id: int, db: Session = Depends(get_db)):
    db_todo_item = crud.get_todo_item(db, todo_item_id=todo_item_id)
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return db_todo_item


@app.put("/todo-items/{todo_item_id}", response_model=schemas.TodoItem)
def update_todo_item(todo_item_id: int, todo_item: schemas.TodoItemCreate, db: Session = Depends(get_db)):
    return crud.update_todo_item(db=db, todo_item_id=todo_item_id, todo_item=todo_item)

@app.delete("/todo-items/{todo_item_id}", response_model=schemas.TodoItem)
def delete_todo_item(todo_item_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo_item(db=db, todo_item_id=todo_item_id)