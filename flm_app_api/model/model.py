from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Float, DateTime, Boolean
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import json
from datetime import datetime

# Cấu hình database
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "0146424Minh"
POSTGRES_DB = "flm_app"
POSTGRES_HOST = "localhost"  # Hoặc địa chỉ server PostgreSQL
POSTGRES_PORT = "5432"  # Cổng mặc định của PostgreSQL

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Tạo engine kết nối
engine = create_engine(DATABASE_URL, echo=True)

# Khởi tạo session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base ORM
Base = declarative_base()

# Hàm tạo session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(16), nullable=False)
    email = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    phone = Column(String(16), nullable=False, unique=True)
    last_modified = Column(DateTime, default=datetime.now, nullable=False)
    
    user = relationship("User", back_populates="tokens")

class LoginHistory(Base):
    __tablename__ = 'login_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Liên kết tới bảng User
    login_time = Column(DateTime, default=datetime.now, nullable=False)  # Thời gian đăng nhập
    ip_address = Column(String(45), nullable=True)  # Địa chỉ IP (IPv4 hoặc IPv6)
    user_agent = Column(String(255), nullable=True)  # Thông tin trình duyệt hoặc thiết bị
    created_at = Column(DateTime, default=datetime.now)  # Thời gian tạo bản ghi
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # Thời gian cập nhật bản ghi

    user = relationship("User", back_populates="login_histories")  # Liên kết tới User

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Liên kết tới bảng User
    title = Column(String(255), nullable=False)  # Tiêu đề thông báo
    content = Column(Text, nullable=False)  # Nội dung thông báo
    is_read = Column(Boolean, default=False)  # Trạng thái đã đọc hay chưa
    created_at = Column(DateTime, default=datetime.now)  # Thời gian tạo thông báo

    user = relationship("User", back_populates="notifications")  # Liên kết tới User

# Thêm quan hệ ngược trong model User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    phone = Column(String(16), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    list_roles = relationship("Role", secondary="user_roles", back_populates="list_users")
    list_potential_customers = relationship("PotentialCustomer", back_populates="user")
    login_histories = relationship("LoginHistory", back_populates="user", cascade="all, delete-orphan")  # Liên kết tới LoginHistory
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")  # Liên kết tới Notification
    
class PotentialCustomer(Base):
    __tablename__ = 'potential_customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(16), nullable=False)
    email = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

class Sector(Base):
    __tablename__ = 'sectors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable= False)
    description = Column(Text)
    image = Column(String(300))
        
class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(16), nullable=False)
    email = Column(String(255), nullable=False)
    description = Column(Text)
    image = Column(String(300))

class Brand(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique= True, nullable=False)
    name = Column(String(255), nullable= False)
    description = Column(Text)
    image = Column(String(300))
    


# Bảng lưu mẫu cấu trúc vật tư
class MerchandiseTemplate(Base):
    __tablename__ = 'merchandise_templates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)   # Mã loại vật tư (e.g., "OCV")
    name = Column(String(255), nullable=False, unique=True)  # Tên loại vật tư
    sector_id = Column(Integer, ForeignKey('sectors.id'), nullable=False)
    structure_json = Column(Text, nullable=False)  # Mẫu cấu trúc dạng JSON
    sector = relationship('Sector')

    def get_structure(self):
        """ Chuyển đổi JSON string thành dict """
        return json.loads(self.structure_json)

# Bảng vật tư được tạo từ mẫu
class Merchandise(Base):
    __tablename__ = 'merchandises'

    id = Column(Integer, primary_key=True, autoincrement=True)
    template_id = Column(Integer, ForeignKey('merchandise_templates.id'), nullable=False)
    brand_id = Column(Integer, ForeignKey('brands.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    code = Column(Integer, unique=True, nullable=False) # Ma code vat tu
    name = Column(String(255), nullable=False)  # Tên vật tư cụ thể
    data_sheet_link = Column(String(800), nullable=True)
    unit = Column(String(50), nullable=False)
    description_in_contract = Column(Text, nullable=False)
    data_json = Column(Text, nullable=False)  # Dữ liệu vật tư dạng JSON
    created_at = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)
    template = relationship("MerchandiseTemplate")  # Liên kết tới mẫu
    brand = relationship("Brand") # Liên kết bảng brand
    supplier = relationship("Supplier") # Liên kết bảng supplier
    price_infos = relationship("PriceInfo", back_populates="merchandise", cascade="all, delete-orphan")  # Liên kết tới PriceInfo

    def get_data(self):
        """ Chuyển đổi JSON string thành dict """
        return json.loads(self.data_json)

class PriceInfo(Base):
    __tablename__ = 'price_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    merchandise_id = Column(Integer, ForeignKey('merchandises.id'), nullable=False)  # Foreign key to Merchandise
    import_vat = Column(Float, nullable=False)
    sale_vat = Column(float,nullable=False)
    import_price_non_vat = Column(float,nullable=False)
    sale_price_non_vat = Column(float,nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    merchandise = relationship("Merchandise", back_populates="price_infos")  # Liên kết tới Merchandise
    

if __name__ == "__main__":
    # Tạo tất cả các bảng trong cơ sở dữ liệu
    Base.metadata.create_all(bind=engine)
