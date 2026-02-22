from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..dependencies import get_current_user
from ..schemas import Todo
from ..database import get_db
from typing import List
from ..models.todo import TodoResponse, TodoCreate, TodoUpdate

todo_router = APIRouter()

@todo_router.get("/", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
async def get_all_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user =  Depends(get_current_user)):
    user_todos = db.query(Todo).filter(owner_id == current_user.id).offset(skip).limit(limit)

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

@todo_router.put("/{todo_id}")
async def update_the_todo():
    pass
