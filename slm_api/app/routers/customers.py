import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.model import get_db, Customer
from app.repository.model_repo import CustomerRepository
from typing import List
from app.model.dto import CustomerCreateDTO

router = APIRouter()

@router.get("/customer", response_model=List[dict])
def get_customers(db: Session = Depends(get_db)):
    """Lấy danh sách khách hàng."""
    customers = CustomerRepository.get_all_customers(db)
    customers_dict = []
    for customer in customers:
        customer_dict = customer.__dict__.copy()
        customer_dict.pop("_sa_instance_state", None)
        customers_dict.append(customer_dict)
    return customers_dict

@router.post("/customer", response_model=dict)
def create_customer(customer_data: CustomerCreateDTO, db: Session = Depends(get_db)):
    """Tạo khách hàng mới."""
    newCustomer = CustomerRepository.create_customer(db, customer_data=customer_data.dict())
    if not newCustomer:
        raise HTTPException(status_code=404, detail="Create customer failed")
    return {"message": "Customer created successfully"}