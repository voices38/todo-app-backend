from fastapi import FastAPI


app = FastAPI()


@app.get('/hello-world')

def read_base_page():
    return {'message': 'Hello, world'}