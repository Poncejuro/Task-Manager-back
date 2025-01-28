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
