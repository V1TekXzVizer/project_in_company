from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db 
from ..utils.artic_client import check_place_exists

router = APIRouter()

@router.post("/{project_id}/places", response_model=schemas.PlaceResponse)
async def add_place_to_project(
    project_id: int,
    place_create: schemas.PlaceCreate,
    db: Session = Depends(get_db)
):
    
    exists = await check_place_exists(place_create.external_id)
    if not exists:
        raise HTTPException(status_code=404, detail="Place not found")
    return crud.add_place_to_project(db, project_id, place_create.external_id)

@router.get("/{project_id}/places", response_model=List[schemas.PlaceResponse])
def list_project_places(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.get_project_places(db, project_id)

@router.get("/{project_id}/places/{place_id}", response_model=schemas.PlaceResponse)
def get_place_in_project(project_id: int, place_id: int, db: Session = Depends(get_db)):
    place = crud.get_place(db, place_id)
    if not place or place.project_id != project_id:
        raise HTTPException(status_code=404, detail="Place not found in this project")
    return place

@router.put("/{project_id}/places/{place_id}", response_model=schemas.PlaceResponse)
def update_place_in_project(
    project_id: int, 
    place_id: int, 
    place_update: schemas.PlaceUpdate, 
    db: Session = Depends(get_db)
):
    
    place = crud.get_place(db, place_id)
    if not place or place.project_id != project_id:
        raise HTTPException(status_code=404, detail="Place not found in this project")
    return crud.update_place(db, place_id, place_update)
    