from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
import schemas, models, database
from blog import oauth2



router = APIRouter(
    prefix='/todo',
    tags=['Todos']
)

@router.get('/list',response_model=List[schemas.showTodo])
def allBlogs(db: Session = Depends(database.get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Todo).all()
    return blogs

@router.post('/create', status_code=status.HTTP_201_CREATED)
def createBlog(request:schemas.Todo, db: Session = Depends(database.get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    
    new_blog = models.Todo(title=request.title, description=request.description,priority = request.priority, user_id=current_user.get('id'))
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/{id}', response_model=schemas.showTodo)
def blog(id:int, db: Session = Depends(database.get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Todo).filter(models.Todo.id==id).first()
    # if not blogs:
    #     responce.status_code = status.HTTP_404_NOT_FOUND
    #     return {'details':f"Blog with the id {id} is not available"}
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        
    return blogs

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delblog(id:int, db: Session = Depends(database.get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Todo).filter(models.Todo.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Blog deleted successfully'

@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id:int,request : schemas.Todo, db: Session = Depends(database.get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Todo).filter(models.Todo.id==id)
    # blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    # blog.update(request)
    blog.update({models.Todo.title:request.title, models.Todo.description:request.description, models.Todo.priority:request.priority})
    db.commit()
    return 'updated successfully'
