from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.model import get_db
from app.repository.model_repo import MerchandiseTemplateRepository, MerchandiseRepository
from app.model.dto import MerchandiseTemplateCreateDTO, MerchandiseCreateDTO
from typing import List
import json



router = APIRouter()


@router.get("/merchandise-templates", response_model=List[dict])
def get_merchandises_template(db: Session = Depends(get_db)):
    """Lấy danh sách loại vật tư."""
    merchandise_templates = MerchandiseTemplateRepository.get_all_merchandise_templates(db)
    merchandise_templates_dict = []
    for merchandise_template in merchandise_templates:
        merchandise_template_dict = merchandise_template.__dict__.copy()
        merchandise_template_dict["structure_json"] = merchandise_template.get_data_structure()
        merchandise_template_dict.pop("_sa_instance_state", None)
        merchandise_templates_dict.append(merchandise_template_dict)
    return merchandise_templates_dict

@router.post("/merchandise-templates", response_model=dict)
def create_merchandise_template(merchandise_template_data: MerchandiseTemplateCreateDTO, db: Session = Depends(get_db)):
    data = merchandise_template_data.dict()
    data["structure_json"] = json.dumps(data["structure_json"])
    """Tạo loại vật tư mới."""
    newMerchandise =  MerchandiseTemplateRepository.create_merchandise_template(db, merchandise_template_data=data)
    if not newMerchandise:
        raise HTTPException(status_code=404, detail="Create merchandise failed")
    return {"message": "Merchandise created successfully"}

@router.get("/merchandise-templates/{id}", response_model=dict)
def get_merchandise_template(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin sản phẩm."""    
    merchandise = MerchandiseTemplateRepository.get_merchandise_template_by_id(db, id)
    if not merchandise:
        raise HTTPException(status_code=404, detail="Merchandise not found")
    merchandise["structure_json"] = json.loads(merchandise["structure_json"])
    return merchandise

@router.post("/products/add")
def create_merchandise(merchandise_dto: MerchandiseCreateDTO,db: Session = Depends(get_db)):
    """Tạo sản phẩm mới."""
    data_json = ""
    if merchandise_dto.data_json:
        data_json = json.dumps(merchandise_dto.data_json)
    merchandise_data = {
        "template_id": merchandise_dto.template_id,
        "brand_id": merchandise_dto.brand_id,
        "supplier_id": merchandise_dto.supplier_id,
        "code": merchandise_dto.code,
        "name": merchandise_dto.name,
        "data_sheet_link": merchandise_dto.data_sheet_link,
        "unit": merchandise_dto.unit,
        "description_in_contract": merchandise_dto.description_in_contract,
        "data_json": data_json
    }
    newMerchandise =  MerchandiseRepository.create_merchandise(db, merchandise_data)
    if not newMerchandise:
        raise HTTPException(status_code=404, detail="Create merchandise failed")
    return {"message": "Merchandise created successfully"}

@router.get("/products", response_model=List[dict])
def get_merchandises(db: Session = Depends(get_db)):
    """Lấy danh sách sản phẩm."""
    list_merchandises = MerchandiseRepository.get_all_merchandises_with_prices(db)
    list_merchandises_dict = []
    for merchandise in list_merchandises:
        merchandise_dict = merchandise.__dict__.copy()
        merchandise_dict.pop("_sa_instance_state", None)
        merchandise_dict["data_json"] = merchandise.get_data()
        list_merchandises_dict.append(merchandise_dict)
    return list_merchandises_dict

@router.get("/products/{id}", response_model=dict)
def get_merchandise(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin sản phẩm."""
    merchandise = MerchandiseRepository.get_merchandise_by_id_with_all(db, id)
    if not merchandise:
        raise HTTPException(status_code=404, detail="Merchandise not found")
    merchandise_dict = merchandise.__dict__.copy()
    merchandise_dict.pop("_sa_instance_state", None)
    merchandise_dict["data_json"] = merchandise.get_data()
    return merchandise_dict