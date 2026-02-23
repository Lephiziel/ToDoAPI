from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..dependencies import get_current_user
from ..models import Todo
from ..database import get_db
from typing import List
from ..schemas.todo import TodoResponse, TodoCreate, TodoUpdate

todo_router = APIRouter()

@todo_router.get("/", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
async def get_all_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user =  Depends(get_current_user)):
    user_todos = db.query(Todo).filter(Todo.owner_id == current_user.id).offset(skip).limit(limit).all()

    return user_todos

@todo_router.get("/{todo_id}", response_model=TodoResponse)
async def get_the_todo(
    todo_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)):
    user_todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if user_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if user_todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")

    return user_todo

@todo_router.post("/", response_model=TodoResponse)
async def create_the_todo(
    todo: TodoCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)):
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        owner_id=current_user.id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@todo_router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def update_the_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    search_todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if search_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo is not found")

    if search_todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this todo")
    
    for i, v in todo_update.dict(exclude_unset=True).items():
        setattr(search_todo, i, v)

    db.commit()
    db.refresh(search_todo)

    return search_todo

@todo_router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_the_todo(
    todo_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)):
    search_todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if search_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    if current_user.id != search_todo.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this todo")

    db.delete(search_todo)
    db.commit()

    return {"message": "Todo deleted successfully"}
    
