import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from flm_app_api.model.model import get_db
from flm_app_api.repository.model_repo import PreQuoteRepository, PreQuoteMerchandiseRepository
from flm_app_api.model.dto import PreQuoteCreateDTO, PreQuoteMerchandiseCreateDTO




router = APIRouter()

@router.post("/api/pre_quote", response_model=dict)
def create_pre_quote(pre_quote_data: PreQuoteCreateDTO, db: Session = Depends(get_db)):
    """Tạo combo mới."""
    total_price = 0
    newCombo = PreQuoteRepository.create_pre_quote(db, combo_data=pre_quote_data.dict())
    if not newCombo:
        raise HTTPException(status_code=404, detail="Create combo failed")
    for pre_quote_merchandise in pre_quote_data.list_pre_quote_merchandise:
        total_price += pre_quote_merchandise.price * pre_quote_merchandise.quantity
        PreQuoteMerchandiseRepository.create_pre_quote_merchandise(db, {"pre_quote_id": newCombo.id, 
                                                                        "merchandise_id": pre_quote_merchandise.merchandise_id, 
                                                                        "quantity": pre_quote_merchandise.quantity, 
                                                                        "price": pre_quote_merchandise.price})
    PreQuoteRepository.update_pre_quote(db, newCombo.id, {"total_price": total_price})
    return {"message": "Combo created successfully"}