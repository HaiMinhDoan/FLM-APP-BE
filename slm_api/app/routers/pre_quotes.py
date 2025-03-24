import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.model import get_db
from app.repository.model_repo import PreQuoteRepository, PreQuoteMerchandiseRepository
from app.model.dto import PreQuoteCreateDTO, PreQuoteMerchandiseCreateDTO

from typing import List




router = APIRouter()

@router.post("/pre_quote", response_model=dict)
def create_pre_quote(pre_quote_data: PreQuoteCreateDTO, db: Session = Depends(get_db)):
    """Tạo combo mới."""
    total_price = 0
    newCombo = PreQuoteRepository.create_pre_quote(db, pre_quote_data={"customer_id": pre_quote_data.customer_id,
                                                                        "code": pre_quote_data.code,
                                                                        "name": pre_quote_data.name,
                                                                        "status": pre_quote_data.status,
                                                                        "installation_type": pre_quote_data.installation_type,
                                                                        "total_price": pre_quote_data.total_price,
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
    PreQuoteRepository.update_pre_quote(db, newCombo.id, {"total_price": total_price})
    return {"message": "Combo created successfully"}

@router.get("/pre_quote/combo", response_model=List[dict])
def get_all_combo(db: Session = Depends(get_db)):
    """Lấy danh sách combo."""
    combos = PreQuoteRepository.get_pre_quotes_by_kind(db, "combo")
    combos_dict = []
    for combo in combos:
        combo_dict = combo.__dict__.copy()
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
