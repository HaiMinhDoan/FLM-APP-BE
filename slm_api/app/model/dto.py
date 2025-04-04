from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime


class UserLoginDTO(BaseModel):
    """DTO cho việc đăng nhập."""
    username: str = Field(..., max_length=50, description="Tên đăng nhập")
    password: str = Field(..., max_length=50, description="Mật khẩu")
    ip_address: str = Field(..., description="Địa chỉ IP")
    user_agent: str = Field(..., description="User Agent")
    

class ResponseDataDTO(BaseModel):
    """DTO cho việc trả về dữ liệu."""
    status: int = Field(..., description="Trạng thái trả về")
    message: str = Field(..., description="Thông điệp trả về")
    data: Any = Field(..., description="Dữ liệu trả về")
    


class SectorCreateDTO(BaseModel):
    """DTO cho việc tạo mới Sector."""
    code: str = Field(..., max_length=50, description="Mã của Sector")
    name: str = Field(..., max_length=255, description="Tên của Sector")
    description: Optional[str] = Field(None, description="Mô tả Sector")
    image: Optional[str] = Field(None, max_length=300, description="Đường dẫn hình ảnh của Sector")


class SectorUpdateDTO(BaseModel):
    """DTO cho việc cập nhật Sector."""
    code: Optional[str] = Field(None, max_length=50, description="Mã của Sector")
    name: Optional[str] = Field(None, max_length=255, description="Tên của Sector")
    description: Optional[str] = Field(None, description="Mô tả Sector")
    image: Optional[str] = Field(None, max_length=300, description="Đường dẫn hình ảnh của Sector")


class BrandCreateDTO(BaseModel):
    """DTO cho việc tạo mới Brand."""
    code: str = Field(..., max_length=50, description="Mã của Brand")
    name: str = Field(..., max_length=255, description="Tên của Brand")
    description: Optional[str] = Field(None, description="Mô tả Brand")
    image: Optional[str] = Field(None, max_length=300, description="Đường dẫn hình ảnh của Brand")


class BrandUpdateDTO(BaseModel):
    """DTO cho việc cập nhật Brand."""
    code: Optional[str] = Field(None, max_length=50, description="Mã của Brand")
    name: Optional[str] = Field(None, max_length=255, description="Tên của Brand")
    description: Optional[str] = Field(None, description="Mô tả Brand")
    image: Optional[str] = Field(None, max_length=300, description="Đường dẫn hình ảnh của Brand")


class MerchandiseTemplateCreateDTO(BaseModel):
    """DTO cho việc tạo mới MerchandiseTemplate."""
    code: str = Field(..., max_length=50, description="Mã của MerchandiseTemplate")
    name: str = Field(..., max_length=255, description="Tên của MerchandiseTemplate")
    sector_id: int = Field(..., description="ID của Sector liên kết")
    structure_json: dict = Field(..., description="Cấu trúc JSON của MerchandiseTemplate")


class MerchandiseTemplateUpdateDTO(BaseModel):
    """DTO cho việc cập nhật MerchandiseTemplate."""
    code: Optional[str] = Field(None, max_length=50, description="Mã của MerchandiseTemplate")
    name: Optional[str] = Field(None, max_length=255, description="Tên của MerchandiseTemplate")
    sector_id: Optional[int] = Field(None, description="ID của Sector liên kết")
    structure_json: Optional[str] = Field(None, description="Cấu trúc JSON của MerchandiseTemplate")


class MerchandiseCreateDTO(BaseModel):
    """DTO cho việc tạo mới Merchandise."""
    template_code: str = Field(..., description="Code của MerchandiseTemplate liên kết")
    brand_id: int = Field(..., description="ID của Brand liên kết")
    supplier_id: Optional[int] = Field(None, description="ID của Supplier liên kết")
    code: str = Field(..., description="Mã của Merchandise")
    name: str = Field(..., max_length=255, description="Tên của Merchandise")
    data_sheet_link: Optional[str] = Field(None, max_length=800, description="Đường dẫn tài liệu kỹ thuật")
    unit: str = Field(..., max_length=50, description="Đơn vị của Merchandise")
    description_in_contract: str = Field(..., description="Mô tả trong hợp đồng")
    description_in_quotation: str = Field(..., description="Mô tả trong báo giá")
    images: Optional[List[str]] = Field(None, description="Danh sách đường dẫn hình ảnh của Merchandise")
    data_json: dict = Field(..., description="Dữ liệu JSON của Merchandise")
    begin_price: float = Field(..., description="Giá khời đầu")
    


class MerchandiseUpdateDTO(BaseModel):
    """DTO cho việc cập nhật Merchandise."""
    template_id: Optional[int] = Field(None, description="ID của MerchandiseTemplate liên kết")
    brand_id: Optional[int] = Field(None, description="ID của Brand liên kết")
    code: Optional[int] = Field(None, description="Mã của Merchandise")
    name: Optional[str] = Field(None, max_length=255, description="Tên của Merchandise")
    data_sheet_link: Optional[str] = Field(None, max_length=800, description="Đường dẫn tài liệu kỹ thuật")
    unit: Optional[str] = Field(None, max_length=50, description="Đơn vị của Merchandise")
    description_in_contract: Optional[str] = Field(None, description="Mô tả trong hợp đồng")
    data_json: Optional[str] = Field(None, description="Dữ liệu JSON của Merchandise")


class PriceInfoCreateDTO(BaseModel):
    """DTO cho việc tạo mới PriceInfo."""
    merchandise_id: int = Field(..., description="ID của Merchandise liên kết")
    import_vat: float = Field(..., description="VAT nhập khẩu")
    sale_vat: float = Field(..., description="VAT bán hàng")
    import_price_non_vat: float = Field(..., description="Giá nhập không VAT")
    sale_price_non_vat: float = Field(..., description="Giá bán không VAT")


class PriceInfoUpdateDTO(BaseModel):
    """DTO cho việc cập nhật PriceInfo."""
    merchandise_id: Optional[int] = Field(None, description="ID của Merchandise liên kết")
    import_vat: Optional[float] = Field(None, description="VAT nhập khẩu")
    sale_vat: Optional[float] = Field(None, description="VAT bán hàng")
    import_price_non_vat: Optional[float] = Field(None, description="Giá nhập không VAT")
    sale_price_non_vat: Optional[float] = Field(None, description="Giá bán không VAT")
    

class UserCreateDTO(BaseModel):
    """DTO cho việc tạo mới User."""
    name: str = Field(..., max_length=50, description="Tên đăng nhập")
    password: str = Field(..., max_length=50, description="Mật khẩu")
    email: str = Field(..., max_length=255, description="Email")
    phone: str = Field(..., max_length=20, description="Số điện thoại")
    role_id: int = Field(..., description="Vai trò")

class UserUpdateDTO(BaseModel):
    """DTO cho việc cập nhật User."""
    username: Optional[str] = Field(None, max_length=50, description="Tên đăng nhập")
    password: Optional[str] = Field(None, max_length=50, description="Mật khẩu")
    full_name: Optional[str] = Field(None, max_length=255, description="Họ tên")
    email: Optional[str] = Field(None, max_length=255, description="Email")
    phone: Optional[str] = Field(None, max_length=20, description="Số điện thoại")
    role_id: Optional[int] = Field(None, max_length=50, description="Vai trò")
    
class NotificationDTO(BaseModel):
    """DTO cho việc tạo mới Notification."""
    title: str = Field(..., max_length=255, description="Tiêu đề thông báo")
    content: str = Field(..., description="Nội dung thông báo")
    user_id: int = Field(..., description="ID của User liên kết")
    is_read: bool = Field(..., description="Trạng thái đã đọc")
    created_at: str = Field(..., description="Thời gian tạo thông báo")

class SectorCreateDTO(BaseModel):
    """DTO cho việc tạo mới Sector."""
    code: str = Field(..., max_length=50, description="Mã của Sector")
    name: str = Field(..., max_length=255, description="Tên của Sector")
    description: Optional[str] = Field(None, description="Mô tả Sector")
    image: Optional[str] = Field(None, max_length=300, description="Đường dẫn hình ảnh của Sector")
    

class PreQuoteMerchandiseCreateDTO(BaseModel):
    """DTO cho việc tạo mới PreQuoteMerchandise."""
    merchandise_id: int = Field(..., description="ID của Merchandise liên kết")
    quantity: int = Field(..., description="Số lượng")
    price: float = Field(..., description="Giá trên đơn vị")
    gm: float = Field(..., description="GM")
    warranty_years: Optional[int] = Field(..., description="Thời gian bảo hành")
    
class ComboMerchandiseCreateDTO(BaseModel):
    """DTO cho việc tạo mới PreQuoteMerchandise."""
    merchandise_id: int = Field(..., description="ID của Merchandise liên kết")
    quantity: int = Field(..., description="Số lượng")
    price: float = Field(..., description="Giá trên đơn vị")
    gm: float = Field(..., description="GM")

class ComboCreateDTO(BaseModel):
    """DTO cho việc tạo mới Combo."""
    description: Optional[str] = Field(...,description="Mô tả")
    code: str = Field(..., description="Mã")
    name: str = Field(..., description="Tên")
    status: str = Field(..., description="Trạng thái")
    installation_type : str = Field(..., description="Loại lắp đặt")
    total_price: Optional[float] = Field(..., description="Tổng giá")
    kind : str = Field(..., description="Loại")
    
    image: Optional[str] = Field(..., description="Ảnh")
    
    list_pre_quote_merchandise: List[ComboMerchandiseCreateDTO] = Field(..., description="Danh sách PreQuoteMerchandise")
    
class PreQuoteCreateDTO(BaseModel):
    """DTO cho việc tạo mới báo giá khảo sát và báo giá chi tiết."""
    agent_id: Optional[int] = Field(...,description="ID của môi giới")
    phone: Optional[str] = Field(...,description="Số điện thoại của khách hàng tiềm năng")
    assumed_code: Optional[str] = Field(...,description="Mã giả định của khách hàng tiềm năng")
    customer_name: Optional[str] = Field(...,description="Tên của khách hàng")
    description: Optional[str] = Field(...,description="Mô tả")
    address: Optional[str] = Field(...,description="Địa chỉ chi tiết khách hàng")
    province: Optional[str] = Field(...,description="Tỉnh của khách hàng")
    district: Optional[str] = Field(...,description="Huyện của khách hàng")
    ward: Optional[str] = Field(...,description="Phường của khách hàng")
    code: str = Field(..., description="Mã")
    name: str = Field(..., description="Tên")
    status: str = Field(..., description="Trạng thái")
    installation_type : str = Field(..., description="Loại lắp đặt")
    total_price: Optional[float] = Field(..., description="Tổng giá")
    kind : str = Field(..., description="Loại")
    
    image: Optional[str] = Field(..., description="Ảnh")
    
    list_pre_quote_merchandise: List[ComboMerchandiseCreateDTO] = Field(..., description="Danh sách PreQuoteMerchandise")

class ContractCreateDTO(BaseModel):
    """DTO cho việc tạo mới PreQuote."""
    description: Optional[str] = Field(None, description="Ghi chú")
    code: str = Field(..., description="Mã")
    name: str = Field(..., description="Tên")
    customer_id: Optional[int] = Field(..., description="ID của khách hàng")
    sale_id: Optional[int] = Field(..., description="ID của nhân viên bán hàng")
    customer_code : Optional[str] = Field(..., description="Mã khách hàng")
    customer_name: Optional[str] = Field(..., description="Tên khách hàng")
    customer_address: Optional[str] = Field(..., description="Địa chỉ cụ thể khách hàng")
    customer_phone: Optional[str] = Field(..., description="Số điện thoại khách hàng")
    customer_email: Optional[str] = Field(..., description="Email khách hàng")
    customer_tax_code: Optional[str] = Field(..., description="Mã số thuế khách hàng")
    customer_province: Optional[str] = Field(..., description="Tỉnh của khách hàng")
    customer_district: Optional[str] = Field(..., description="Huyện của khách hàng")
    customer_ward: Optional[str] = Field(..., description="Phường của khách hàng")
    customer_gender: Optional[bool] = Field(..., description="Giới tính của khách hàng")
    status: Optional[str] = Field(..., description="Trạng thái")
    installation_type : str = Field(..., description="Loại lắp đặt")
    total_price: Optional[float] = Field(..., description="Tổng giá trị đơn hàng")
    kind : str = Field(..., description="Loại")
    created_at: datetime = Field(..., description="Ngày lắp đặt")
    image: Optional[str] = Field(..., description="Ảnh")
    
    list_pre_quote_merchandise: List[PreQuoteMerchandiseCreateDTO] = Field(..., description="Danh sách PreQuoteMerchandise")
    


    
class CustomerCreateDTO(BaseModel):
    """DTO cho việc tạo mới Customer."""
    code: Optional[str] = Field(..., max_length=50, description="Mã của Customer")
    name: Optional[str] = Field(..., max_length=255, description="Tên của Customer")
    address: Optional[str] = Field(..., description="Địa chỉ của Customer")
    phone: Optional[str] = Field(..., max_length=20, description="Số điện thoại của Customer")
    email: Optional[str] = Field(..., max_length=255, description="Email của Customer")
    tax_code: Optional[str] = Field(..., max_length=50, description="Mã số thuế của Customer")
    citizen_id: Optional[str] = Field(..., max_length=50, description="Số CMND của Customer")
    gender: Optional[str] = Field(..., description="Giới tính của Customer")
    user_id: Optional[int] = Field(..., description="ID của User liên kết")
    created_at: Optional[datetime] = Field(..., description="Thời gian tạo Customer")
    description: Optional[str] = Field(None, description="Mô tả của Customer")


class ContentCategoryCreateDTO(BaseModel):
    """DTO cho việc tạo mới ContentCategory."""
    code: str = Field(..., max_length=50, description="Mã của ContentCategory")
    name: str = Field(..., max_length=255, description="Tên của ContentCategory")
    description: Optional[str] = Field(None, description="Mô tả của ContentCategory")
    
    
class MediaContentCreateDTO(BaseModel):
    """DTO cho việc tạo mới MediaContent."""
    title: Optional[str] = Field(None, description="Tiêu đề của MediaContent")
    kind: str = Field(..., description="Loại media")
    link: str = Field(..., description="Đường dẫn media")

class ContentCreateDTO(BaseModel):
    """DTO cho việc tạo mới Content."""
    title: Optional[str] = Field(..., max_length=250, description="Tiêu đề nội dung")
    content_category_id: int = Field(..., description="ID của ContentCategory liên kết")
    hashtag: Optional[str] = Field(None, description="Hashtag của Content")
    content: Optional[str] = Field(None, description="Nội dung của Content")
    
    media_contents: List[MediaContentCreateDTO] = Field(..., description="Danh sách MediaContent")

class PotentialCustomerCreateDTO(BaseModel):
    """DTO cho việc tạo khách hàng tiềm năng mới"""
    agent_id: Optional[int] = Field(...,description="ID của môi giới")
    assumed_code: Optional[str] = Field(...,description="Mã giả định của khách hàng")
    name: Optional[str] = Field(...,description="Tên của khách hàng")
    phone: Optional[str] = Field(...,description="Số điện thoại khách hàng")
    gender: Optional[bool] = Field(...,description="Giới tính khách hàng")
    email: Optional[str] = Field(...,description="Email của khách hàng")
    address: Optional[str] = Field(...,description="Địa chỉ chi tiết khách hàng")
    province: Optional[str] = Field(...,description="Tỉnh của khách hàng")
    district: Optional[str] = Field(...,description="Huyện của khách hàng")
    ward: Optional[str] = Field(...,description="Phường của khách hàng")
    interested_in_combo_id: Optional[int] = Field(...,description="ID của combo quan tâm")
    description: Optional[str] = Field(...,description="Nội dung chi tiết")