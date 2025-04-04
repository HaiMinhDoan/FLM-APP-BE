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