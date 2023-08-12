from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas, models
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@app.get('/bloglist',response_model=List[schemas.ShowBlog])
def allBlogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.post('/createblog', status_code=status.HTTP_201_CREATED)
def createBlog(request:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog/{id}', response_model=schemas.ShowBlog)
def blog(id:int,responce : Response, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id==id).first()
    # if not blogs:
    #     responce.status_code = status.HTTP_404_NOT_FOUND
    #     return {'details':f"Blog with the id {id} is not available"}
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        
    return blogs

@app.delete('/removeblog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delblog(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Blog deleted successfully'

@app.put('/updateblog/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id,request : schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    # blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
    # blog.update(request)
    blog.update({models.Blog.title:request.title, models.Blog.body:request.body})
    db.commit()
    return 'updated successfully'



@app.post('/createuser', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def createUser(request:schemas.User, db: Session = Depends(get_db)):

    new_user = models.User(name=request.name, email= request.email, password = Hash.bcrypt(request.password))
    # new_user = models.User(request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
