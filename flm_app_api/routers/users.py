from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from flm_app_api.model.model import get_db
from flm_app_api.repository.model_repo import UserRepository, LoginHistoryRepository, NotificationRepository, Role
from flm_app_api.model.dto import UserCreateDTO, UserUpdateDTO
from typing import List

router = APIRouter()


# Quản lý Người dùng

@router.get("/users", response_model=List[dict])
def get_users(db: Session = Depends(get_db)):
    """Lấy danh sách người dùng."""
    return UserRepository.get_all_users(db)

@router.post("/users", response_model=dict)
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

@router.get("/users/{id}", response_model=dict)
def get_user(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin người dùng."""
    user = UserRepository.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{id}", response_model=dict)
def update_user(id: int, user_data: UserUpdateDTO, db: Session = Depends(get_db)):
    """Cập nhật thông tin người dùng."""
    updated_user = UserRepository.update_user(db, id, user_data.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    """Xóa người dùng."""
    if not UserRepository.delete_user(db, id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.put("/users/{id}/{status}")
def update_user_status(id: int, status: str, db: Session = Depends(get_db)):
    """Cập nhật trạng thái người dùng."""
    updated_user = UserRepository.update_user(db, id, {"status": status})
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.put("/users/{id}/password")
def update_user_password(id: int, new_password: dict, db: Session = Depends(get_db)):
    """Đổi mật khẩu người dùng."""
    updated_user = UserRepository.update_user(db, id, new_password)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.get("/users/me", response_model=dict)
def get_current_user(db: Session = Depends(get_db)):
    """Lấy thông tin người dùng hiện tại."""
    # Giả sử user_id được lấy từ token (cần tích hợp xác thực)
    user_id = 1  # Thay bằng logic lấy user_id từ token
    user = UserRepository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/me")
def update_current_user(user_data: UserUpdateDTO, db: Session = Depends(get_db)):
    """Cập nhật thông tin cá nhân."""
    user_id = 1  # Thay bằng logic lấy user_id từ token
    updated_user = UserRepository.update_user(db, user_id, user_data.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.post("/users/import")
def import_users(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Import người dùng từ file."""
    # Logic xử lý file import (ví dụ: đọc file CSV và thêm người dùng)
    return {"message": "Import users successfully"}

@router.get("/users/export")
def export_users(db: Session = Depends(get_db)):
    """Export danh sách người dùng."""
    # Logic export danh sách người dùng (ví dụ: tạo file CSV)
    return {"message": "Export users successfully"}

# Quản lý Hoạt động Người dùng

@router.get("/users/{id}/activities")
def get_user_activities(id: int, db: Session = Depends(get_db)):
    """Lấy lịch sử hoạt động."""
    # Logic lấy lịch sử hoạt động (nếu có bảng riêng cho hoạt động)
    return {"message": "User activities"}

@router.get("/users/{id}/login-history", response_model=List[dict])
def get_login_history(id: int, db: Session = Depends(get_db)):
    """Lấy lịch sử đăng nhập."""
    return LoginHistoryRepository.get_login_histories_by_user_id(db, id)

@router.get("/users/online")
def get_online_users(db: Session = Depends(get_db)):
    """Lấy danh sách người dùng đang online."""
    # Logic xác định người dùng online (ví dụ: dựa trên token hoặc trạng thái)
    return {"message": "Online users"}

@router.get("/users/{id}/notifications", response_model=List[dict])
def get_user_notifications(id: int, db: Session = Depends(get_db)):
    """Lấy thông báo của người dùng."""
    return NotificationRepository.get_notifications_by_user_id(db, id)

@router.put("/users/{id}/notifications/{notificationId}/read")
def mark_notification_as_read(id: int, notificationId: int, db: Session = Depends(get_db)):
    """Đánh dấu thông báo đã đọc."""
    updated_notification = NotificationRepository.mark_notification_as_read(db, notificationId)
    if not updated_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notification