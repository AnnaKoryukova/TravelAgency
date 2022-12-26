from fastapi import FastAPI
from API.routes import router
from db.database import Base, engine

app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)
