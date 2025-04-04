from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.model import get_db, Sector
from app.repository.model_repo import SectorRepository, ContentCategoryRepository, ContentRepository, PreQuoteRepository
from app.repository.model_repo import ContentRepository
from app.model.dto import SectorCreateDTO
from typing import List
import json, traceback


router = APIRouter()
@router.get("/sector", response_model=List[dict])
def get_sectors(db: Session = Depends(get_db)):
    """Lấy danh sách Sector."""
    try:
        # Lấy tất cả các Sector từ repository
        sectors = SectorRepository.get_all_sectors(db)
        sectors_dict = []

        for sector in sectors:
            # Lấy danh sách combo theo sector code
            combos = PreQuoteRepository.get_pre_quotes_by_kind_and_sector(db=db, kind="combo", sector=sector.code)
            contents = ContentRepository.get_all_contents_by_sector(db, sector=sector.code)
            sector_dict = sector.__dict__.copy()

            # Xử lý danh sách combo
            combos_dict = []
            contents_dict = []
            for combo in combos:
                # Sắp xếp pre_quote_merchandises theo thứ tự tăng dần id
                combo.pre_quote_merchandises = sorted(combo.pre_quote_merchandises, key=lambda x: x.id)
                combo_dict = combo.__dict__.copy()

                # Xử lý danh sách pre_quote_merchandises
                combo_dict["pre_quote_merchandises"] = []
                for pre_quote_merchandise in combo.pre_quote_merchandises:
                    pre_quote_merchandise_dict = pre_quote_merchandise.__dict__.copy()
                    pre_quote_merchandise_dict["price_on_gm"] = pre_quote_merchandise_dict["price"]/(1-pre_quote_merchandise_dict["gm"]/100)
                    merchandise_dict = pre_quote_merchandise.merchandise.__dict__.copy()
                    merchandise_dict.pop("_sa_instance_state", None)
                    merchandise_dict["data_json"] = json.loads(merchandise_dict["data_json"])
                    images = pre_quote_merchandise.merchandise.images
                    images_dict = []
                    for image in images:
                        image_dict = image.__dict__.copy()
                        image_dict.pop("_sa_instance_state", None)
                        images_dict.append(image_dict)
                    merchandise_dict["images"] = images_dict.copy()
                    pre_quote_merchandise.merchandise.template.structure_json = None
                    merchandise_template_dict = pre_quote_merchandise.merchandise.template.__dict__.copy()
                    merchandise_template_dict.pop("_sa_instance_state", None)
                    merchandise_dict["template"] = merchandise_template_dict
                    pre_quote_merchandise_dict["merchandise"] = merchandise_dict
                    pre_quote_merchandise_dict["merchandise"].pop("_sa_instance_state", None)
                    pre_quote_merchandise_dict.pop("_sa_instance_state", None)
                    combo_dict["pre_quote_merchandises"].append(pre_quote_merchandise_dict)
                
                grouped_merchandises = {}
                for pre_quote_merchandise in combo_dict["pre_quote_merchandises"]:
                    template_id = pre_quote_merchandise["merchandise"]["template"]["id"]
                    if template_id not in grouped_merchandises:
                        grouped_merchandises[template_id] = {
                            "template": pre_quote_merchandise["merchandise"]["template"],
                            "pre_quote_merchandises": []
                        }
                    grouped_merchandises[template_id]["pre_quote_merchandises"].append(pre_quote_merchandise)

                combo_dict["grouped_merchandises"] = list(grouped_merchandises.values())
                #sắp xếp combo_dict["grouped_merchandises"] them template.id
                combo_dict["grouped_merchandises"] = sorted(
                    combo_dict["grouped_merchandises"], key=lambda x: x["template"]["id"]
                )
                combo_dict["pre_quote_merchandises"] =[]
                combo_dict.pop("_sa_instance_state", None)
                combos_dict.append(combo_dict)
            for content in contents:
                content_dict = content.__dict__.copy()
                content_dict["category"] = content.category.__dict__.copy()
                content_dict["category"].pop("_sa_instance_state", None)
                content_dict["media_contents"] = []
                for media_content in content.media_contents:
                    media_content_dict = media_content.__dict__.copy()
                    media_content_dict.pop("_sa_instance_state", None)
                    content_dict["media_contents"].append(media_content_dict)
                content_dict.pop("_sa_instance_state", None)
                contents_dict.append(content_dict)
            # Gắn danh sách combo vào sector
            sector_dict["list_combos"] = combos_dict
            sector_dict["list_contents"] = contents_dict
            sector_dict.pop("_sa_instance_state", None)

            # Thêm sector vào danh sách kết quả
            sectors_dict.append(sector_dict)

        return sectors_dict

    except Exception as e:
        print("Error occurred while fetching sectors:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching sectors: {str(e)}")

@router.post("/sector", response_model=dict)
def create_sector(sector_data: SectorCreateDTO, db: Session = Depends(get_db)):
    """Tạo Sector mới."""
    newSector = SectorRepository.create_sector(db, sector_data=sector_data.dict())
    if not newSector:
        raise HTTPException(status_code=404, detail="Create sector failed")
    return {"message": "Sector created successfully"}

@router.get("/sector/{id}", response_model=dict)
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