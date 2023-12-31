from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
import schemas, models, database
from blog import oauth2



router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)

@router.get('/list',response_model=List[schemas.ShowBlogUser])
def allBlogs(db: Session = Depends(database.get_db),current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.BlogBase)
def createBlog(request:schemas.Blog, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):

    new_blog = models.Blog(title=request.title, body=request.body, user_id=current_user.get('id'))
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/{id}', response_model=schemas.ShowBlogUser)
def blog(id:int, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        
    return blogs

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delblog(id:int, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    
    db.query(models.Todo).filter(and_(models.Todo.id==id, models.Todo.user_id== current_user.get('id'))).delete(synchronize_session=False)
    
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Blog deleted successfully'

@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id:int,request : schemas.Blog, db: Session = Depends(database.get_db), current_user:schemas.ShowUser = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    # blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    # blog.update(request)
    blog.update({models.Blog.title:request.title, models.Blog.body:request.body})
    db.commit()
    return 'updated successfully'
