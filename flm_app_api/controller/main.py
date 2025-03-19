from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from flm_app_api.model.model import get_db
from flm_app_api.repository.model_repo import UserRepository, LoginHistoryRepository, NotificationRepository
from flm_app_api.model.dto import UserCreateDTO, UserUpdateDTO, NotificationDTO
from typing import List

app = FastAPI()

# Quản lý Người dùng

@app.get("/api/users", response_model=List[dict])
def get_users(db: Session = Depends(get_db)):
    """Lấy danh sách người dùng."""
    return UserRepository.get_all_users(db)

@app.post("/api/users", response_model=dict)
def create_user(user_data: UserCreateDTO, db: Session = Depends(get_db)):
    """Tạo người dùng mới."""
    return UserRepository.create_user(db, user_data.dict())

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

@app.put("/api/users/{id}/status")
def update_user_status(id: int, status: str, db: Session = Depends(get_db)):
    """Cập nhật trạng thái người dùng."""
    updated_user = UserRepository.update_user(db, id, {"status": status})
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.put("/api/users/{id}/password")
def update_user_password(id: int, new_password: str, db: Session = Depends(get_db)):
    """Đổi mật khẩu người dùng."""
    updated_user = UserRepository.update_user(db, id, {"password": new_password})
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)