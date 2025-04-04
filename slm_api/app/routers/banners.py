from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.model.model import get_db, User, Base, Role, LoginHistory, Notification, Commission, PotentialCustomer
from app.repository.model_repo import UserRepository, PotentialCustomerRepository, BannerRepository
from app.model.dto import UserCreateDTO, UserUpdateDTO, PotentialCustomerCreateDTO
from typing import List
from sqlalchemy import func
from datetime import datetime
import traceback

router = APIRouter()

# Quản lý Banner
@router.get("/banners", response_model=List[dict])
def get_banners(db: Session = Depends(get_db)):
    """Lấy danh sách banner."""
    banners = BannerRepository.get_all_banners(db)
    banners_dict = []
    for banner in banners:
        banner_dict = banner.__dict__.copy()
        banner_images_dict = []
        for image in banner.banner_images:
            image_dict = image.__dict__.copy()
            image_dict.pop("_sa_instance_state", None)
            banner_images_dict.append(image_dict)
        banner_dict["banner_images"] = banner_images_dict
        banner_dict.pop("_sa_instance_state", None)
        banners_dict.append(banner_dict)
    return banners_dict