from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from flm_app_api.model.model import get_db
from flm_app_api.repository.model_repo import ComboRepository, MerchandiseTemplateRepository, SectorRepository, UserRepository, LoginHistoryRepository, NotificationRepository, ComboMerchandiseRepository, MerchandiseRepository
from flm_app_api.model.dto import ComboCreateDTO, UserCreateDTO, UserUpdateDTO, NotificationDTO, MerchandiseCreateDTO, SectorCreateDTO, MerchandiseTemplateCreateDTO
from typing import List
from flm_app_api.model.model import User, LoginHistory, Notification, Role, Base, Combo, Sector
import json

app = FastAPI()

# Quản lý Người dùng

@app.get("/api/users", response_model=List[dict])
def get_users(db: Session = Depends(get_db)):
    """Lấy danh sách người dùng."""
    return UserRepository.get_all_users(db)

@app.post("/api/users", response_model=dict)
def create_user(user_data: UserCreateDTO, db: Session = Depends(get_db)):
    """Tạo người dùng mới."""
    newUser =  UserRepository.create_user(db, user_data=user_data.dict())
    if not newUser:
        raise HTTPException(status_code=404, detail="Create user failed")
    role_id = user_data.role_id
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    list_roles = List[dict]
    list_roles.append(role)
    UserRepository.update_user(db, newUser.id, {"list_roles": list_roles})
    return {"message": "User created successfully"}

@app.get("/api/users/{id}", response_model=dict)
def get_user(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin người dùng."""
    user = UserRepository.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users/{id}", response_model=dict)
def update_user(id: int, user_data: UserUpdateDTO, db: Session = Depends(get_db)):
    """Cập nhật thông tin người dùng."""
    updated_user = UserRepository.update_user(db, id, user_data.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/api/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    """Xóa người dùng."""
    if not UserRepository.delete_user(db, id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.put("/api/users/{id}/{status}")
def update_user_status(id: int, status: str, db: Session = Depends(get_db)):
    """Cập nhật trạng thái người dùng."""
    updated_user = UserRepository.update_user(db, id, {"status": status})
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.put("/api/users/{id}/password")
def update_user_password(id: int, new_password: dict, db: Session = Depends(get_db)):
    """Đổi mật khẩu người dùng."""
    updated_user = UserRepository.update_user(db, id, new_password)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.get("/api/users/me", response_model=dict)
def get_current_user(db: Session = Depends(get_db)):
    """Lấy thông tin người dùng hiện tại."""
    # Giả sử user_id được lấy từ token (cần tích hợp xác thực)
    user_id = 1  # Thay bằng logic lấy user_id từ token
    user = UserRepository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users/me")
def update_current_user(user_data: UserUpdateDTO, db: Session = Depends(get_db)):
    """Cập nhật thông tin cá nhân."""
    user_id = 1  # Thay bằng logic lấy user_id từ token
    updated_user = UserRepository.update_user(db, user_id, user_data.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.post("/api/users/import")
def import_users(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Import người dùng từ file."""
    # Logic xử lý file import (ví dụ: đọc file CSV và thêm người dùng)
    return {"message": "Import users successfully"}

@app.get("/api/users/export")
def export_users(db: Session = Depends(get_db)):
    """Export danh sách người dùng."""
    # Logic export danh sách người dùng (ví dụ: tạo file CSV)
    return {"message": "Export users successfully"}

# Quản lý Hoạt động Người dùng

@app.get("/api/users/{id}/activities")
def get_user_activities(id: int, db: Session = Depends(get_db)):
    """Lấy lịch sử hoạt động."""
    # Logic lấy lịch sử hoạt động (nếu có bảng riêng cho hoạt động)
    return {"message": "User activities"}

@app.get("/api/users/{id}/login-history", response_model=List[dict])
def get_login_history(id: int, db: Session = Depends(get_db)):
    """Lấy lịch sử đăng nhập."""
    return LoginHistoryRepository.get_login_histories_by_user_id(db, id)

@app.get("/api/users/online")
def get_online_users(db: Session = Depends(get_db)):
    """Lấy danh sách người dùng đang online."""
    # Logic xác định người dùng online (ví dụ: dựa trên token hoặc trạng thái)
    return {"message": "Online users"}

@app.get("/api/users/{id}/notifications", response_model=List[dict])
def get_user_notifications(id: int, db: Session = Depends(get_db)):
    """Lấy thông báo của người dùng."""
    return NotificationRepository.get_notifications_by_user_id(db, id)

@app.put("/api/users/{id}/notifications/{notificationId}/read")
def mark_notification_as_read(id: int, notificationId: int, db: Session = Depends(get_db)):
    """Đánh dấu thông báo đã đọc."""
    updated_notification = NotificationRepository.mark_notification_as_read(db, notificationId)
    if not updated_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notification

# Quản lý Đại lý

@app.get("/api/agents", response_model=List[dict])
def get_agents(db: Session = Depends(get_db)):
    """Lấy danh sách đại lý."""
    return db.query(User).filter(User.role_id == 2).all()

@app.post("/api/agents", response_model=dict)
def create_agent(agent_data: dict, db: Session = Depends(get_db)):
    """Tạo đại lý mới."""
    agent_data["role_id"] = 2  # Đảm bảo role_id là 2
    agent = User(**agent_data)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@app.get("/api/agents/{id}", response_model=dict)
def get_agent(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin đại lý."""
    agent = db.query(User).filter(User.id == id, User.role_id == 2).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.put("/api/agents/{id}", response_model=dict)
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

@app.delete("/api/agents/{id}")
def delete_agent(id: int, db: Session = Depends(get_db)):
    """Xóa đại lý."""
    agent = db.query(User).filter(User.id == id, User.role_id == 2).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
    return {"message": "Agent deleted successfully"}

@app.get("/api/agents/{id}/downlines", response_model=List[dict])
def get_downlines(id: int, db: Session = Depends(get_db)):
    """Lấy danh sách đại lý cấp dưới."""
    # Giả sử có quan hệ parent_id để xác định cấp dưới
    return db.query(User).filter(User.role_id == 2, User.parent_id == id).all()

@app.get("/api/agents/{id}/commissions")
def get_commissions(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin hoa hồng."""
    # Giả sử có bảng hoa hồng liên kết với đại lý
    return {"message": f"Commission data for agent {id}"}

@app.get("/api/agents/{id}/sales")
def get_sales(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin doanh số."""
    # Giả sử có bảng doanh số liên kết với đại lý
    return {"message": f"Sales data for agent {id}"}

@app.get("/api/agents/{id}/territories")
def get_territories(id: int, db: Session = Depends(get_db)):
    """Lấy khu vực phụ trách."""
    # Giả sử có bảng khu vực liên kết với đại lý
    return {"message": f"Territories data for agent {id}"}

@app.put("/api/agents/{id}/territories")
def update_territories(id: int, territories_data: dict, db: Session = Depends(get_db)):
    """Cập nhật khu vực phụ trách."""
    # Giả sử có logic cập nhật khu vực
    return {"message": f"Territories updated for agent {id}"}







@app.get("/api/sector", response_model=List[dict])
def get_sectors(db: Session = Depends(get_db)):
    """Lấy danh sách Sector."""
    return SectorRepository.get_all_sectors(db)

@app.post("/api/sector", response_model=dict)
def create_sector(sector_data: SectorCreateDTO, db: Session = Depends(get_db)):
    """Tạo Sector mới."""
    newSector = SectorRepository.create_sector(db, sector_data=sector_data.dict())
    if not newSector:
        raise HTTPException(status_code=404, detail="Create sector failed")
    return {"message": "Sector created successfully"}

@app.get("/api/sector/{id}", response_model=dict)
def get_sector(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin Sector."""
    sector = SectorRepository.get_sector_by_id(db, id)
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")
    return sector

@app.put("/api/sector/{id}", response_model=dict)
def update_sector(id: int, sector_data: SectorCreateDTO, db: Session = Depends(get_db)):
    """Cập nhật thông tin Sector."""
    updated_sector = SectorRepository.update_sector(db, id, sector_data.dict(exclude_unset=True))
    if not updated_sector:
        raise HTTPException(status_code=404, detail="Sector not found")
    return updated_sector

@app.get("/api/merchandise-template", response_model=List[dict])
def get_merchandises_template(db: Session = Depends(get_db)):
    """Lấy danh sách loại vật tư."""
    return MerchandiseTemplateRepository.get_all_merchandise_templates(db)

@app.post("/api/merchandise-template", response_model=dict)
def create_merchandise_template(merchandise_template_data: MerchandiseTemplateCreateDTO, db: Session = Depends(get_db)):
    data = merchandise_template_data.dict()
    data["structure_json"] = json.dumps(data["structure_json"])
    """Tạo loại vật tư mới."""
    newMerchandise =  MerchandiseTemplateRepository.create_merchandise_template(db, merchandise_template_data=data)
    if not newMerchandise:
        raise HTTPException(status_code=404, detail="Create merchandise failed")
    return {"message": "Merchandise created successfully"}

@app.get("/api/merchandise-template/{id}", response_model=dict)
def get_merchandise_template(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin sản phẩm."""    
    merchandise = MerchandiseTemplateRepository.get_merchandise_template_by_id(db, id)
    if not merchandise:
        raise HTTPException(status_code=404, detail="Merchandise not found")
    merchandise["structure_json"] = json.loads(merchandise["structure_json"])
    return merchandise

@app.post("/api/products/add")
def create_merchandise(merchandise_dto: MerchandiseCreateDTO,db: Session = Depends(get_db)):
    """Tạo sản phẩm mới."""
    data_json = ""
    if merchandise_dto.data_json:
        data_json = json.dumps(merchandise_dto.data_json)
    merchandise_data = {
        "template_id": merchandise_dto.template_id,
        "brand_id": merchandise_dto.brand_id,
        "supplier_id": merchandise_dto.supplier_id,
        "code": merchandise_dto.code,
        "name": merchandise_dto.name,
        "data_sheet_link": merchandise_dto.data_sheet_link,
        "unit": merchandise_dto.unit,
        "description_in_contract": merchandise_dto.description_in_contract,
        "data_json": data_json
    }
    newMerchandise =  MerchandiseRepository.create_merchandise(db, merchandise_data)
    if not newMerchandise:
        raise HTTPException(status_code=404, detail="Create merchandise failed")
    return {"message": "Merchandise created successfully"}

@app.get("/api/products", response_model=List[dict])
def get_merchandises(db: Session = Depends(get_db)):
    """Lấy danh sách sản phẩm."""
    list_merchandises = MerchandiseRepository.get_all_merchandises(db)
    for merchandise in list_merchandises:
        merchandise["data_json"] = json.loads(merchandise["data_json"])
    return MerchandiseRepository.get_all_merchandises_with_prices(db)

@app.get("/api/products/{id}", response_model=dict)
def get_merchandise(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin sản phẩm."""
    merchandise = MerchandiseRepository.get_merchandise_by_id_with_prices(db, id)
    if not merchandise:
        raise HTTPException(status_code=404, detail="Merchandise not found")
    merchandise["data_json"] = json.loads(merchandise["data_json"])
    return merchandise

@app.post("/api/combo", response_model=dict)
def create_combo(combo_data: ComboCreateDTO, db: Session = Depends(get_db)):
    """Tạo combo mới."""
    total_price = 0
    newCombo = ComboRepository.create_combo(db, combo_data=combo_data.dict())
    if not newCombo:
        raise HTTPException(status_code=404, detail="Create combo failed")
    for combo_merchandise in combo_data.list_combo_merchandise:
        total_price += combo_merchandise["price"]
        ComboMerchandiseRepository.create_combo_merchandise(db, {"combo_id": newCombo.id, "merchandise_id": combo_merchandise["merchandise_id"], "quantity": combo_merchandise["quantity"], "price": combo_merchandise["price"]})
    ComboRepository.update_combo(db, newCombo.id, {"total_price": total_price})
    return {"message": "Combo created successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)