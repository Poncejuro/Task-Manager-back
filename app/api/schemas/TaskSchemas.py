from pydantic import BaseModel

class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    status: str

    class Config:
        orm_mode = True
        
class TaskCreateSchema(BaseModel):
    title: str
    description: str
    status: str
    
    class Config:
        orm_mode = True 
    