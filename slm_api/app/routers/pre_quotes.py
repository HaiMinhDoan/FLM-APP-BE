import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.model import get_db
from app.repository.model_repo import PreQuoteRepository, PreQuoteMerchandiseRepository, CustomerRepository, UserRepository
from app.model.dto import PreQuoteCreateDTO, PreQuoteMerchandiseCreateDTO

from typing import List




router = APIRouter()

@router.get("/pre_quote/get_one/{id}", response_model=dict)
def get_pre_quote(id: int, db: Session = Depends(get_db)):
    print('id', id)
    """Lấy thông tin combo."""
    combo = PreQuoteRepository.get_pre_quote_by_id(db, id)
    if not combo:
        raise HTTPException(status_code=404, detail="Combo not found")
    combo_dict = combo.__dict__.copy()
    combo_dict["pre_quote_merchandises"] = []
    for pre_quote_merchandise in combo.pre_quote_merchandises:
        pre_quote_merchandise_dict = pre_quote_merchandise.__dict__.copy()
        merchandise_dict = pre_quote_merchandise.merchandise.__dict__.copy()
        merchandise_dict.pop("_sa_instance_state", None)
        merchandise_dict["data_json"] = json.loads(merchandise_dict["data_json"])
        pre_quote_merchandise_dict["merchandise"] = merchandise_dict
        pre_quote_merchandise_dict["merchandise"].pop("_sa_instance_state", None)
        pre_quote_merchandise_dict.pop("_sa_instance_state", None)
        combo_dict["pre_quote_merchandises"].append(pre_quote_merchandise_dict)
    if(combo.customer):
        combo_dict["customer"] = combo.customer.__dict__.copy()
        combo_dict["customer"].pop("_sa_instance_state", None)
    combo_dict.pop("_sa_instance_state", None)
    return combo_dict

@router.post("/pre_quote", response_model=dict)
def create_pre_quote(pre_quote_data: PreQuoteCreateDTO, db: Session = Depends(get_db)):
    """Tạo combo mới."""
    total_price = 0
    if pre_quote_data.customer_id == None and pre_quote_data.kind != "combo":
        customer = CustomerRepository.create_customer(db, {"name": pre_quote_data.customer_name,
                                                            "address": pre_quote_data.customer_address,
                                                            "code": pre_quote_data.customer_code,
                                                            "user_id": pre_quote_data.sale_id,
                                                            "phone": pre_quote_data.customer_phone,
                                                            "email": pre_quote_data.customer_email})
        pre_quote_data.customer_id = customer.id
    newCombo = PreQuoteRepository.create_pre_quote(db, pre_quote_data={"customer_id": pre_quote_data.customer_id,
                                                                        "code": pre_quote_data.code,
                                                                        "name": pre_quote_data.name,
                                                                        "status": pre_quote_data.status,
                                                                        "installation_type": pre_quote_data.installation_type,
                                                                        "total_price": 0.0,
                                                                        "kind": pre_quote_data.kind,
                                                                        "description": pre_quote_data.description})
    if not newCombo:
        raise HTTPException(status_code=404, detail="Create combo failed")
    for pre_quote_merchandise in pre_quote_data.list_pre_quote_merchandise:
        total_price += pre_quote_merchandise.price * pre_quote_merchandise.quantity*(100+pre_quote_merchandise.gm_price)/100
        PreQuoteMerchandiseRepository.create_pre_quote_merchandise(db, {"pre_quote_id": newCombo.id, 
                                                                        "merchandise_id": pre_quote_merchandise.merchandise_id, 
                                                                        "quantity": pre_quote_merchandise.quantity, 
                                                                        "price": pre_quote_merchandise.price})
    if pre_quote_data.total_price != None and pre_quote_data.total_price != 0.0:
        total_price = pre_quote_data.total_price
    PreQuoteRepository.update_pre_quote(db, newCombo.id, {"total_price": total_price})
    if pre_quote_data.kind == "contract_quote":
        customer = CustomerRepository.get_customer_by_id(db, newCombo.customer_id)
        user = UserRepository.get_user_by_id(db, customer.user_id)
        UserRepository.update_user(db,customer.user_id,{"total_commission":user.total_commission + total_price*user.commission_rate/100})
        if user.parent_id != None:
            parent = UserRepository.get_user_by_id(db, user.parent_id)
            UserRepository.update_user(db,user.parent_id,{"total_commission":parent.total_commission + total_price/100})
    return {"message": "Combo created successfully"}

@router.get("/pre_quote/combo", response_model=List[dict])
def get_all_combo(db: Session = Depends(get_db)):
    """Lấy danh sách combo."""
    combos = PreQuoteRepository.get_pre_quotes_by_kind(db, "combo")
    combos_dict = []
    for combo in combos:
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
    return combos_dict

@router.get("/pre_quote/combo/installation_type/{installation_type}", response_model=List[dict])
def get_combo_by_installation_type(installation_type: str, db: Session = Depends(get_db)):
    """Lấy danh sách combo theo loại lắp đặt."""
    combos = PreQuoteRepository.get_pre_quotes_by_kind_and_installation_type(db, "combo", installation_type)
    combos_dict = []

    for combo in combos:
        combo_dict = {
            "id": combo.id,
            "code": combo.code,
            "name": combo.name,
            "description": combo.description,
            "total_price": combo.total_price,
            "kind": combo.kind,
            "status": combo.status,
            "customer": {
                "id": combo.customer.id,
                "name": combo.customer.name,
                "address": combo.customer.address,
                "phone": combo.customer.phone,
                "email": combo.customer.email,
            } if combo.customer else None,
            "pre_quote_merchandises": [
                {
                    "id": pre_quote_merchandise.id,
                    "quantity": pre_quote_merchandise.quantity,
                    "price": pre_quote_merchandise.price,
                    "merchandise": {
                        "id": pre_quote_merchandise.merchandise.id,
                        "name": pre_quote_merchandise.merchandise.name,
                        "data_json": json.loads(pre_quote_merchandise.merchandise.data_json)
                    }
                } for pre_quote_merchandise in combo.pre_quote_merchandises
            ]
        }
        combos_dict.append(combo_dict)
    return combos_dict
