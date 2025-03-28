from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.model.model import get_db, Brand
from app.repository.model_repo import BrandRepository


router = APIRouter()

@router.get("/brands", response_model=list[dict])
def get_brands(db: Session = Depends(get_db)):
    """Lấy danh sách thương hiệu."""
    brands = BrandRepository.get_all_brands(db)
    brands_dict = []
    for brand in brands:
        brand_dict = brand.__dict__.copy()
        brand_dict.pop("_sa_instance_state", None)
        brands_dict.append(brand_dict)
    return brands_dict

@router.post("/brands", response_model=dict)
def create_brand(brand_data: dict, db: Session = Depends(get_db)):
    """Tạo thương hiệu mới."""
    newBrand = BrandRepository.create_brand(db, brand_data=brand_data)
    if not newBrand:
        raise HTTPException(status_code=404, detail="Create brand failed")
    return {"message": "Brand created successfully"}

@router.get("/brands/{id}", response_model=dict)
def get_brand(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin thương hiệu."""
    brand = BrandRepository.get_brand_by_id(db, id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    brand_dict = brand.__dict__.copy()
    brand_dict.pop("_sa_instance_state", None)
    return brand_dict