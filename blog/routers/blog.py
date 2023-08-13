from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
import schemas, models, database



router = APIRouter()




@router.get('/bloglist',response_model=List[schemas.BlogBase], tags=['blogs'])
def allBlogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
@router.post('/createblog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def createBlog(request:schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['blogs'])
def blog(id:int, db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id==id).first()
    # if not blogs:
    #     responce.status_code = status.HTTP_404_NOT_FOUND
    #     return {'details':f"Blog with the id {id} is not available"}
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        
    return blogs

@router.delete('/removeblog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delblog(id:int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Blog deleted successfully'

@router.put('/updateblog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def updateBlog(id:int,request : schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    # blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    # blog.update(request)
    blog.update({models.Blog.title:request.title, models.Blog.body:request.body})
    db.commit()
    return 'updated successfully'
