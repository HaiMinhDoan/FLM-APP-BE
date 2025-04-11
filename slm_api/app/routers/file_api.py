import json
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app.model.model import get_db
from app.repository.model_repo import MerchandiseTemplateRepository
from app.repository.model_repo import  PreQuoteRepository, PreQuoteMerchandiseRepository, CustomerRepository, UserRepository, CommissionRepository, ElectricPriceRepository
from app.model.dto import ContractCreateDTO, PreQuoteMerchandiseCreateDTO, ComboCreateDTO
from typing import List
import traceback
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pdfkit
templates = Jinja2Templates(directory="app/templates")
config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
options = {
    'no-stop-slow-scripts': None
}
router = APIRouter()


@router.get("/file/pre_quote_detail/{pre_quote_id}", response_class=HTMLResponse)
def generate_pre_quote_detail_pdf(pre_quote_id:int,request: Request, db: Session = Depends(get_db)):
    """API lấy file pdf chi tiết báo giá."""
    combo = PreQuoteRepository.get_pre_quote_by_id_with_brand(db, pre_quote_id=pre_quote_id)
    el_price = 3000
    electric_price = ElectricPriceRepository.get_electric_price_by_id(db=db, electric_price_id=1)
    storage_capacity_kwh = 0.0
    check_add_storage_capacity_kwh = False
    if electric_price:
        el_price = electric_price.price
    if not combo:
        raise HTTPException(status_code=404, detail="Combo not found")
    # Sắp xếp pre_quote_merchandises theo thứ tự tăng dần id
    combo.pre_quote_merchandises = sorted(combo.pre_quote_merchandises, key=lambda x: x.id)
    combo_dict = combo.__dict__.copy()
    combo_dict["payback_period"] = combo.total_price/((combo.output_max+combo.output_min)/2*el_price*12)
    # Xử lý danh sách pre_quote_merchandises
    combo_dict["pre_quote_merchandises"] = []
    for pre_quote_merchandise in combo.pre_quote_merchandises:
        pre_quote_merchandise_dict = pre_quote_merchandise.__dict__.copy()
        pre_quote_merchandise_dict["price_on_gm"] = pre_quote_merchandise_dict["price"]/(1-pre_quote_merchandise_dict["gm"]/100)
        merchandise_dict = pre_quote_merchandise.merchandise.__dict__.copy()
        merchandise_dict.pop("_sa_instance_state", None)
        merchandise_dict["data_json"] = json.loads(merchandise_dict["data_json"])
        if pre_quote_merchandise.merchandise.template.code == "BATTERY_STORAGE" and (not check_add_storage_capacity_kwh):
            storage_capacity_kwh = merchandise_dict["data_json"]["storage_capacity_kwh"]
            check_add_storage_capacity_kwh = True
        images = pre_quote_merchandise.merchandise.images
        images_dict = []
        for image in images:
            image_dict = image.__dict__.copy()
            image_dict.pop("_sa_instance_state", None)
            images_dict.append(image_dict)
        merchandise_dict["images"] = images_dict.copy()
        pre_quote_merchandise.merchandise.template.structure_json = None
        merchandise_template_dict = pre_quote_merchandise.merchandise.template.__dict__.copy()
        merchandise_template_dict.pop("_sa_instance_state", None)
        merchandise_dict["template"] = merchandise_template_dict
        pre_quote_merchandise_dict["merchandise"] = merchandise_dict
        pre_quote_merchandise_dict["merchandise"].pop("_sa_instance_state", None)
        pre_quote_merchandise_dict.pop("_sa_instance_state", None)
        combo_dict["pre_quote_merchandises"].append(pre_quote_merchandise_dict)
                
    grouped_merchandises = {}
    for pre_quote_merchandise in combo_dict["pre_quote_merchandises"]:
        template_id = pre_quote_merchandise["merchandise"]["template"]["id"]
        if template_id not in grouped_merchandises:
            grouped_merchandises[template_id] = {
                "template": pre_quote_merchandise["merchandise"]["template"],
                "pre_quote_merchandises": []
            }
        grouped_merchandises[template_id]["pre_quote_merchandises"].append(pre_quote_merchandise)

    combo_dict["grouped_merchandises"] = list(grouped_merchandises.values())
    #sắp xếp combo_dict["grouped_merchandises"] them template.id
    combo_dict["grouped_merchandises"] = sorted(
        combo_dict["grouped_merchandises"], key=lambda x: x["template"]["id"]
    )
    combo_dict["pre_quote_merchandises"] =[]
    combo_dict.pop("_sa_instance_state", None)
    
    power = 0
    for grouped_merchandises_dict in combo_dict["grouped_merchandises"]:
        if(grouped_merchandises_dict["template"]["code"] == "PIN_PV"):
            power += grouped_merchandises_dict["pre_quote_merchandises"][0]["merchandise"]["data_json"]["power_watt"]*grouped_merchandises_dict["pre_quote_merchandises"][0]["quantity"]/1000
    # làm tròn lên power theo đúng quy tắc làm tròn  lên và xuống tới hàng đơn vị
    power = round(power, 0)
    phase_type = ""
    if combo_dict["phase_type"] == "3-phase":
        phase_type = "3 pha"
    elif combo_dict["phase_type"] == "1-phase":
        phase_type = "1 pha"
    elif combo_dict["phase_type"] == "3-phase high voltage":
        phase_type = "3 pha áp cao"
    elif combo_dict["phase_type"] == "3-phase low voltage":
        phase_type = "3 pha áp thấp"
    
    
    params = {
        "request": request,
        "phase_type" : phase_type,
        "power" : power,
        "combo": combo_dict,
        "storage_capacity_kwh" : storage_capacity_kwh
    }
    html_content = templates.TemplateResponse("bao_gia_chi_tiet.html", params).body.decode()
    # Chuyển đổi HTML sang PDF
    pdf = pdfkit.from_string(html_content, verbose=False,configuration=config, options=options)  # False để không lưu file
    # Trả về file PDF cho người dùng tải
    return Response(pdf, media_type='application/pdf', headers={"Content-Disposition": "attachment; filename=quote.pdf"})
    