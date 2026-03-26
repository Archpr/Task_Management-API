from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import auth
from app.routers import auth, projects
from app.routers import tasks
from app.routers import comments
from app.routers import attachments
from app.routers import reminders

app = FastAPI(
    title="Task Management System",
    description="A task management API built with FastAPI and PostgreSQL",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(projects.router) 
app.include_router(tasks.router)
app.include_router(comments.router)
app.include_router(attachments.router)
app.include_router(reminders.router) 

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Task Management System is running!"}


