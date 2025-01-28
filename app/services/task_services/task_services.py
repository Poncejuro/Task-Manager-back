from app.dataBases.postgresDb import SessionLocal
from app.models.task import Task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.api.schemas.TaskSchemas import TaskCreateSchema

class TaskService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_tasks(self):
        try:
            result = await self.db_session.execute(select(Task))
            tasks = result.scalars().all()  
            return tasks  
        except SQLAlchemyError as e:
            raise Exception(f"Error al ejecutar la consulta: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado: {str(e)}")
        
        
    async def insert_task(self, task_data: TaskCreateSchema):
        try:
            new_task = Task(
                title=task_data.title,
                description=task_data.description
            )
            
            self.db_session.add(new_task)
            await self.db_session.commit() 
            
            return new_task  
            
        except SQLAlchemyError as e:
            await self.db_session.rollback()  
            raise Exception(f"Error al insertar la tarea: {str(e)}")
        except Exception as e:
            await self.db_session.rollback()  
            raise Exception(f"Error inesperado: {str(e)}")
        
    async def update_task(self, task_id: int, task_data: TaskCreateSchema):
        try:
            task_to_update = await self.db_session.get(Task, task_id)
            
            if not task_to_update:
                raise Exception(f"Tarea con ID {task_id} no encontrada")

            task_to_update.title = task_data.title
            task_to_update.description = task_data.description
            
            self.db_session.add(task_to_update)
            await self.db_session.commit()

            return task_to_update  
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise Exception(f"Error al actualizar la tarea: {str(e)}")
        except Exception as e:
            await self.db_session.rollback()
            raise Exception(f"Error inesperado: {str(e)}")

    async def delete_task(self, task_id: int):
        try:
            task_to_delete = await self.db_session.get(Task, task_id)

            if not task_to_delete:
                raise Exception(f"Tarea con ID {task_id} no encontrada")

            await self.db_session.delete(task_to_delete)
            await self.db_session.commit()

            return task_to_delete 

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise Exception(f"Error al eliminar la tarea: {str(e)}")

        except Exception as e:
            await self.db_session.rollback()
            raise Exception(f"Error inesperado: {str(e)}")