from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.model.model import get_db
from app.repository.model_repo import Role, TokenRepository,PreQuoteRepository
from app.repository.model_repo import UserRepository, LoginHistoryRepository, NotificationRepository, CommissionRepository
from app.model.dto import UserCreateDTO, UserUpdateDTO, UserLoginDTO
from typing import List
from datetime import datetime
import json
router = APIRouter()


# Quản lý Người dùng

@router.get("/users/sale",response_model=List[dict])
def get_users(db: Session = Depends(get_db)):
    """Lấy danh sách người dùng."""
    users_dict = []
    users = UserRepository.get_all_sales(db)
    for user in users:
        user_dict = user.__dict__.copy()
        user_dict["role"] = user.role.__dict__.copy()
        user_dict["role"].pop("_sa_instance_state", None)
        user_dict.pop("_sa_instance_state", None)
        users_dict.append(user_dict)
    return users_dict

@router.get("/users", response_model=List[dict])
def get_users(db: Session = Depends(get_db)):
    """Lấy danh sách người dùng."""
    users_dict = []
    users = UserRepository.get_all_users(db)
    for user in users:
        user_dict = user.__dict__.copy()
        user_dict["role"] = user.role.__dict__.copy()
        user_dict["role"].pop("_sa_instance_state", None)
        user_dict.pop("_sa_instance_state", None)
        users_dict.append(user_dict)
    return users_dict

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
    user_dict = user.__dict__.copy()
    user_dict["role"] = user.role.__dict__.copy()
    user_dict["role"].pop("_sa_instance_state", None)
    user_dict.pop("_sa_instance_state", None)
    """Lấy danh sách combo."""
    combos = PreQuoteRepository.get_pre_quotes_by_kind(db, "contract_quote")
    # Lọc combo mà có customer.user_id = user_id
    combos = [combo for combo in combos if combo.customer and combo.customer.user_id == user.id]
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
    # user_dict["c"]
    return user_dict

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
@router.post("/users/register", response_model=dict)
def register(user_data: UserCreateDTO, db: Session = Depends(get_db)):
    """Đăng ký."""
    # Logic xác thực đăng ký (ví dụ: kiểm tra username/password)
    finding_user  = UserRepository.get_user_by_phone(db, phone= user_data.phone)
    if finding_user:
        raise HTTPException(status_code=404, detail="User existed")
    new_user = UserRepository.create_user(db, user_data=user_data.dict())
    if not new_user:
        raise HTTPException(status_code=404, detail="Create user failed")
    return {"message": "Register successfully"}
@router.post("/users/login", response_model=dict)
def login(user_data: UserLoginDTO, db: Session = Depends(get_db)):
    """Đăng nhập."""
    # Logic xác thực đăng nhập (ví dụ: so sánh username/password)
    finding_user  = UserRepository.get_user_by_phone(db, phone= user_data.username)
    if not finding_user:
        raise HTTPException(status_code=404, detail="User not found")
    if finding_user.password != user_data.password:
        raise HTTPException(status_code=404, detail="Password is incorrect")
    # Lưu lịch sử đăng nhập
    token = TokenRepository.get_token_by_user_id(db, finding_user.id)
    if token:
        token = TokenRepository.update_token(db, token.id, {"last_modified": datetime.now()})
    else:
        token = TokenRepository.create_token(db, {"user_id": finding_user.id, "last_modified": datetime.now(),"phone": finding_user.phone})
    LoginHistoryRepository.create_login_history(db, {"user_id": finding_user.id, "ip_address": user_data.ip_address, "user_agent": user_data.user_agent})
    token_dict = token.__dict__.copy()
    token_dict["role"] = finding_user.role.__dict__.copy()
    token_dict["role"].pop("_sa_instance_state", None)
    token_dict.pop("_sa_instance_state", None)
    return {"message": "Login successfully", "token": token_dict, "user_id":finding_user.id}

@router.get("/users/modify/{id}", response_model=dict)
def modify_user(id: int, db: Session = Depends(get_db)):
    """Lấy thông tin tokend."""
    token = TokenRepository.get_token_by_user_id(db,id)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    token.last_modified = datetime.now()
    TokenRepository.update_token(db, token.id, token.__dict__)
    return {"message": "Modify token"}

@router.get("/user/commission/{user_id}/{year}", response_model=List[dict])
def get_user_commission_by_user_id(user_id:int,year:int, db: Session = Depends(get_db)):
    """Lấy thông tin hoa hồng theo tháng"""
    commissions = CommissionRepository.get_commissions_by_user_id(db,user_id=user_id)
    # lấy commission trong năm và xếp commissions theo tháng
    commissions_in_year = [commission for commission in commissions if commission.created_at.year >= year]
    monthly_commissions = {}
    for commission in commissions_in_year:
        month = commission.created_at.month
        if month not in monthly_commissions:
            monthly_commissions[month] = []
        monthly_commissions[month].append(commission.__dict__.copy())
    
    # Remove SQLAlchemy state from each commission
    for month in monthly_commissions:
        for commission in monthly_commissions[month]:
            commission.pop("_sa_instance_state", None)
    
    return [{"month": month, "commissions": monthly_commissions[month]} for month in sorted(monthly_commissions.keys())]