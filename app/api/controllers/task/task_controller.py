from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.services.task_services.task_services import TaskService
from app.api.schemas.TaskSchemas import TaskSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.dataBases.postgresDb import get_db
from app.api.schemas.TaskSchemas import TaskCreateSchema

router = APIRouter()

@router.get("/tasks", response_model=List[TaskSchema])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    
    try:
        tasks = await task_service.get_all_tasks()
        if not tasks:
            raise HTTPException(status_code=404, detail="No se encontraron tareas.")
        return tasks  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las tareas: {str(e)}")
    
    
@router.post("/tasks", response_model=TaskSchema)
async def create_task(task_data: TaskCreateSchema, db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    
    try:
        new_task = await task_service.insert_task(task_data)
        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la tarea: {str(e)}")
    
@router.put("/tasks/{task_id}", response_model=TaskSchema)
async def update_task(task_id: int, task_data: TaskCreateSchema, db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    
    try:
        updated_task = await task_service.update_task(task_id, task_data)
        
        if not updated_task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        return updated_task 
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la tarea: {str(e)}")
    
@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    
    try:
        deleted_task = await task_service.delete_task(task_id)
        
        if not deleted_task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        return "deleted_task"  
        
    except Exception as e:
       
        raise HTTPException(status_code=500, detail=f"Error al eliminar la tarea: {str(e)}")