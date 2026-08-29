from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.errors import register_exception_handlers, task_not_found
from app.models import Task
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Task Manager",
    description="A simple REST API to create, view, update, and delete student tasks.",
    version="1.0.0",
)
register_exception_handlers(app)


def get_task_or_404(task_id: int, db: Session) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise task_not_found(task_id)
    return task


@app.get("/")
def root():
    return {"message": "Student Task Manager API. Visit /docs for Swagger UI."}


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status.value,
        priority=task.priority.value,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return get_task_or_404(task_id, db)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = get_task_or_404(task_id, db)

    update_data = task_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    for field, value in update_data.items():
        if hasattr(value, "value"):
            value = value.value
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_or_404(task_id, db)

    db.delete(task)
    db.commit()
    return {"message": f"Task with id {task_id} deleted successfully"}
