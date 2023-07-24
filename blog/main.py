from fastapi import FastAPI, Depends, status, Response, HTTPException
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
    

@app.post('/blog', status_code=status.HTTP_201_CREATED)
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
def blog(id:int,responce : Response, db: Session = Depends(get_db)):
    blogs = db.query(models.Bolg).filter(models.Bolg.id==id).first()
    # if not blogs:
    #     responce.status_code = status.HTTP_404_NOT_FOUND
    #     return {'details':f"Blog with the id {id} is not available"}
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        
    return blogs

@app.delete('/blogdlt/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delblog(id:int,responce : Response, db: Session = Depends(get_db)):
    db.query(models.Bolg).filter(models.Bolg.id==id).delete(synchronize_session=False)
    db.commit()
    return 'Blog deleted successfully'