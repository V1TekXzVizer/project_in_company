from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(
        name=project.name,
        description=project.description,
        start_date=project.start_date
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    if project.places:
        for place in project.places:
            db_place = models.Place(
                external_id=place.external_id,
                project_id=db_project.id
            )
            db.add(db_place)
        db.commit()
        db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project_update.name is not None:
        db_project.name = project_update.name
    if project_update.description is not None:
        db_project.description = project_update.description
    if project_update.start_date is not None:
        db_project.start_date = project_update.start_date
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if any(p.visited for p in db_project.places):
        raise HTTPException(status_code=400, detail="Cannot delete project with visited places")
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted successfully"}

def get_place(db: Session, place_id: int):
    return db.query(models.Place).filter(models.Place.id == place_id).first()

def get_project_places(db: Session, project_id: int):
    return db.query(models.Place).filter(models.Place.project_id == project_id).all()

def add_place_to_project(db: Session, project_id: int, external_id: str):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if len(project.places) >= 10:
        raise HTTPException(status_code=400, detail="Project cannot have more than 10 places")
    
    for p in project.places:
        if p.external_id == external_id:
            raise HTTPException(status_code=400, detail="Place already exists in this project")
    
    db_place = models.Place(
        external_id=external_id,
        project_id=project_id
    )
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

def update_place(db: Session, place_id: int, place_update: schemas.PlaceUpdate):
    db_place = get_place(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")
    if place_update.notes is not None:
        db_place.notes = place_update.notes
    if place_update.visited is not None:
        db_place.visited = place_update.visited
    db.commit()
    db.refresh(db_place)
    return db_place