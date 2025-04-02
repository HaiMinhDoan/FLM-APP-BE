from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.model import get_db, User, Base, Role, LoginHistory, Notification, Commission
from app.repository.model_repo import UserRepository
from app.model.dto import UserCreateDTO, UserUpdateDTO
from typing import List
from sqlalchemy import func
from datetime import datetime

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
    children = UserRepository.get_user_by_parent_id(db=db, parent_id=id)
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