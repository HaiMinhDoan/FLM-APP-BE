from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.model.model import get_db, User, Base, Role, LoginHistory, Notification, Commission, PotentialCustomer
from app.repository.model_repo import UserRepository, PotentialCustomerRepository, PreQuoteRepository, CustomerRepository
from app.model.dto import UserCreateDTO, UserUpdateDTO, PotentialCustomerCreateDTO
from typing import List
from sqlalchemy import func
from datetime import datetime
import traceback

router = APIRouter()

# Quản lý Đại lý

@router.get("/agents", response_model=List[dict])
def get_agents(db: Session = Depends(get_db)):
    """Lấy danh sách đại lý."""
    return db.query(User).filter(User.role_id == 2).all()

@router.post("/agents", response_model=dict)
def create_agent(agent_data: dict, db: Session = Depends(get_db)):
    """Tạo đại lý mới."""
    agent_data["role_id"] = 2  # Đảm bảo role_id là 2
    agent = User(**agent_data)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.get("/agents/{id}", response_model=dict)
def get_agent(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin đại lý."""
    agent = db.query(User).filter(User.id == id, User.role_id == 2).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/agents/{id}", response_model=dict)
def update_agent(id: int, agent_data: dict, db: Session = Depends(get_db)):
    """Cập nhật thông tin đại lý."""
    agent = db.query(User).filter(User.id == id, User.role_id == 2).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    for key, value in agent_data.items():
        setattr(agent, key, value)
    db.commit()
    db.refresh(agent)
    return agent

@router.delete("/agents/{id}")
def delete_agent(id: int, db: Session = Depends(get_db)):
    """Xóa đại lý."""
    agent = db.query(User).filter(User.id == id, User.role_id == 2).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
    return {"message": "Agent deleted successfully"}

@router.get("/agents/{id}/downlines", response_model=List[dict])
def get_downlines(id: int, db: Session = Depends(get_db)):
    """Lấy danh sách đại lý cấp dưới."""
    children = UserRepository.get_agent_by_parent_id(db=db, parent_id=id)
    #Sắp xếp children bằng tổng hoa hồng kiếm được trong tháng này 
    # Giả sử có bảng Commission với các cột: user_id, amount, created_at
    current_month = datetime.now().month
    current_year = datetime.now().year

    children = sorted(
        children,
        key=lambda child: db.query(func.sum(Commission.money))
        .filter(
            Commission.seller == child.id,
            func.extract('month', Commission.created_at) == current_month,
            func.extract('year', Commission.created_at) == current_year
        )
        .scalar() or 0,
        reverse=True
    )
    #chuyển toàn bộ children thành danh sách dict
    children_dict = []
    total_turnover = 0
    for child in children:
        child_turnover = 0
                
        child_dict = child.__dict__.copy()
        commissions = child.commissions
        commissions_dict = []
        #hoàn thiện code để có commissions_dict
        for commission in commissions:
            commission_dict = commission.__dict__.copy()
            commission_dict.pop('_sa_instance_state', None)
            commissions_dict.append(commission_dict)
            print(commission.contract_id)
            contract_temp = PreQuoteRepository.get_pre_quote_by_id_simple(db=db,pre_quote_id=commission.contract_id)
            if contract_temp:
                child_turnover += contract_temp.total_price
                total_turnover += contract_temp.total_price
        child_dict['commissions'] = commissions_dict
        child_dict['child_turnover'] = child_turnover
        child_dict.pop('_sa_instance_state', None)
        children_dict.append(child_dict)
    # Giả sử có quan hệ parent_id để xác định cấp dưới
    return children_dict

@router.get("/agents/{id}/old-customer", response_model=List[dict])
def get_old_customers(id: int, db: Session = Depends(get_db)):
    """Lấy danh sách đại lý cấp dưới."""
    children = UserRepository.get_customer_account_by_parent_id(db=db, parent_id=id)
    #Sắp xếp children bằng tổng hoa hồng kiếm được trong tháng này 
    # Giả sử có bảng Commission với các cột: user_id, amount, created_at
    current_month = datetime.now().month
    current_year = datetime.now().year

    children = sorted(
        children,
        key=lambda child: db.query(func.sum(Commission.money))
        .filter(
            Commission.seller == child.id,
            func.extract('month', Commission.created_at) == current_month,
            func.extract('year', Commission.created_at) == current_year
        )
        .scalar() or 0,
        reverse=True
    )
    #chuyển toàn bộ children thành danh sách dict
    children_dict = []
    for child in children:
        child_dict = child.__dict__.copy()
        commissions = child.commissions
        commissions_dict = []
        #hoàn thiện code để có commissions_dict
        for commission in commissions:
            commission_dict = commission.__dict__.copy()
            commission_dict.pop('_sa_instance_state', None)
            commissions_dict.append(commission_dict)
        child_dict['commissions'] = commissions_dict
        child_dict.pop('_sa_instance_state', None)
        children_dict.append(child_dict)
    # Giả sử có quan hệ parent_id để xác định cấp dưới
    return children_dict

@router.get("/agents/{id}/commissions")
def get_commissions(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin hoa hồng."""
    # Giả sử có bảng hoa hồng liên kết với đại lý
    return {"message": f"Commission data for agent {id}"}

@router.get("/agents/{id}/sales")
def get_sales(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin doanh số."""
    # Giả sử có bảng doanh số liên kết với đại lý
    return {"message": f"Sales data for agent {id}"}

@router.get("/agents/{id}/territories")
def get_territories(id: int, db: Session = Depends(get_db)):
    """Lấy khu vực phụ trách."""
    # Giả sử có bảng khu vực liên kết với đại lý
    return {"message": f"Territories data for agent {id}"}

@router.put("/agents/{id}/territories")
def update_territories(id: int, territories_data: dict, db: Session = Depends(get_db)):
    """Cập nhật khu vực phụ trách."""
    # Giả sử có logic cập nhật khu vực
    return {"message": f"Territories updated for agent {id}"}


@router.get("/agents/check-remaining-adding-customer/{agent_id}", response_model=dict)
def check_remaining_adding_customer(agent_id:int,db: Session = Depends(get_db)):
    """Kiểm tra có còn lượt thêm khách hàng tiềm năng hay không"""
    potential_customers = PotentialCustomerRepository.get_all_potential_customers_by_agent_id(db=db, agent_id=agent_id)
    result = 20 - len(potential_customers)
    if result < 0:
        result = 0
    return {"remaining":result}

@router.post("/agents/create-new-potential-customer", response_model=dict)
def create_new_potential_customer(potential_customer_data: PotentialCustomerCreateDTO, db: Session = Depends(get_db)):
    """Tạo khách hàng tiềm năng mới."""
    try:
        # Bắt đầu giao dịch
        with db.begin():
            # Kiểm tra khách hàng tiềm năng đã tồn tại hay chưa
            check_exist_customer = PotentialCustomerRepository.get_potential_customer_by_phone(
                db=db, potential_customer_phone=potential_customer_data.phone
            )
            if check_exist_customer:
                raise HTTPException(status_code=400, detail="Potential customer already exists")

            # Tạo khách hàng tiềm năng mới
            new_potential_customer = PotentialCustomerRepository.create_potential_customer(
                db=db,
                potential_customer_data={
                    "agent_id": potential_customer_data.agent_id,
                    "name": potential_customer_data.name,
                    "phone": potential_customer_data.phone,
                    "gender": potential_customer_data.gender,
                    "email": potential_customer_data.email,
                    "address": potential_customer_data.address,
                    "province": potential_customer_data.province,
                    "district": potential_customer_data.district,
                    "ward": potential_customer_data.ward,
                    "interested_in_combo_id": potential_customer_data.interested_in_combo_id,
                    "description": potential_customer_data.description
                },
            )

            if not new_potential_customer:
                raise HTTPException(status_code=500, detail="Failed to create new potential customer")

        # Nếu không có lỗi, trả về kết quả thành công
        return {"message": "success"}
    except HTTPException as http_exc:
        # Trả về lỗi HTTPException nếu có
        raise http_exc
    except Exception as e:
        # Xử lý lỗi không mong muốn
        print("Error occurred while creating potential customer:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
#Lấy danh  sách khách hàng tiềm năng của đại lý
@router.get("/agents/{agent_id}/potential-customers", response_model=List[dict])
def get_potential_customers(agent_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách khách hàng tiềm năng của đại lý."""
    potential_customers = PotentialCustomerRepository.get_all_potential_customers_by_agent_id(db=db, agent_id=agent_id)
    potential_customers_dict = []
    for potential_customer in potential_customers:
        potential_customer_dict = potential_customer.__dict__.copy()
        potential_customer_dict.pop('_sa_instance_state', None)
        potential_customers_dict.append(potential_customer_dict)
    return potential_customers_dict

@router.delete("/agents/delete-potential-customers/{potential_customer_id}", response_model=dict)
def delete_potential_customer(potential_customer_id: int, db: Session = Depends(get_db)):
    """Xoá một khách hàng tiềm năng."""
    try:
        # Bắt đầu giao dịch
        with db.begin():
            # Lấy thông tin khách hàng tiềm năng
            potential_customer = PotentialCustomerRepository.get_potential_customer_by_id(
                db=db, potential_customer_id=potential_customer_id
            )
            if not potential_customer:
                raise HTTPException(status_code=404, detail="Potential customer not found")
            # Xoá khách hàng tiềm năng
            PotentialCustomerRepository.delete_potential_customer(db=db, potential_customer_id=potential_customer_id)
        # Nếu không có lỗi, trả về kết quả thành công
        return {"success": True}
    except HTTPException as http_exc:
        # Trả về lỗi HTTPException nếu có
        raise http_exc
    except Exception as e:
        # Xử lý lỗi không mong muốn
        print("Error occurred while deleting potential customer:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")