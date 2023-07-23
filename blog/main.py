from fastapi import FastAPI, Depends
from . import schemas, models
from .database import engine, sessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@app.post('/blog')
def createBlog(request:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Bolg(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/bloglist')
def allBlogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Bolg).all()
    return blogs

@app.get('/blog/{id}')
def blog(id:int, db: Session = Depends(get_db)):
    blogs = db.query(models.Bolg).filter(models.Bolg.id==id).first()
    return blogs