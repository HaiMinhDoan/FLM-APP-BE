from sqlalchemy.orm import Session
from flm_app_api.model.model import Merchandise, PriceInfo, Brand, Sector, MerchandiseTemplate, User, Notification, LoginHistory, Role, PotentialCustomer, Supplier




class LoginHistoryRepository:
    """Repository cho model LoginHistory."""

    @staticmethod
    def create_login_history(db: Session, login_history_data: dict) -> LoginHistory:
        """Tạo một LoginHistory mới."""
        login_history = LoginHistory(**login_history_data)
        db.add(login_history)
        db.commit()
        db.refresh(login_history)
        return login_history

    @staticmethod
    def get_login_history_by_id(db: Session, login_history_id: int) -> LoginHistory:
        """Lấy LoginHistory theo ID."""
        return db.query(LoginHistory).filter(LoginHistory.id == login_history_id).first()

    @staticmethod
    def get_login_histories_by_user_id(db: Session, user_id: int):
        """Lấy danh sách LoginHistory theo User ID."""
        return db.query(LoginHistory).filter(LoginHistory.user_id == user_id).all()

    @staticmethod
    def delete_login_history(db: Session, login_history_id: int) -> bool:
        """Xóa LoginHistory theo ID."""
        login_history = db.query(LoginHistory).filter(LoginHistory.id == login_history_id).first()
        if not login_history:
            return False
        db.delete(login_history)
        db.commit()
        return True


class NotificationRepository:
    """Repository cho model Notification."""

    @staticmethod
    def create_notification(db: Session, notification_data: dict) -> Notification:
        """Tạo một Notification mới."""
        notification = Notification(**notification_data)
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def get_notification_by_id(db: Session, notification_id: int) -> Notification:
        """Lấy Notification theo ID."""
        return db.query(Notification).filter(Notification.id == notification_id).first()

    @staticmethod
    def get_notifications_by_user_id(db: Session, user_id: int):
        """Lấy danh sách Notification theo User ID."""
        return db.query(Notification).filter(Notification.user_id == user_id).all()

    @staticmethod
    def mark_notification_as_read(db: Session, notification_id: int) -> Notification:
        """Đánh dấu Notification là đã đọc."""
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return None
        notification.is_read = True
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def delete_notification(db: Session, notification_id: int) -> bool:
        """Xóa Notification theo ID."""
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return False
        db.delete(notification)
        db.commit()
        return True

class UserRepository:
    """Repository cho model User."""

    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        """Tạo một User mới."""
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Lấy User theo ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Lấy User theo email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all_users(db: Session):
        """Lấy danh sách tất cả User."""
        return db.query(User).all()

    @staticmethod
    def update_user(db: Session, user_id: int, update_data: dict) -> User:
        """Cập nhật User theo ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Xóa User theo ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True
    
class SectorRepository:
    """Repository cho model Sector."""
    
    @staticmethod
    def create_sector(db: Session, sector_data: dict) -> Sector:
        """Tạo một Sector mới."""
        sector = Sector(**sector_data)
        db.add(sector)
        db.commit()
        db.refresh(sector)
        return sector

    @staticmethod
    def get_sector_by_id(db: Session, sector_id: int) -> Sector:
        """Lấy Sector theo ID."""
        return db.query(Sector).filter(Sector.id == sector_id).first()

    @staticmethod
    def get_all_sectors(db: Session):
        """Lấy danh sách tất cả Sector."""
        return db.query(Sector).all()

    @staticmethod
    def update_sector(db: Session, sector_id: int, update_data: dict) -> Sector:
        """Cập nhật Sector theo ID."""
        sector = db.query(Sector).filter(Sector.id == sector_id).first()
        if not sector:
            return None
        for key, value in update_data.items():
            setattr(sector, key, value)
        db.commit()
        db.refresh(sector)
        return sector

    @staticmethod
    def delete_sector(db: Session, sector_id: int) -> bool:
        """Xóa Sector theo ID."""
        sector = db.query(Sector).filter(Sector.id == sector_id).first()
        if not sector:
            return False
        db.delete(sector)
        db.commit()
        return True


class BrandRepository:
    """Repository cho model Brand."""

    @staticmethod
    def create_brand(db: Session, brand_data: dict) -> Brand:
        """Tạo một Brand mới."""
        brand = Brand(**brand_data)
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand

    @staticmethod
    def get_brand_by_id(db: Session, brand_id: int) -> Brand:
        """Lấy Brand theo ID."""
        return db.query(Brand).filter(Brand.id == brand_id).first()

    @staticmethod
    def get_all_brands(db: Session):
        """Lấy danh sách tất cả Brand."""
        return db.query(Brand).all()

    @staticmethod
    def update_brand(db: Session, brand_id: int, update_data: dict) -> Brand:
        """Cập nhật Brand theo ID."""
        brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not brand:
            return None
        for key, value in update_data.items():
            setattr(brand, key, value)
        db.commit()
        db.refresh(brand)
        return brand

    @staticmethod
    def delete_brand(db: Session, brand_id: int) -> bool:
        """Xóa Brand theo ID."""
        brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not brand:
            return False
        db.delete(brand)
        db.commit()
        return True


class MerchandiseTemplateRepository:
    """Repository cho model MerchandiseTemplate."""

    @staticmethod
    def create_merchandise_template(db: Session, template_data: dict) -> MerchandiseTemplate:
        """Tạo một MerchandiseTemplate mới."""
        template = MerchandiseTemplate(**template_data)
        db.add(template)
        db.commit()
        db.refresh(template)
        return template

    @staticmethod
    def get_merchandise_template_by_id(db: Session, template_id: int) -> MerchandiseTemplate:
        """Lấy MerchandiseTemplate theo ID."""
        return db.query(MerchandiseTemplate).filter(MerchandiseTemplate.id == template_id).first()

    @staticmethod
    def get_all_merchandise_templates(db: Session):
        """Lấy danh sách tất cả MerchandiseTemplate."""
        return db.query(MerchandiseTemplate).all()

    @staticmethod
    def update_merchandise_template(db: Session, template_id: int, update_data: dict) -> MerchandiseTemplate:
        """Cập nhật MerchandiseTemplate theo ID."""
        template = db.query(MerchandiseTemplate).filter(MerchandiseTemplate.id == template_id).first()
        if not template:
            return None
        for key, value in update_data.items():
            setattr(template, key, value)
        db.commit()
        db.refresh(template)
        return template

    @staticmethod
    def delete_merchandise_template(db: Session, template_id: int) -> bool:
        """Xóa MerchandiseTemplate theo ID."""
        template = db.query(MerchandiseTemplate).filter(MerchandiseTemplate.id == template_id).first()
        if not template:
            return False
        db.delete(template)
        db.commit()
        return True

class MerchandiseRepository:
    """Repository cho model Merchandise."""

    @staticmethod
    def create_merchandise(db: Session, merchandise_data: dict) -> Merchandise:
        """Tạo một Merchandise mới."""
        merchandise = Merchandise(**merchandise_data)
        db.add(merchandise)
        db.commit()
        db.refresh(merchandise)
        return merchandise

    @staticmethod
    def get_merchandise_by_id(db: Session, merchandise_id: int) -> Merchandise:
        """Lấy Merchandise theo ID."""
        return db.query(Merchandise).filter(Merchandise.id == merchandise_id).first()

    @staticmethod
    def get_all_merchandises(db: Session):
        """Lấy danh sách tất cả Merchandise."""
        return db.query(Merchandise).all()

    @staticmethod
    def update_merchandise(db: Session, merchandise_id: int, update_data: dict) -> Merchandise:
        """Cập nhật Merchandise theo ID."""
        merchandise = db.query(Merchandise).filter(Merchandise.id == merchandise_id).first()
        if not merchandise:
            return None
        for key, value in update_data.items():
            setattr(merchandise, key, value)
        db.commit()
        db.refresh(merchandise)
        return merchandise

    @staticmethod
    def delete_merchandise(db: Session, merchandise_id: int) -> bool:
        """Xóa Merchandise theo ID."""
        merchandise = db.query(Merchandise).filter(Merchandise.id == merchandise_id).first()
        if not merchandise:
            return False
        db.delete(merchandise)
        db.commit()
        return True


class PriceInfoRepository:
    """Repository cho model PriceInfo."""

    @staticmethod
    def create_price_info(db: Session, price_info_data: dict) -> PriceInfo:
        """Tạo một PriceInfo mới."""
        price_info = PriceInfo(**price_info_data)
        db.add(price_info)
        db.commit()
        db.refresh(price_info)
        return price_info

    @staticmethod
    def get_price_info_by_id(db: Session, price_info_id: int) -> PriceInfo:
        """Lấy PriceInfo theo ID."""
        return db.query(PriceInfo).filter(PriceInfo.id == price_info_id).first()

    @staticmethod
    def get_price_infos_by_merchandise_id(db: Session, merchandise_id: int):
        """Lấy danh sách PriceInfo theo Merchandise ID."""
        return db.query(PriceInfo).filter(PriceInfo.merchandise_id == merchandise_id).all()

    @staticmethod
    def update_price_info(db: Session, price_info_id: int, update_data: dict) -> PriceInfo:
        """Cập nhật PriceInfo theo ID."""
        price_info = db.query(PriceInfo).filter(PriceInfo.id == price_info_id).first()
        if not price_info:
            return None
        for key, value in update_data.items():
            setattr(price_info, key, value)
        db.commit()
        db.refresh(price_info)
        return price_info

    @staticmethod
    def delete_price_info(db: Session, price_info_id: int) -> bool:
        """Xóa PriceInfo theo ID."""
        price_info = db.query(PriceInfo).filter(PriceInfo.id == price_info_id).first()
        if not price_info:
            return False
        db.delete(price_info)
        db.commit()
        return True