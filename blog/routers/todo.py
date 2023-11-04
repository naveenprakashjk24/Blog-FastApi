from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_, text
import schemas, models, database
from blog import oauth2



router = APIRouter(
    prefix='/todo',
    tags=['Todos']
)

@router.get('/list',response_model=List[schemas.showTodo])
def allTodo(db: Session = Depends(database.get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    todos = db.query(models.Todo).all()
    return todos

@router.post('/create', status_code=status.HTTP_201_CREATED)
def createTodo(request:schemas.Todo, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):
    
    new_todo = models.Todo(title=request.title, description=request.description,priority = request.priority, user_id=current_user.get('id'))
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get('/{id}', response_model=schemas.showTodo)
def todo(id:int, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id==id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        
    return todo

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delTodo(id:int, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    
    # todo_model = db.query(models.Todo).filter(models.Todo.id == id).filter(models.Todo.owner == current_user.get('id'))
    todo_model = db.query(models.Todo).filter(and_(models.Todo.id==id, models.Todo.user_id== current_user.get('id'))).first()
    print(todo_model)
    
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'Todo not found or No Todo for this user')
    
    db.query(models.Todo).filter(models.Todo.id == id).delete(synchronize_session=False)
    db.commit()
    return 'Todo deleted successfully'

@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateTodo(id:int,request : schemas.UpdateTodo, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id==id)
    if not todo.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    todo.update({models.Todo.title:request.title, models.Todo.description:request.description, models.Todo.priority:request.priority, models.Todo.completed : request.completed})
    db.commit()
    return 'updated successfully'
