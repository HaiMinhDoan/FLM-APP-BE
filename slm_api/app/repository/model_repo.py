from sqlalchemy.orm import Session, joinedload
from app.model.model import Commission,MediaContent, Merchandise, Content, PriceInfo, Brand, Sector, MerchandiseTemplate, User, Notification, LoginHistory
from app.model.model import Role, Supplier,PreQuoteMerchandise, PreQuote,Token, Customer, ContentCategory, PotentialCustomer, ElectricPrice
from app.model.model import Image, Banner
from typing import List
from sqlalchemy import or_



class LoginHistoryRepository:
    """Repository cho model LoginHistory."""

    @staticmethod
    def create_login_history(db: Session, login_history_data: dict) -> LoginHistory:
        """Tạo một LoginHistory mới."""
        login_history = LoginHistory(**login_history_data)
        db.add(login_history)
        db.flush()
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
        db.flush()
        return True
    
class TokenRepository:
    """Repository cho model Token."""

    @staticmethod
    def create_token(db: Session, token_data: dict) -> Token:
        """Tạo một Token mới."""
        token = Token(**token_data)
        db.add(token)
        db.flush()
        db.refresh(token)
        return token

    @staticmethod
    def get_token_by_id(db: Session, token_id: int) -> Token:
        """Lấy Token theo ID."""
        return db.query(Token).filter(Token.id == token_id).first()

    @staticmethod
    def get_token_by_user_id(db: Session, user_id: int) -> Token:
        """Lấy Token theo User ID."""
        return db.query(Token).filter(Token.user_id == user_id).first()

    @staticmethod
    def delete_token(db: Session, token_id: int) -> bool:
        """Xóa Token theo ID."""
        token = db.query(Token).filter(Token.id == token_id).first()
        if not token:
            return False
        db.delete(token)
        db.flush()
        return True
    @staticmethod
    def update_token(db: Session, token_id: int, update_data: dict) -> Token:
        """Cập nhật Token theo ID."""
        token = db.query(Token).filter(Token.id == token_id).first()
        if not token:
            return None
        for key, value in update_data.items():
            setattr(token, key, value)
        db.flush()
        db.refresh(token)
        return token


class NotificationRepository:
    """Repository cho model Notification."""

    @staticmethod
    def create_notification(db: Session, notification_data: dict) -> Notification:
        """Tạo một Notification mới."""
        notification = Notification(**notification_data)
        db.add(notification)
        db.flush()
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
        db.flush()
        db.refresh(notification)
        return notification

    @staticmethod
    def delete_notification(db: Session, notification_id: int) -> bool:
        """Xóa Notification theo ID."""
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return False
        db.delete(notification)
        db.flush()
        return True

class UserRepository:
    """Repository cho model User."""

    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        """Tạo một User mới."""
        user = User(**user_data)
        db.add(user)
        db.flush()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Lấy User theo ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_parent_id(db: Session, parent_id: int) -> List[User]:
        """Lấy User theo ID."""
        return db.query(User).options(joinedload(User.commissions)).filter(User.parent_id == parent_id).all()
    
    @staticmethod
    def get_agent_by_parent_id(db: Session, parent_id: int) -> List[User]:
        """Lấy User theo ID."""
        return db.query(User).options(joinedload(User.commissions)).filter(User.parent_id == parent_id, User.role_id != 3).all()
    
    @staticmethod
    def get_customer_account_by_parent_id(db: Session, parent_id: int) -> List[User]:
        """Lấy User theo ID."""
        return db.query(User).options(joinedload(User.commissions)).filter(User.parent_id == parent_id, User.role_id == 3).all()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Lấy User theo email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_phone(db: Session, phone: str) -> User:
        """Lấy User theo phone."""
        return db.query(User).options(joinedload(User.role)).filter(User.phone == phone).first()
    
    @staticmethod
    def get_active_user_by_phone(db: Session, phone: str) -> User:
        """Lấy User theo phone."""
        return db.query(User).options(joinedload(User.role)).filter(User.phone == phone, User.active != False).first()

    @staticmethod
    def get_all_users(db: Session):
        """Lấy danh sách tất cả User."""
        return db.query(User).all()
    
    @staticmethod
    def get_all_active_users(db: Session):
        """Lấy danh sách tất cả User."""
        return db.query(User).filter(User.active == True).all()
    
    @staticmethod
    def get_all_sales(db: Session):
        """Lấy danh sách tất cả User có Role.name chứa 'ad_sale' hoặc 'agent1'."""
        return (
            db.query(User)
            .join(Role)
            .filter(or_(Role.name.like('%ad_sale%'), Role.name.like('%agent1%'),Role.name.like('%agent2%')))
            .all()
        )
    
    @staticmethod
    def update_user(db: Session, user_id: int, update_data: dict) -> User:
        """Cập nhật User theo ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        db.flush()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Xóa User theo ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.flush()
        return True
    
class SectorRepository:
    """Repository cho model Sector."""
    
    @staticmethod
    def create_sector(db: Session, sector_data: dict) -> Sector:
        """Tạo một Sector mới."""
        sector = Sector(**sector_data)
        db.add(sector)
        db.flush()
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
        db.flush()
        db.refresh(sector)
        return sector

    @staticmethod
    def delete_sector(db: Session, sector_id: int) -> bool:
        """Xóa Sector theo ID."""
        sector = db.query(Sector).filter(Sector.id == sector_id).first()
        if not sector:
            return False
        db.delete(sector)
        db.flush()
        return True


class BrandRepository:
    """Repository cho model Brand."""

    @staticmethod
    def create_brand(db: Session, brand_data: dict) -> Brand:
        """Tạo một Brand mới."""
        brand = Brand(**brand_data)
        db.add(brand)
        db.flush()
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
        db.flush()
        db.refresh(brand)
        return brand

    @staticmethod
    def delete_brand(db: Session, brand_id: int) -> bool:
        """Xóa Brand theo ID."""
        brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not brand:
            return False
        db.delete(brand)
        db.flush()
        return True


class MerchandiseTemplateRepository:
    """Repository cho model MerchandiseTemplate."""

    @staticmethod
    def create_merchandise_template(db: Session, template_data: dict) -> MerchandiseTemplate:
        """Tạo một MerchandiseTemplate mới."""
        template = MerchandiseTemplate(**template_data)
        db.add(template)
        db.flush()
        db.refresh(template)
        return template

    @staticmethod
    def get_merchandise_template_by_id(db: Session, template_id: int) -> MerchandiseTemplate:
        """Lấy MerchandiseTemplate theo ID."""
        return db.query(MerchandiseTemplate).filter(MerchandiseTemplate.id == template_id).first()
    
    @staticmethod
    def get_merchandise_template_by_code(db: Session, code: str) -> MerchandiseTemplate:
        """Lấy MerchandiseTemplate theo ID."""
        return db.query(MerchandiseTemplate).filter(MerchandiseTemplate.code == code).first()

    @staticmethod
    def get_all_merchandise_templates(db: Session) -> List[MerchandiseTemplate]:
        """Lấy danh sách tất cả MerchandiseTemplate."""
        templates = db.query(MerchandiseTemplate).all()
        return templates

    @staticmethod
    def update_merchandise_template(db: Session, template_id: int, update_data: dict) -> MerchandiseTemplate:
        """Cập nhật MerchandiseTemplate theo ID."""
        template = db.query(MerchandiseTemplate).filter(MerchandiseTemplate.id == template_id).first()
        if not template:
            return None
        for key, value in update_data.items():
            setattr(template, key, value)
        db.flush()
        db.refresh(template)
        return template

    @staticmethod
    def delete_merchandise_template(db: Session, template_id: int) -> bool:
        """Xóa MerchandiseTemplate theo ID."""
        template = db.query(MerchandiseTemplate).filter(MerchandiseTemplate.id == template_id).first()
        if not template:
            return False
        db.delete(template)
        db.flush()
        return True

class MerchandiseRepository:
    """Repository cho model Merchandise."""
    @staticmethod
    def create_image(db: Session, image_data: dict) -> Image:
        """Tạo một Image mới."""
        image = Image(**image_data)
        db.add(image)
        db.flush()
        db.refresh(image)
        return image

    @staticmethod
    def create_merchandise(db: Session, merchandise_data: dict) -> Merchandise:
        """Tạo một Merchandise mới."""
        merchandise = Merchandise(**merchandise_data)
        db.add(merchandise)
        db.flush()
        db.refresh(merchandise)
        return merchandise

    @staticmethod
    def get_merchandise_by_id(db: Session, merchandise_id: int) -> Merchandise:
        """Lấy Merchandise theo ID."""
        return db.query(Merchandise).filter(Merchandise.id == merchandise_id).first()
    
    @staticmethod
    def get_merchandise_by_code(db: Session, code: str) -> Merchandise:
        """Lấy Merchandise theo ID."""
        return db.query(Merchandise).filter(Merchandise.code == code).first()
    
    @staticmethod
    def get_merchandise_by_id_with_all(db: Session, id: int) -> Merchandise:
        """Lấy Merchandise theo ID cùng với PriceInfo."""
        return db.query(Merchandise).options(joinedload(Merchandise.price_infos), joinedload(Merchandise.images)).filter(Merchandise.id == id).first()
    
    @staticmethod
    def get_all_merchandises(db: Session):
        """Lấy danh sách tất cả Merchandise."""
        return db.query(Merchandise).all()
    
    @staticmethod
    def get_all_merchandises_with_prices(db: Session):
        """Lấy danh sách tất cả Merchandise cùng với PriceInfo."""
        return db.query(Merchandise).options(joinedload(Merchandise.price_infos), joinedload(Merchandise.template), joinedload(Merchandise.brand), joinedload(Merchandise.supplier)).all()
    
    @staticmethod
    def get_all_merchandises_with_prices_and_images(db: Session):
        """Lấy danh sách tất cả Merchandise cùng với PriceInfo."""
        return db.query(Merchandise).options(
            joinedload(Merchandise.price_infos),
            joinedload(Merchandise.images), 
            joinedload(Merchandise.template), 
            joinedload(Merchandise.brand), joinedload(Merchandise.supplier)).all()

    @staticmethod
    def update_merchandise(db: Session, merchandise_id: int, update_data: dict) -> Merchandise:
        """Cập nhật Merchandise theo ID."""
        merchandise = db.query(Merchandise).filter(Merchandise.id == merchandise_id).first()
        if not merchandise:
            return None
        for key, value in update_data.items():
            setattr(merchandise, key, value)
        db.flush()
        db.refresh(merchandise)
        return merchandise

    @staticmethod
    def delete_merchandise(db: Session, merchandise_id: int) -> bool:
        """Xóa Merchandise theo ID."""
        merchandise = db.query(Merchandise).filter(Merchandise.id == merchandise_id).first()
        if not merchandise:
            return False
        db.delete(merchandise)
        db.flush()
        return True


class PriceInfoRepository:
    """Repository cho model PriceInfo."""

    @staticmethod
    def create_price_info(db: Session, price_info_data: dict) -> PriceInfo:
        """Tạo một PriceInfo mới."""
        price_info = PriceInfo(**price_info_data)
        db.add(price_info)
        db.flush()
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
        db.flush()
        db.refresh(price_info)
        return price_info

    @staticmethod
    def delete_price_info(db: Session, price_info_id: int) -> bool:
        """Xóa PriceInfo theo ID."""
        price_info = db.query(PriceInfo).filter(PriceInfo.id == price_info_id).first()
        if not price_info:
            return False
        db.delete(price_info)
        db.flush()
        return True
    
class PreQuoteRepository:
    """Repository cho model PreQuote."""

    @staticmethod
    def create_pre_quote(db: Session, pre_quote_data: dict) -> PreQuote:
        """Tạo một PreQuote mới."""
        pre_quote = PreQuote(**pre_quote_data)
        db.add(pre_quote)
        db.flush()  # Đảm bảo ID được tạo trước khi refresh
        db.refresh(pre_quote)  # Tải lại đối tượng từ cơ sở dữ liệu
        return pre_quote

    @staticmethod
    def get_pre_quote_by_id(db: Session, pre_quote_id: int) -> PreQuote:
        """Lấy PreQuote theo ID."""
        return db.query(PreQuote).options(joinedload(PreQuote.customer), joinedload(PreQuote.pre_quote_merchandises).joinedload(PreQuoteMerchandise.merchandise).joinedload(Merchandise.template)).filter(PreQuote.id == pre_quote_id).first()
    
    @staticmethod
    def get_pre_quote_by_id_with_brand(db: Session, pre_quote_id: int) -> PreQuote:
        """Lấy PreQuote theo ID với brand."""
        return db.query(PreQuote).options(
            joinedload(PreQuote.customer), 
            joinedload(PreQuote.pre_quote_merchandises).
            joinedload(PreQuoteMerchandise.merchandise).
            joinedload(Merchandise.template),
            joinedload(PreQuote.pre_quote_merchandises)
            .joinedload(PreQuoteMerchandise.merchandise)
            .joinedload(Merchandise.brand)).filter(PreQuote.id == pre_quote_id).first()
    
    
    @staticmethod
    def get_pre_quote_by_potential_customer_id(db: Session, potential_customer_id: int) -> PreQuote:
        """Lấy PreQuote theo ID."""
        return db.query(PreQuote).options(
            joinedload(PreQuote.pre_quote_merchandises)
            .joinedload(PreQuoteMerchandise.merchandise)
            .joinedload(Merchandise.template)).filter(PreQuote.potential_customer_id == potential_customer_id).all()
    
    
    @staticmethod
    def get_pre_quote_by_id_simple(db: Session, pre_quote_id: int) -> PreQuote:
        """Lấy PreQuote theo ID."""
        return db.query(PreQuote).options(joinedload(PreQuote.customer)).filter(PreQuote.id == pre_quote_id).first()
    
    @staticmethod
    def get_all_pre_quotes(db: Session):
        """Lấy danh sách tất cả PreQuote."""
        return db.query(PreQuote).options(joinedload(PreQuote.customer)).all()

    @staticmethod
    def update_pre_quote(db: Session, pre_quote_id: int, update_data: dict) -> PreQuote:
        """Cập nhật PreQuote theo ID."""
        pre_quote = db.query(PreQuote).filter(PreQuote.id == pre_quote_id).first()
        if not pre_quote:
            return None
        for key, value in update_data.items():
            setattr(pre_quote, key, value)
        db.flush()
        db.refresh(pre_quote)
        return pre_quote

    @staticmethod
    def delete_pre_quote(db: Session, pre_quote_id: int) -> bool:
        """Xóa PreQuote theo ID."""
        pre_quote = db.query(PreQuote).filter(PreQuote.id == pre_quote_id).first()
        if not pre_quote:
            return False
        db.delete(pre_quote)
        db.flush()
        return True
    
    @staticmethod
    def get_pre_quotes_by_kind_and_sector(db: Session, kind: str, sector: str) -> List[PreQuote]:
        """Lấy danh sách PreQuote theo kind và sector, bao gồm cả template của merchandise."""
        return (
            db.query(PreQuote)
            .options(
                joinedload(PreQuote.customer),
                joinedload(PreQuote.pre_quote_merchandises)
                .joinedload(PreQuoteMerchandise.merchandise)
                .joinedload(Merchandise.images),
                joinedload(PreQuote.pre_quote_merchandises)
                .joinedload(PreQuoteMerchandise.merchandise)
                .joinedload(Merchandise.template),
            )
            .filter(
                PreQuote.kind == kind,
                PreQuote.status == "accepted",
                PreQuote.sector == sector,
            )
            .all()
        )
    @staticmethod
    def get_best_selling_combos(db: Session) -> List[PreQuote]:
        """Lấy danh sách PreQuote theo kind."""
        return db.query(PreQuote).options(
            joinedload(PreQuote.customer), 
            joinedload(PreQuote.pre_quote_merchandises)
            .joinedload(PreQuoteMerchandise.merchandise)
            .joinedload(Merchandise.images)).filter(
                PreQuote.kind == "combo", 
                PreQuote.status == "accepted", 
                PreQuote.best_selling == True ).all()
    
    @staticmethod
    def get_contract_quote_by_buyer_id_and_sector(buyer_id:int,sector:str,db: Session) -> List[PreQuote]:
        """Lấy danh sách PreQuote theo kind."""
        return db.query(PreQuote).options(
            joinedload(PreQuote.customer), 
            joinedload(PreQuote.pre_quote_merchandises)
            .joinedload(PreQuoteMerchandise.merchandise)
            .joinedload(Merchandise.images)).filter(
                PreQuote.kind == "contract_quote", 
                PreQuote.status == "accepted", 
                PreQuote.sector == sector,
                PreQuote.buyer_id == buyer_id ).all()
    
    @staticmethod
    def get_pre_quotes_by_kind_and_user_id(db: Session, kind: str, user_id:int) -> List[PreQuote]:
        """Lấy danh sách PreQuote theo kind."""
        return db.query(PreQuote).options(joinedload(PreQuote.customer), joinedload(PreQuote.pre_quote_merchandises).joinedload(PreQuoteMerchandise.merchandise).joinedload(Merchandise.images)).filter(PreQuote.kind == kind, PreQuote.status == "accepted", PreQuote.customer.user_id==user_id ).all()
    @staticmethod
    def get_pre_quotes_by_kind_and_installation_type(db: Session, kind: str, installation_type: str) -> List[PreQuote]:
        """Lấy danh sách PreQuote theo kind và installation_type."""
        return db.query(PreQuote).options(joinedload(PreQuote.customer), joinedload(PreQuote.pre_quote_merchandises).joinedload(PreQuoteMerchandise.merchandise)).filter(PreQuote.kind == kind, PreQuote.status == "accepted", PreQuote.installation_type == installation_type).all()
    
class PreQuoteMerchandiseRepository:
    """Repository cho model PreQuoteMerchandise."""

    @staticmethod
    def create_pre_quote_merchandise(db: Session, pre_quote_merchandise_data: dict) -> PreQuoteMerchandise:
        """Tạo một PreQuoteMerchandise mới."""
        pre_quote_merchandise = PreQuoteMerchandise(**pre_quote_merchandise_data)
        db.add(pre_quote_merchandise)
        db.flush()
        db.refresh(pre_quote_merchandise)
        return pre_quote_merchandise

    @staticmethod
    def get_pre_quote_merchandise_by_id(db: Session, pre_quote_merchandise_id: int) -> PreQuoteMerchandise:
        """Lấy PreQuoteMerchandise theo ID."""
        return db.query(PreQuoteMerchandise).filter(PreQuoteMerchandise.id == pre_quote_merchandise_id).first()

    @staticmethod
    def get_pre_quote_merchandises_by_pre_quote_id(db: Session, pre_quote_id: int):
        """Lấy danh sách PreQuoteMerchandise theo PreQuote ID."""
        return db.query(PreQuoteMerchandise).filter(PreQuoteMerchandise.pre_quote_id == pre_quote_id).all()

    @staticmethod
    def update_pre_quote_merchandise(db: Session, pre_quote_merchandise_id: int, update_data: dict) -> PreQuoteMerchandise:
        """Cập nhật PreQuoteMerchandise theo ID."""
        pre_quote_merchandise = db.query(PreQuoteMerchandise).filter(PreQuoteMerchandise.id == pre_quote_merchandise_id).first()
        if not pre_quote_merchandise:
            return None
        for key, value in update_data.items():
            setattr(pre_quote_merchandise, key, value)
        db.flush()
        db.refresh(pre_quote_merchandise)
        return pre_quote_merchandise

    @staticmethod
    def delete_pre_quote_merchandise(db: Session, pre_quote_merchandise_id: int) -> bool:
        """Xóa PreQuoteMerchandise theo ID."""
        pre_quote_merchandise = db.query(PreQuoteMerchandise).filter(PreQuoteMerchandise.id == pre_quote_merchandise_id).first
    
class RoleRepository:
    """Repository cho model Role."""

    @staticmethod
    def create_role(db: Session, role_data: dict) -> Role:
        """Tạo một Role mới."""
        role = Role(**role_data)
        db.add(role)
        db.flush()
        db.refresh(role)
        return role

    @staticmethod
    def get_role_by_id(db: Session, role_id: int) -> Role:
        """Lấy Role theo ID."""
        return db.query(Role).filter(Role.id == role_id).first()

    @staticmethod
    def get_all_roles(db: Session):
        """Lấy danh sách tất cả Role."""
        return db.query(Role).all()

    @staticmethod
    def update_role(db: Session, role_id: int, update_data: dict) -> Role:
        """Cập nhật Role theo ID."""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return None
        for key, value in update_data.items():
            setattr(role, key, value)
        db.flush()
        db.refresh(role)
        return role

    @staticmethod
    def delete_role(db: Session, role_id: int) -> bool:
        """Xóa Role theo ID."""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return False
        db.flush(role)
        db.flush()
        return True

class SectorRepository:
    """Repository cho model Sector."""

    @staticmethod
    def create_sector(db: Session, sector_data: dict) -> Sector:
        """Tạo một Sector mới."""
        sector = Sector(**sector_data)
        db.add(sector)
        db.flush()
        db.refresh(sector)
        return sector

    @staticmethod
    def get_sector_by_id(db: Session, sector_id: int) -> Sector:
        """Lấy Sector theo ID."""
        return db.query(Sector).filter(Sector.id == sector_id).first()
    
    @staticmethod
    def get_sector_by_code(db: Session, code: str) -> Sector:
        """Lấy Sector theo ID."""
        return db.query(Sector).filter(Sector.code == code).first()

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
        db.flush()
        db.refresh(sector)
        return sector

    @staticmethod
    def delete_sector(db: Session, sector_id: int) -> bool:
        """Xóa Sector theo ID."""
        sector = db.query(Sector).filter(Sector.id == sector_id).first()
        if not sector:
            return False
        db.delete(sector)
        db.flush()
        return True
    

class CustomerRepository:
    """Repository cho model Customer."""

    @staticmethod
    def create_customer(db: Session, customer_data: dict) -> Customer:
        """Tạo một Customer mới."""
        customer = Customer(**customer_data)
        db.add(customer)
        db.flush()
        db.refresh(customer)
        return customer

    @staticmethod
    def get_customer_by_id(db: Session, customer_id: int) -> Customer:
        """Lấy Customer theo ID."""
        return db.query(Customer).filter(Customer.id == customer_id).first()
    
    @staticmethod
    def get_customer_by_sale_id(db: Session, sale_id: int) -> List[Customer]:
        """Lấy Customer theo sale ID."""
        return db.query(Customer).filter(Customer.user_id == sale_id).all()
    
    @staticmethod
    def get_customer_by_code(db: Session, code: str) -> Customer:
        """Lấy Customer theo ID."""
        return db.query(Customer).filter(Customer.code == code).first()
    
    @staticmethod
    def get_customer_by_phone(db: Session, phone: str) -> Customer:
        """Lấy Customer theo ID."""
        return db.query(Customer).filter(Customer.phone == phone).first()

    @staticmethod
    def get_all_customers(db: Session) -> List[Customer]:
        """Lấy danh sách tất cả Customer."""
        return db.query(Customer).all()

    @staticmethod
    def update_customer(db: Session, customer_id: int, update_data: dict) -> Customer:
        """Cập nhật Customer theo ID."""
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return None
        for key, value in update_data.items():
            setattr(customer, key, value)
        db.flush()
        db.refresh(customer)
        return customer

    @staticmethod
    def delete_customer(db: Session, customer_id: int) -> bool:
        """Xóa Customer theo ID."""
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return False
        db.delete(customer)
        db.flush()
        return True

class ContentRepository:
    """Repository cho model Content."""

    @staticmethod
    def create_content(db: Session, content_data: dict) -> Content:
        """Tạo một Content mới."""
        content = Content(**content_data)
        db.add(content)
        db.flush()
        db.refresh(content)
        return content

    @staticmethod
    def get_content_by_id(db: Session, content_id: int) -> Content:
        """Lấy Content theo ID."""
        return db.query(Content).filter(Content.id == content_id).first()

    @staticmethod
    def get_all_contents(db: Session) -> List[Content]:
        """Lấy danh sách tất cả Content."""
        return db.query(Content).options(joinedload(Content.media_contents), joinedload(Content.category)).all()
    
    @staticmethod
    def get_all_contents_by_sector(db: Session, sector: str) -> List[Content]:
        """Lấy danh sách Content mà category.sector chứa một đoạn chuỗi cụ thể."""
        return (
            db.query(Content)
            .join(ContentCategory, Content.category_id == ContentCategory.id)
            .filter(ContentCategory.sector.like(f"%{sector}%"))
            .options(joinedload(Content.media_contents), joinedload(Content.category))
            .all()
        )
    @staticmethod
    def get_contents_by_hashtag(db: Session, hashtag: str) -> List[Content]:
        """Lấy danh sách tất cả Content theo hashtag hoặc có all_agent = True."""
        return (
            db.query(Content)
            .options(joinedload(Content.media_contents), joinedload(Content.category))
            .filter(
                or_(
                    Content.hashtag.like(f"%{hashtag}%"),
                    Content.all_agent == True
                )
            )
            .all()
        )
    @staticmethod
    def update_content(db: Session, content_id: int, update_data: dict) -> Content:
        """Cập nhật Content theo ID."""
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            return None
        for key, value in update_data.items():
            setattr(content, key, value)
        db.flush()
        db.refresh(content)
        return content

    @staticmethod
    def delete_content(db: Session, content_id: int) -> bool:
        """Xóa Content theo ID."""
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            return False
        db.delete(content)
        db.flush()
        return True

class MediaContentRepository:
    """Repository cho model MediaContent."""
    @staticmethod
    def create_media_content(db: Session, media_content_data: dict) -> MediaContent:
        """Tạo một MediaContent mới."""
        media_content = MediaContent(**media_content_data)
        db.add(media_content)
        db.flush()
        db.refresh(media_content)
        return media_content

    @staticmethod
    def get_media_content_by_id(db: Session, media_content_id: int) -> MediaContent:
        """Lấy MediaContent theo ID."""
        return db.query(MediaContent).filter(MediaContent.id == media_content_id).first()
    
    @staticmethod
    def get_media_content_by_content_id(db: Session, content_id: int) -> List[MediaContent]:
        """Lấy MediaContent theo ID."""
        return db.query(MediaContent).filter(MediaContent.content_id == content_id).all()

    @staticmethod
    def get_all_media_contents(db: Session) -> List[MediaContent]:
        """Lấy danh sách tất cả MediaContent."""
        return db.query(MediaContent).all()

    @staticmethod
    def update_media_content(db: Session, media_content_id: int, update_data: dict) -> MediaContent:
        """Cập nhật MediaContent theo ID."""
        media_content = db.query(MediaContent).filter(MediaContent.id == media_content_id).first()
        if not media_content:
            return None
        for key, value in update_data.items():
            setattr(media_content, key, value)
        db.flush()
        db.refresh(media_content)
        return media_content

    @staticmethod
    def delete_media_content(db: Session, media_content_id: int) -> bool:
        """Xóa MediaContent theo ID."""
        media_content = db.query(MediaContent).filter(MediaContent.id == media_content_id).first()
        if not media_content:
            return False
        db.delete(media_content)
        db.flush()
        return True
    
class ContentCategoryRepository:
    """Repository cho model ContentCategory."""
    @staticmethod
    def create_content_category(db: Session, content_category_data: dict) -> ContentCategory:
        """Tạo một ContentCategory mới."""
        content_category = ContentCategory(**content_category_data)
        db.add(content_category)
        db.flush()
        db.refresh(content_category)
        return content_category

    @staticmethod
    def get_content_category_by_id(db: Session, content_category_id: int) -> ContentCategory:
        """Lấy ContentCategory theo ID."""
        return db.query(ContentCategory).filter(ContentCategory.id == content_category_id).first()
    
    @staticmethod
    def get_content_category_by_content_id(db: Session, content_id: int) -> ContentCategory:
        """Lấy ContentCategory theo ID."""
        return db.query(ContentCategory).filter(ContentCategory.content_id == content_id).first()

    @staticmethod
    def get_all_content_categories(db: Session) -> List[ContentCategory]:
        """Lấy danh sách tất cả ContentCategory."""
        return db.query(ContentCategory).all()

    @staticmethod
    def update_content_category(db: Session, content_category_id: int, update_data: dict) -> ContentCategory:
        """Cập nhật ContentCategory theo ID."""
        content_category = db.query(ContentCategory).filter(ContentCategory.id == content_category_id).first()
        if not content_category:
            return None
        for key, value in update_data.items():
            setattr(content_category, key, value)
        db.flush()
        db.refresh(content_category)
        return content_category

    @staticmethod
    def delete_content_category(db: Session, content_category_id: int) -> bool:
        """Xóa ContentCategory theo ID."""
        content_category = db.query(ContentCategory).filter(ContentCategory.id == content_category_id).first()
        if not content_category:
            return False
        db.delete(content_category)
        db.flush()
        return True


class CommissionRepository:
    """Repository cho model Commission."""

    @staticmethod
    def create_commission(db: Session, commission_data: dict) -> Commission:
        """Tạo một Commission mới."""
        commission = Commission(**commission_data)
        db.add(commission)
        db.flush()
        db.refresh(commission)
        return commission

    @staticmethod
    def get_commission_by_id(db: Session, commission_id: int) -> Commission:
        """Lấy Commission theo ID."""
        return db.query(Commission).filter(Commission.id == commission_id).first()

    @staticmethod
    def get_commissions_by_user_id(db: Session, user_id: int) -> List[Commission]:
        """Lấy danh sách Commission theo User ID."""
        return db.query(Commission).options(joinedload(Commission.sector)).filter(Commission.seller == user_id).all()

    @staticmethod
    def get_all_commissions(db: Session) -> List[Commission]:
        """Lấy danh sách tất cả Commission."""
        return db.query(Commission).all()

    @staticmethod
    def update_commission(db: Session, commission_id: int, update_data: dict) -> Commission:
        """Cập nhật Commission theo ID."""
        commission = db.query(Commission).filter(Commission.id == commission_id).first()
        if not commission:
            return None
        for key, value in update_data.items():
            setattr(commission, key, value)
        db.flush()
        db.refresh(commission)
        return commission

    @staticmethod
    def delete_commission(db: Session, commission_id: int) -> bool:
        """Xóa Commission theo ID."""
        commission = db.query(Commission).filter(Commission.id == commission_id).first()
        if not commission:
            return False
        db.delete(commission)
        db.flush()
        return True

class PotentialCustomerRepository:
    """PotentialCustomerRepository thao tác dữ liệu với bảng PotentialCustomer"""
    @staticmethod
    def get_one_potential_customers_by_assumed_code(db: Session, code:str) -> PotentialCustomer:
        """Lấy tất cả những khách hàng tiềm năng của agent có id là agent_id"""
        return db.query(PotentialCustomer).filter(PotentialCustomer.assumed_code == code).first()
    @staticmethod
    def get_all_potential_customers_by_agent_id(db: Session, agent_id:int) -> List[PotentialCustomer]:
        """Lấy tất cả những khách hàng tiềm năng của agent có id là agent_id"""
        return db.query(PotentialCustomer).filter(PotentialCustomer.agent_id == agent_id).all()
    
    @staticmethod
    def create_potential_customer(db: Session, potential_customer_data: dict) -> PotentialCustomer:
        """Tạo một PotentialCustomer mới."""
        potential_customer = PotentialCustomer(**potential_customer_data)
        db.add(potential_customer)
        db.flush()
        db.refresh(potential_customer)
        return potential_customer
    
    @staticmethod
    def get_potential_customer_by_assumed_or_phone(db: Session, phone:str, assumed_code:str) -> PotentialCustomer:
        """Lấy PotentialCustomer theo điện thoại."""
        return db.query(PotentialCustomer).filter(or_(PotentialCustomer.phone == phone, PotentialCustomer.assumed_code == assumed_code)).first()

    @staticmethod
    def get_potential_customer_by_id(db: Session, potential_customer_id: int) -> PotentialCustomer:
        """Lấy PotentialCustomer theo ID."""
        return db.query(PotentialCustomer).filter(PotentialCustomer.id == potential_customer_id).first()
    
    @staticmethod
    def get_potential_customer_by_phone(db: Session, potential_customer_phone: str) -> PotentialCustomer:
        """Lấy PotentialCustomer theo số điện thoại."""
        return db.query(PotentialCustomer).filter(PotentialCustomer.phone == potential_customer_phone).first()
    
    @staticmethod
    def get_potential_customer_by_code(db: Session, potential_customer_code: str) -> PotentialCustomer:
        """Lấy PotentialCustomer theo mã."""
        return db.query(PotentialCustomer).filter(PotentialCustomer.assumed_code == potential_customer_code).first()

    @staticmethod
    def get_all_potential_customers(db: Session) -> List[PotentialCustomer]:
        """Lấy danh sách tất cả PotentialCustomer."""
        return db.query(PotentialCustomer).all()

    @staticmethod
    def update_potential_customer(db: Session, potential_customer_id: int, update_data: dict) -> PotentialCustomer:
        """Cập nhật PotentialCustomer theo ID."""
        potential_customer = db.query(PotentialCustomer).filter(PotentialCustomer.id == potential_customer_id).first()
        if not potential_customer:
            return None
        for key, value in update_data.items():
            setattr(potential_customer, key, value)
        db.flush()
        db.refresh(potential_customer)
        return potential_customer

    @staticmethod
    def delete_potential_customer(db: Session, potential_customer_id: int) -> bool:
        """Xóa PotentialCustomer theo ID."""
        potential_customer = db.query(PotentialCustomer).filter(PotentialCustomer.id == potential_customer_id).first()
        if not potential_customer:
            return False
        db.delete(potential_customer)
        db.flush()
        return True
    
class BannerRepository:
    """Repository cho model Banner."""

    @staticmethod
    def create_banner(db: Session, banner_data: dict) -> Banner:
        """Tạo một Banner mới."""
        banner = Banner(**banner_data)
        db.add(banner)
        db.flush()
        db.refresh(banner)
        return banner

    @staticmethod
    def get_banner_by_id(db: Session, banner_id: int) -> Banner:
        """Lấy Banner theo ID."""
        return db.query(Banner).filter(Banner.id == banner_id).first()

    @staticmethod
    def get_all_banners(db: Session) -> List[Banner]:
        """Lấy danh sách tất cả Banner."""
        return db.query(Banner).options(joinedload(Banner.banner_images)).all()

    @staticmethod
    def update_banner(db: Session, banner_id: int, update_data: dict) -> Banner:
        """Cập nhật Banner theo ID."""
        banner = db.query(Banner).filter(Banner.id == banner_id).first()
        if not banner:
            return None
        for key, value in update_data.items():
            setattr(banner, key, value)
        db.flush()
        db.refresh(banner)
        return banner

class ElectricPriceRepository:
    """Repository cho model ElectricPrice."""

    @staticmethod
    def create_electric_price(db: Session, electric_price_data: dict) -> ElectricPrice:
        """Tạo một ElectricPrice mới."""
        electric_price = ElectricPrice(**electric_price_data)
        db.add(electric_price)
        db.flush()
        db.refresh(electric_price)
        return electric_price

    @staticmethod
    def get_electric_price_by_id(db: Session, electric_price_id: int) -> ElectricPrice:
        """Lấy ElectricPrice theo ID."""
        return db.query(ElectricPrice).filter(ElectricPrice.id == electric_price_id).first()

    @staticmethod
    def get_all_electric_prices(db: Session) -> List[ElectricPrice]:
        """Lấy danh sách tất cả ElectricPrice."""
        return db.query(ElectricPrice).all()

    @staticmethod
    def update_electric_price(db: Session, electric_price_id: int, update_data: dict) -> ElectricPrice:
        """Cập nhật ElectricPrice theo ID."""
        electric_price = db.query(ElectricPrice).filter(ElectricPrice.id == electric_price_id).first()
        if not electric_price:
            return None
        for key, value in update_data.items():
            setattr(electric_price, key, value)
        db.flush()
        db.refresh(electric_price)
        return electric_price

    @staticmethod
    def delete_electric_price(db: Session, electric_price_id: int) -> bool:
        """Xóa ElectricPrice theo ID."""
        electric_price = db.query(ElectricPrice).filter(ElectricPrice.id == electric_price_id).first()
        if not electric_price:
            return False
        db.delete(electric_price)
        db.flush()
        return True
