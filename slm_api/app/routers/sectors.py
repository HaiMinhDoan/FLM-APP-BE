from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.model import get_db, Sector
from app.repository.model_repo import SectorRepository
from app.model.dto import SectorCreateDTO
from typing import List


router = APIRouter()
@router.get("/api/sector", response_model=List[dict])
def get_sectors(db: Session = Depends(get_db)):
    """Lấy danh sách Sector."""
    return SectorRepository.get_all_sectors(db)

@router.post("/api/sector", response_model=dict)
def create_sector(sector_data: SectorCreateDTO, db: Session = Depends(get_db)):
    """Tạo Sector mới."""
    newSector = SectorRepository.create_sector(db, sector_data=sector_data.dict())
    if not newSector:
        raise HTTPException(status_code=404, detail="Create sector failed")
    return {"message": "Sector created successfully"}

@router.get("/api/sector/{id}", response_model=dict)
def get_sector(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin Sector."""
    sector = SectorRepository.get_sector_by_id(db, id)
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")
    return sector

@router.put("/api/sector/{id}", response_model=dict)
def update_sector(id: int, sector_data: SectorCreateDTO, db: Session = Depends(get_db)):
    """Cập nhật thông tin Sector."""
    updated_sector = SectorRepository.update_sector(db, id, sector_data.dict(exclude_unset=True))
    if not updated_sector:
        raise HTTPException(status_code=404, detail="Sector not found")
    return updated_sector