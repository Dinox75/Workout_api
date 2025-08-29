from fastapi import FastAPI
from routes import atletas
from fastapi_pagination import add_pagination

app = FastAPI()

app.include_router(atletas.router)
add_pagination(app)

@app.get("/")
def root():
    return {"message": "API Workout API funcionando!"}
