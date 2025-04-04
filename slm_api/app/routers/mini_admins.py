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
        potential_customer_exist_dict = potential_customer_exist.__dict__.copy()
        potential_customer_exist_dict.pop('_sa_instance_state', None)
        return {"exist": True, "potential_customer": potential_customer_exist_dict}
    else:
        return {"exist": False}
    

@router.get("/mini_admins/potential-customer/check-exist-by-code/{code}", response_model=dict)
def  check_exist_potential_customer_by_code(code: str, db: Session = Depends(get_db)):
    """Kiểm tra xem khách hàng tiềm năng đã tồn tại hay chưa bằng mã giả định."""
    potential_customer_exist = PotentialCustomerRepository.get_one_potential_customers_by_assumed_code(db= db, code=code)
    if potential_customer_exist:
        potential_customer_exist_dict = potential_customer_exist.__dict__.copy()
        potential_customer_exist_dict.pop('_sa_instance_state', None)
        return {"exist": True, "potential_customer": potential_customer_exist_dict}
    else:
        return {"exist": False}
    
@router.post("/mini_admins/add-new-pre-quote", response_model=dict)
def create_pre_quote(pre_quote_create_data: PreQuoteCreateDTO, db: Session = Depends(get_db)):
    """Tạo báo giá khảo sát hoặc báo giá khảo sát cho khách hàng tiềm năng."""
    try:
        # Bắt đầu giao dịch
        with db.begin():
            # Kiểm tra khách hàng tiềm năng đã tồn tại hay chưa
            old_potential_customer = PotentialCustomerRepository.get_potential_customer_by_assumed_or_phone(
                db=db,
                phone=pre_quote_create_data.phone,
                assumed_code=pre_quote_create_data.assumed_code
            )

            # Nếu khách hàng tiềm năng chưa tồn tại, tạo mới
            if not old_potential_customer:
                new_potential_customer = PotentialCustomerRepository.create_potential_customer(
                    db=db,
                    potential_customer_data={
                        "agent_id": pre_quote_create_data.agent_id,
                        "name": pre_quote_create_data.customer_name,
                        "phone": pre_quote_create_data.phone,
                        "assumed_code": pre_quote_create_data.assumed_code,
                        "description": pre_quote_create_data.description,
                        "address": pre_quote_create_data.address,
                        "province": pre_quote_create_data.province,
                        "district": pre_quote_create_data.district,
                        "ward": pre_quote_create_data.ward,
                    }
                )
                potential_customer_id = new_potential_customer.id
            else:
                potential_customer_id = old_potential_customer.id

            # Tạo báo giá khảo sát (PreQuote)
            new_pre_quote = PreQuoteRepository.create_pre_quote(
                db=db,
                pre_quote_data={
                    "code": pre_quote_create_data.code,
                    "name": pre_quote_create_data.name,
                    "description": pre_quote_create_data.description,
                    "created_at": datetime.now(),
                    "total_price": pre_quote_create_data.total_price,
                    "installation_type": pre_quote_create_data.installation_type,
                    "kind": pre_quote_create_data.kind,
                    "status": pre_quote_create_data.status,
                    "potential_customer_id": potential_customer_id,
                    "agent_id": pre_quote_create_data.agent_id,
                }
            )
            if not new_pre_quote:
                raise HTTPException(status_code=404, detail="Create pre quote failed")

            # Tạo danh sách PreQuoteMerchandise
            for pre_quote_merchandise in pre_quote_create_data.list_pre_quote_merchandise:
                PreQuoteMerchandiseRepository.create_pre_quote_merchandise(
                    db=db,
                    pre_quote_merchandise_data={
                        "pre_quote_id": new_pre_quote.id,
                        "merchandise_id": pre_quote_merchandise.merchandise_id,
                        "quantity": pre_quote_merchandise.quantity,
                        "price": pre_quote_merchandise.price,
                    }
                )

        # Nếu không có lỗi, trả về kết quả thành công
        return {"message": "Pre quote created successfully"}
    except HTTPException as http_exc:
        # Trả về lỗi HTTPException nếu có
        raise http_exc
    except Exception as e:
        # Xử lý lỗi không mong muốn
        print("Error occurred while creating pre quote:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")