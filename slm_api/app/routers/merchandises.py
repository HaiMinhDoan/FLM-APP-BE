from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.model.model import get_db
from app.repository.model_repo import MerchandiseTemplateRepository, MerchandiseRepository, PriceInfoRepository, ImageRepository
from app.model.dto import MerchandiseTemplateCreateDTO, MerchandiseCreateDTO, MerchandiseUpdateVer2DTO
from typing import List
import json
from pydantic import BaseModel, validator
from datetime import datetime


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

@router.post("/products")
def create_merchandise(merchandise_dto: MerchandiseCreateDTO, db: Session = Depends(get_db)):
    """Tạo sản phẩm mới."""
    try:
        # Chuẩn bị dữ liệu
        data_json = ""
        merchandise_template = MerchandiseTemplateRepository.get_merchandise_template_by_code(db, merchandise_dto.template_code)
        if not merchandise_template:
            raise HTTPException(status_code=404, detail="Merchandise template not found")
        if merchandise_dto.data_json:
            data_json = json.dumps(merchandise_dto.data_json)

        merchandise_data = {
            "template_id": merchandise_template.id,
            "brand_id": merchandise_dto.brand_id,
            "supplier_id": merchandise_dto.supplier_id,
            "code": merchandise_dto.code,
            "name": merchandise_dto.name,
            "data_sheet_link": merchandise_dto.data_sheet_link,
            "unit": merchandise_dto.unit,
            "description_in_contract": merchandise_dto.description_in_contract,
            "data_json": data_json,
            "description_in_quotation" :merchandise_dto.description_in_quotation
        }

        # Tạo Merchandise
        newMerchandise = MerchandiseRepository.create_merchandise(db, merchandise_data)
        if not newMerchandise:
            raise HTTPException(status_code=500, detail="Failed to create merchandise")

        # Tạo PriceInfo
        price_info = PriceInfoRepository.create_price_info(db, {
            "merchandise_id": newMerchandise.id,
            "import_price_include_vat": merchandise_dto.begin_price
        })
        if not price_info:
            raise HTTPException(status_code=500, detail="Failed to create price info")

        # Tạo danh sách hình ảnh
        images = merchandise_dto.images
        if images:
            for image in images:
                MerchandiseRepository.create_image(db, {"merchandise_id": newMerchandise.id, "link": image})

        # Commit giao dịch để lưu dữ liệu
        db.commit()

        return {"message": "Merchandise created successfully"}
    except Exception as e:
        # Rollback nếu có lỗi
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating merchandise: {str(e)}")

@router.get("/products", response_model=List[dict])
def get_merchandises(db: Session = Depends(get_db)):
    """Lấy danh sách sản phẩm."""
    list_merchandises = MerchandiseRepository.get_all_merchandises_with_prices(db)
    list_merchandises.sort(key=lambda merchandise: merchandise.id)
    list_merchandises_dict = []
    for merchandise in list_merchandises:
        merchandise_dict = merchandise.__dict__.copy()
        merchandise_dict.pop("_sa_instance_state", None)
        
        # Process price information
        price_infos_dict = []
        for price_info in merchandise.price_infos:
            price_info_dict = price_info.__dict__.copy()
            price_info_dict.pop("_sa_instance_state", None)
            price_infos_dict.append(price_info_dict)
        merchandise_dict["price_infos"] = price_infos_dict
        
        # Process template information
        template_dict = merchandise.template.__dict__.copy()
        template_dict.pop("_sa_instance_state", None)
        template_dict["structure_json"] = json.loads(template_dict["structure_json"])
        merchandise_dict["template"] = template_dict
        # Process brand information
        brand_dict = merchandise.brand.__dict__.copy()
        brand_dict.pop("_sa_instance_state", None)
        merchandise_dict["brand"] = brand_dict
        # Process supplier information
        supplier_dict = merchandise.brand.__dict__.copy()
        supplier_dict.pop("_sa_instance_state", None)
        merchandise_dict["supplier"] = supplier_dict
        # Process data_json
        merchandise_dict["data_json"] = merchandise.get_data()
        
        list_merchandises_dict.append(merchandise_dict)
    return list_merchandises_dict

@router.get("/products/detail/{id}", response_model=dict)
def get_merchandise(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin sản phẩm."""
    merchandise = MerchandiseRepository.get_merchandise_by_id_with_all(db, id)
    if not merchandise:
        raise HTTPException(status_code=404, detail="Merchandise not found")
    merchandise_dict = merchandise.__dict__.copy()
    merchandise_dict.pop("_sa_instance_state", None)
    merchandise_dict["data_json"] = merchandise.get_data()
    return merchandise_dict


@router.get("/products/with-images", response_model=List[dict])
def get_merchandises_with_images(db: Session = Depends(get_db)):
    """Lấy danh sách sản phẩm."""
    list_merchandises = MerchandiseRepository.get_all_merchandises_with_prices_and_images(db)
    list_merchandises.sort(key=lambda merchandise: merchandise.id)
    list_merchandises_dict = []
    for merchandise in list_merchandises:
        merchandise_dict = merchandise.__dict__.copy()
        
        
        # Process price information
        price_infos_dict = []
        for price_info in merchandise.price_infos:
            price_info_dict = price_info.__dict__.copy()
            price_info_dict.pop("_sa_instance_state", None)
            price_infos_dict.append(price_info_dict)
        merchandise_dict["price_infos"] = price_infos_dict
        
        # Process template information
        template_dict = merchandise.template.__dict__.copy()
        template_dict.pop("_sa_instance_state", None)
        template_dict["structure_json"] = json.loads(template_dict["structure_json"])
        merchandise_dict["template"] = template_dict
        # Process brand information
        brand_dict = merchandise.brand.__dict__.copy()
        brand_dict.pop("_sa_instance_state", None)
        merchandise_dict["brand"] = brand_dict
        # Process supplier information
        supplier_dict = merchandise.brand.__dict__.copy()
        supplier_dict.pop("_sa_instance_state", None)
        merchandise_dict["supplier"] = supplier_dict
        #process images
        images_dict = []
        for image in merchandise.images:
            image_dict = image.__dict__.copy()
            image_dict.pop("_sa_instance_state", None)
            images_dict.append(image_dict)
        merchandise_dict["images"] = images_dict
        # Process data_json
        merchandise_dict["data_json"] = merchandise.get_data()
        merchandise_dict.pop("_sa_instance_state", None)
        
        list_merchandises_dict.append(merchandise_dict)
    return list_merchandises_dict

#api cập nhật sản phẩm
@router.put("/products/{id}")
def update_merchandise(id: int, merchandise_dto: MerchandiseUpdateVer2DTO, db: Session = Depends(get_db)):
    """Cập nhật thông tin sản phẩm."""
    try:
        # Lấy sản phẩm hiện tại
        current_merchandise = MerchandiseRepository.get_merchandise_by_id(db, id)
        if not current_merchandise:
            raise HTTPException(status_code=404, detail="Merchandise not found")

        # Cập nhật thông tin sản phẩm
        data_json = ""
        if merchandise_dto.data_json:
            data_json = json.dumps(merchandise_dto.data_json)
        merchandise_data = {
            "name": merchandise_dto.name,
            "data_sheet_link": merchandise_dto.data_sheet_link,
            "unit": merchandise_dto.unit,
            "description_in_contract": merchandise_dto.description_in_contract,
            "data_json": data_json,
            "description_in_quotation" :merchandise_dto.description_in_quotation,
            "active": merchandise_dto.active,
        }

        # Cập nhật sản phẩm
        updated_merchandise = MerchandiseRepository.update_merchandise(db, id, merchandise_data)
        if not updated_merchandise:
            raise HTTPException(status_code=500, detail="Failed to update merchandise")

        # # Cập nhật danh sách hình ảnh
        # images = merchandise_dto.images
        # if images:
        #     # Xóa tất cả hình ảnh hiện tại
        #     MerchandiseRepository.delete_all_images(db, id)
        #     for image in images:
        #         MerchandiseRepository.create_image(db, {"merchandise_id": id, "link": image})

        # Commit giao dịch để lưu dữ liệu
        db.commit()

        return {"message": "Merchandise updated successfully"}
    except Exception as e:
        # Rollback nếu có lỗi
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating merchandise: {str(e)}")
    
    
    
# DTOs for price and image operations
class PriceAddDTO(BaseModel):
    merchandise_id: int
    import_price_include_vat: float

    @validator('import_price_include_vat')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price cannot be negative')
        return v

class ImageAddDTO(BaseModel):
    merchandise_id: int
    link: str

    @validator('link')
    def validate_link(cls, v):
        if not v or not v.strip():
            raise ValueError('Image link cannot be empty')
        return v

class ImagesAddDTO(BaseModel):
    merchandise_id: int
    links: List[str]

    @validator('links')
    def validate_links(cls, v):
        if not v:
            raise ValueError('Image links cannot be empty')
        for link in v:
            if not link or not link.strip():
                raise ValueError('Image link cannot be empty')
        return v

# API Endpoints
@router.post("/products/{id}/price", status_code=status.HTTP_201_CREATED)
def add_price(id: int, dto: PriceAddDTO, db: Session = Depends(get_db)):
    """Add a new price to a product/merchandise."""
    try:
        # Check if merchandise exists
        merchandise = MerchandiseRepository.get_merchandise_by_id(db, id)
        if not merchandise:
            raise HTTPException(status_code=404, detail="Merchandise not found")

        # Create price info
        price_data = {
            "merchandise_id": id,
            "import_price_include_vat": dto.import_price_include_vat,
        }

        price = MerchandiseRepository.create_price_info(db, price_data)
        if not price:
            raise HTTPException(status_code=500, detail="Failed to add price")

        # Commit transaction
        db.commit()

        return {"message": "Price added successfully", "price_id": price.id}
    except Exception as e:
        # Rollback on error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding price: {str(e)}")


@router.post("/products/{id}/image", status_code=status.HTTP_201_CREATED)
def add_image(id: int, dto: ImageAddDTO, db: Session = Depends(get_db)):
    """Add a new image to a product/merchandise."""
    try:
        # Check if merchandise exists
        merchandise = MerchandiseRepository.get_merchandise_by_id(db, id)
        if not merchandise:
            raise HTTPException(status_code=404, detail="Merchandise not found")

        # Create image
        image_data = {
            "merchandise_id": id,
            "link": dto.link
        }

        image = MerchandiseRepository.create_image(db, image_data)
        if not image:
            raise HTTPException(status_code=500, detail="Failed to add image")

        # Commit transaction
        db.commit()

        return {"message": "Image added successfully", "image_id": image.id}
    except Exception as e:
        # Rollback on error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding image: {str(e)}")


@router.post("/products/{id}/images", status_code=status.HTTP_201_CREATED)
def add_multiple_images(id: int, dto: ImagesAddDTO, db: Session = Depends(get_db)):
    """Add multiple images to a product/merchandise."""
    try:
        # Check if merchandise exists
        merchandise = MerchandiseRepository.get_merchandise_by_id(db, id)
        if not merchandise:
            raise HTTPException(status_code=404, detail="Merchandise not found")

        # Create images
        image_ids = []
        for link in dto.links:
            image_data = {
                "merchandise_id": id,
                "link": link
            }

            image = MerchandiseRepository.create_image(db, image_data)
            if not image:
                raise HTTPException(status_code=500, detail="Failed to add some images")
            image_ids.append(image.id)

        # Commit transaction
        db.commit()

        return {"message": f"{len(image_ids)} images added successfully", "image_ids": image_ids}
    except Exception as e:
        # Rollback on error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding images: {str(e)}")


@router.get("/products/{id}/prices")
def get_product_prices(id: int, db: Session = Depends(get_db)):
    """Get all prices for a specific product."""
    try:
        # Check if merchandise exists
        merchandise = MerchandiseRepository.get_merchandise_by_id(db, id)
        if not merchandise:
            raise HTTPException(status_code=404, detail="Merchandise not found")

        # Get prices
        prices = MerchandiseRepository.get_prices_by_merchandise_id(db, id)
        
        # Format result
        result = []
        for price in prices:
            result.append({
                "id": price.id,
                "merchandise_id": price.merchandise_id,
                "import_price_include_vat": price.import_price_include_vat,
                "created_at": price.created_at
            })
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting prices: {str(e)}")


@router.get("/products/{id}/images")
def get_product_images(id: int, db: Session = Depends(get_db)):
    """Get all images for a specific product."""
    try:
        # Check if merchandise exists
        merchandise = MerchandiseRepository.get_merchandise_by_id(db, id)
        if not merchandise:
            raise HTTPException(status_code=404, detail="Merchandise not found")

        # Get images
        images = MerchandiseRepository.get_images_by_merchandise_id(db, id)
        
        # Format result
        result = []
        for image in images:
            result.append({
                "id": image.id,
                "merchandise_id": image.merchandise_id,
                "link": image.link
            })
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting images: {str(e)}")