from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.model.model import get_db, User, Base, Role, LoginHistory, Notification, Commission, PotentialCustomer
from app.repository.model_repo import UserRepository, PotentialCustomerRepository
from app.repository.model_repo import PreQuoteRepository, PreQuoteMerchandiseRepository, PotentialCustomerRepository
from app.model.model import PreQuote, PreQuoteMerchandise, PotentialCustomer
from app.model.dto import UserCreateDTO, UserUpdateDTO, PotentialCustomerCreateDTO, PreQuoteCreateDTO
from typing import List
from sqlalchemy import func
from datetime import datetime
import traceback

router = APIRouter()

#Chức năng cho mini_admin
@router.get("/mini_admins/potential-customer/check-exist-by-phone/{phone}", response_model=dict)
def check_exist_potential_customer_by_phone(phone: str, db: Session = Depends(get_db)):
    """Kiểm tra xem khách hàng tiềm năng đã tồn tại hay chưa bằng số điện thoại."""
    potential_customer_exist = PotentialCustomerRepository.get_potential_customer_by_phone(
        db= db, 
        potential_customer_phone=phone)
    if potential_customer_exist:
        return {"exist": True, "potential_customer": potential_customer_exist}
    else:
        return {"exist": False}
    

@router.get("/mini_admins/potential-customer/check-exist-by-code/{code}", response_model=dict)
def  check_exist_potential_customer_by_code(code: str, db: Session = Depends(get_db)):
    """Kiểm tra xem khách hàng tiềm năng đã tồn tại hay chưa bằng mã giả định."""
    potential_customer_exist = PotentialCustomerRepository.get_one_potential_customers_by_assumed_code(db= db, code=code)
    if potential_customer_exist:
        return {"exist": True, "potential_customer": potential_customer_exist}
    else:
        return {"exist": False}
    
@router.post("/mini_admins/add-new-pre-quote",response_model=dict)
def create_pre_quote(pre_quote_create_data:PreQuoteCreateDTO,db: Session = Depends(get_db)):
    """Tạo báo giá khảo sát hoặc báo giá khảo sát cho khách hàng tiềm năng"""
    
    old_potential_customer = PotentialCustomerRepository.get_potential_customer_by_assumed_or_phone(
        db=db, 
        phone=pre_quote_create_data.phone,
        assumed_code=pre_quote_create_data.assumed_code)
    if not old_potential_customer:
        new_potential_customer = PotentialCustomerRepository.create_potential_customer(
            db=db, 
            potential_customer_data={
                "agent_id": pre_quote_create_data.agent_id,
                "name": pre_quote_create_data.name,
                "phone": pre_quote_create_data.phone,
                "assumed_code": pre_quote_create_data.assumed_code,
                "description": pre_quote_create_data.description,
                "address": pre_quote_create_data.address,
                "province": pre_quote_create_data.province,
                "district": pre_quote_create_data.district,
                "ward": pre_quote_create_data.ward,
                "name": pre_quote_create_data.customer_name,
            })