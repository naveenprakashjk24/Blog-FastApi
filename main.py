from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

class Blog(BaseModel):
    title : str
    body : str
    published : Optional[bool]
    

@app.get('/')
def index():
    return {'data': 'blog list'}

@app.get('/blog/unpublished')
def unpublishedblog():
    return {'data':'All unpublished blog'}

@app.get('/blog/{id}')
def showBlog(id:int):
    #fetch blog withh id
    return {'data':f'{id} is published'}


@app.post('/blog')
def blog_create(blog: Blog):
    return {'date':f'Blog is created with title as {blog.title}'}

# if __name__ == "__main__":
#     uvicorn.run(app, host='localhost', port=4041 )