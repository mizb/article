from sqlalchemy.orm import Session

from app.models.task import Task
from app.scheduler import restart_scheduler
from app.schemas.response import success
from app.schemas.task import TaskForm


def list_task(db: Session):
    task_list = db.query(Task).all()
    return success(task_list)


def add_task(db: Session, task_form: TaskForm):
    task = Task(**task_form.model_dump(exclude={"id"}))
    db.add(task)
    db.flush()
    restart_scheduler()
    return success(task)


def update_task(db: Session, task_form: TaskForm):
    task = db.query(Task).filter_by(id=task_form.id).first()
    if task:
        task.task_name = task_form.task_name
        task.task_func = task_form.task_func
        task.task_args = task_form.task_args
        task.task_cron = task_form.task_cron
        task.enable = task_form.enable
        db.flush()
        restart_scheduler()
    return success(task)


def delete_task(db: Session, task_id):
    task = db.get(Task, task_id)
    if task:
        db.delete(task)
        restart_scheduler()
    return success()
