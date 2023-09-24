import os
import sys

# Add the parent directory of blog to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi import FastAPI
import  models
from database import engine, get_db

from routers import blog, user, authentication, todo


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(todo.router)

# def get_db():
#     db = sessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()   

# @app.get('/bloglist',response_model=List[schemas.ShowBlog], tags=['blogs'])
# def allBlogs(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

# @app.post('/createblog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
# def createBlog(request:schemas.Blog, db: Session = Depends(get_db)):
#     new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

# @app.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['blogs'])
# def blog(id:int,responce : Response, db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).filter(models.Blog.id==id).first()
#     # if not blogs:
#     #     responce.status_code = status.HTTP_404_NOT_FOUND
#     #     return {'details':f"Blog with the id {id} is not available"}
#     if not blogs:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        
#     return blogs

# @app.delete('/removeblog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
# def delblog(id:int, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id==id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
#     blog.delete(synchronize_session=False)
#     db.commit()
#     return 'Blog deleted successfully'

# @app.put('/updateblog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
# def updateBlog(id:int,request : schemas.Blog, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id==id)
#     # blog = db.query(models.Blog).filter(models.Blog.id==id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')
#     # blog.update(request)
#     blog.update({models.Blog.title:request.title, models.Blog.body:request.body})
#     db.commit()
#     return 'updated successfully'



# @app.post('/createuser', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['users'])
# def createUser(request:schemas.User, db: Session = Depends(get_db)):

#     new_user = models.User(name=request.name, email= request.email, password = Hash.bcrypt(request.password))
#     # new_user = models.User(request)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get('/user/{id}', response_model=schemas.ShowBlogUser, tags=['users'])
# def user(id:int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=' User Not found')
#     return user