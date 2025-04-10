from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.model.model import get_db, User, Base, Role, LoginHistory, Notification, Commission, PotentialCustomer
from app.repository.model_repo import UserRepository, PotentialCustomerRepository
from app.repository.model_repo import PreQuoteRepository, PreQuoteMerchandiseRepository, PotentialCustomerRepository, CustomerRepository
from app.model.model import PreQuote, PreQuoteMerchandise, PotentialCustomer
from app.model.dto import UserCreateDTO, UserUpdateDTO, PotentialCustomerCreateDTO, PreQuoteCreateDTO
from typing import List
from sqlalchemy import func
from datetime import datetime
import traceback
import json

router = APIRouter()

#Chức năng cho mini_admin
@router.get("/mini_admins/potential-customer/check-exist-by-phone/{phone}", response_model=dict)
def check_exist_potential_customer_by_phone(phone: str, db: Session = Depends(get_db)):
    """Kiểm tra xem khách hàng tiềm năng đã tồn tại hay chưa bằng số điện thoại."""
    potential_customer_exist = PotentialCustomerRepository.get_potential_customer_by_phone(
        db= db, 
        potential_customer_phone=phone)
    user = UserRepository.get_user_by_phone(
        db=db, phone=phone)
    if user:
        user_dict = user.__dict__.copy()
        user_dict["role"] = user.role.__dict__.copy()
        user_dict["role"].pop("_sa_instance_state", None)
        
        combos = PreQuoteRepository.get_contract_quote_by_buyer_id_and_sector(db=db,buyer_id=user.id,sector="SLM")
        combos_dict = []
        for combo in combos:
            #sắp xếp pre_quote_merchandises theo thứ tự tăng dần id
            combo.pre_quote_merchandises = sorted(combo.pre_quote_merchandises, key=lambda x: x.id)
            combo_dict = combo.__dict__.copy()
            combo_dict["pre_quote_merchandises"] = []
            for pre_quote_merchandise in combo.pre_quote_merchandises:
                pre_quote_merchandise_dict = pre_quote_merchandise.__dict__.copy()
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
                pre_quote_merchandise_dict["merchandise"] = merchandise_dict
                pre_quote_merchandise_dict["merchandise"].pop("_sa_instance_state", None)
                pre_quote_merchandise_dict.pop("_sa_instance_state", None)
                # pre_quote_merchandise_dict["gm_price"] = pre_quote_merchandise_dict["gm_price"] if pre_quote_merchandise_dict["gm_price"] else 0
                combo_dict["pre_quote_merchandises"].append(pre_quote_merchandise_dict)
            if(combo.customer):
                combo_dict["customer"] = combo.customer.__dict__.copy()
                combo_dict["customer"].pop("_sa_instance_state", None)
            
            combo_dict.pop("_sa_instance_state", None)
            combos_dict.append(combo_dict)
        
        user_dict["combos"] = combos_dict.copy()
        user_dict["combos"].sort(key=lambda x: x["created_at"], reverse=True)
        user_dict.pop("_sa_instance_state", None)
        customer = CustomerRepository.get_customer_by_phone(db=db, phone=phone)
        customer_dict = None
        if customer:
            customer_dict = customer.__dict__.copy()
            customer_dict.pop("_sa_instance_state", None)
        
        return {"exist": True, "user": user_dict, "customer": customer_dict}
    if potential_customer_exist:
        old_pre_quotes = PreQuoteRepository.get_pre_quote_by_potential_customer_id(
            db=db, potential_customer_id=potential_customer_exist.id)
        old_pre_quotes_dict = []
        for pre_quote in old_pre_quotes:
            pre_quote_dict = pre_quote.__dict__.copy()
            pre_quote_merchandises_dict = []
            for pre_quote_merchandise in pre_quote.pre_quote_merchandises:
                pre_quote_merchandise_dict = pre_quote_merchandise.__dict__.copy()
                merchandise_dict = pre_quote_merchandise.merchandise.__dict__.copy()
                template_dict = pre_quote_merchandise.merchandise.template.__dict__.copy()
                template_dict.pop('_sa_instance_state', None)
                merchandise_dict['template'] = template_dict
                merchandise_dict.pop('_sa_instance_state', None)
                pre_quote_merchandise_dict['merchandise'] = merchandise_dict
                pre_quote_merchandise_dict.pop('_sa_instance_state', None)
                pre_quote_merchandises_dict.append(pre_quote_merchandise_dict)
            pre_quote_dict['pre_quote_merchandises'] = pre_quote_merchandises_dict
            pre_quote_dict.pop('_sa_instance_state', None)
            old_pre_quotes_dict.append(pre_quote_dict)
        potential_customer_exist_dict = potential_customer_exist.__dict__.copy()
        potential_customer_exist_dict['old_pre_quotes'] = old_pre_quotes_dict
        potential_customer_exist_dict.pop('_sa_instance_state', None)
        return {"exist": True, "potential_customer": potential_customer_exist_dict}
    else:
        return {"exist": False}
    

@router.get("/mini_admins/potential-customer/check-exist-by-code/{code}", response_model=dict)
def  check_exist_potential_customer_by_code(code: str, db: Session = Depends(get_db)):
    """Kiểm tra xem khách hàng tiềm năng đã tồn tại hay chưa bằng mã giả định."""
    potential_customer_exist = PotentialCustomerRepository.get_one_potential_customers_by_assumed_code(db= db, code=code)
    if potential_customer_exist:
        old_pre_quotes = PreQuoteRepository.get_pre_quote_by_potential_customer_id(
            db=db, potential_customer_id=potential_customer_exist.id)
        old_pre_quotes_dict = []
        for pre_quote in old_pre_quotes:
            pre_quote_dict = pre_quote.__dict__.copy()
            pre_quote_merchandises_dict = []
            for pre_quote_merchandise in pre_quote.pre_quote_merchandises:
                pre_quote_merchandise_dict = pre_quote_merchandise.__dict__.copy()
                merchandise_dict = pre_quote_merchandise.merchandise.__dict__.copy()
                template_dict = pre_quote_merchandise.merchandise.template.__dict__.copy()
                template_dict.pop('_sa_instance_state', None)
                merchandise_dict['template'] = template_dict
                merchandise_dict.pop('_sa_instance_state', None)
                pre_quote_merchandise_dict['merchandise'] = merchandise_dict
                pre_quote_merchandise_dict.pop('_sa_instance_state', None)
                pre_quote_merchandises_dict.append(pre_quote_merchandise_dict)
            pre_quote_dict['pre_quote_merchandises'] = pre_quote_merchandises_dict
            pre_quote_dict.pop('_sa_instance_state', None)
            old_pre_quotes_dict.append(pre_quote_dict)
        potential_customer_exist_dict = potential_customer_exist.__dict__.copy()
        potential_customer_exist_dict['old_pre_quotes'] = old_pre_quotes_dict
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