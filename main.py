from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return "hello world"

@app.get('/about')
def about():
    return {'data':'This is Blog using Python FastApi'}