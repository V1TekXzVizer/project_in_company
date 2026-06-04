from pydantic import BaseModel
from typing import Optional, List
from datetime import date 

class PlaceBase(BaseModel):
    external_id: str
    notes: Optional[str] = None
    visited: bool = False

class PlaceCreate(BaseModel):
    external_id: str

class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None

class PlaceResponse(PlaceBase):
    id: int
    created_at: date
    updated_at: date
    
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None

class ProjectCreate(ProjectBase):
    places: Optional[list[PlaceCreate]] = []

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None

class ProjectResponse(ProjectBase):
    id: int
    completed: bool 
    places: List[PlaceResponse] = []
    
    class Config:
        from_attributes = True