import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model.model import get_db
from app.repository.model_repo import MerchandiseTemplateRepository
from app.repository.model_repo import  PreQuoteRepository, PreQuoteMerchandiseRepository, CustomerRepository, UserRepository, CommissionRepository
from app.model.dto import ContractCreateDTO, PreQuoteMerchandiseCreateDTO, ComboCreateDTO
from typing import List
import traceback




router = APIRouter()

@router.get("/pre_quote/get_one/{id}", response_model=dict)
def get_pre_quote(id: int, db: Session = Depends(get_db)):
    print('id', id)
    """Lấy thông tin combo."""
    combo = PreQuoteRepository.get_pre_quote_by_id(db, id)
    if not combo:
        raise HTTPException(status_code=404, detail="Combo not found")
    combo_dict = combo.__dict__.copy()
    combo_dict["pre_quote_merchandises"] = []
    for pre_quote_merchandise in combo.pre_quote_merchandises:
        pre_quote_merchandise_dict = pre_quote_merchandise.__dict__.copy()
        merchandise_dict = pre_quote_merchandise.merchandise.__dict__.copy()
        merchandise_dict.pop("_sa_instance_state", None)
        merchandise_dict["data_json"] = json.loads(merchandise_dict["data_json"])
        pre_quote_merchandise_dict["merchandise"] = merchandise_dict
        pre_quote_merchandise_dict["merchandise"].pop("_sa_instance_state", None)
        pre_quote_merchandise_dict.pop("_sa_instance_state", None)
        combo_dict["pre_quote_merchandises"].append(pre_quote_merchandise_dict)
    if(combo.customer):
        combo_dict["customer"] = combo.customer.__dict__.copy()
        combo_dict["customer"].pop("_sa_instance_state", None)
    combo_dict.pop("_sa_instance_state", None)
    return combo_dict

@router.post("/pre_quote/combo", response_model=dict)
def create_combo(pre_quote_data: ComboCreateDTO, db: Session = Depends(get_db)):
    """Tạo combo mới."""
    total_price = 0
    try:
        # Bắt đầu giao dịch
        with db.begin():
            # Tạo mới combo
            newCombo = PreQuoteRepository.create_pre_quote(db, pre_quote_data={
                "code": pre_quote_data.code,
                "name": pre_quote_data.name,
                "status": pre_quote_data.status,
                "installation_type": pre_quote_data.installation_type,
                "total_price": pre_quote_data.total_price,
                "kind": "combo",
                "description": pre_quote_data.description,
                "image": pre_quote_data.image
            })

            if not newCombo:
                raise HTTPException(status_code=400, detail="Mã combo bị trùng lặp")

            # Xử lý danh sách pre_quote_merchandises
            for pre_quote_merchandise in pre_quote_data.list_pre_quote_merchandise:
                total_price += pre_quote_merchandise.price * pre_quote_merchandise.quantity * (100 + pre_quote_merchandise.gm) / 100
                PreQuoteMerchandiseRepository.create_pre_quote_merchandise(db, {
                    "pre_quote_id": newCombo.id,
                    "merchandise_id": pre_quote_merchandise.merchandise_id,
                    "quantity": pre_quote_merchandise.quantity,
                    "price": pre_quote_merchandise.price,
                    "gm": pre_quote_merchandise.gm
                })

            # Cập nhật total_price nếu cần
            if pre_quote_data.total_price != None and pre_quote_data.total_price != 0.0:
                total_price = pre_quote_data.total_price
            PreQuoteRepository.update_pre_quote(db, newCombo.id, {"total_price": total_price})

        # Nếu không có lỗi, trả về kết quả thành công
        return {"message": "Combo created successfully"}
    except Exception as e:
        # Rollback sẽ tự động được thực hiện bởi `db.begin()` nếu có lỗi
        print("HTTPException occurred:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create combo: {str(e)}")
@router.post("/pre_quote/contract_quote/old", response_model=dict)
def create_contract_quote(pre_quote_data: ContractCreateDTO, db: Session = Depends(get_db)):
    """Tạo hợp đồng mới với cơ chế rollback nếu có lỗi."""
    total_price = 0
    customer = None

    try:
        # Bắt đầu giao dịch
        with db.begin():
            # Tạo khách hàng nếu chưa có
            if pre_quote_data.customer_id is None:
                try:
                    finding_customer = CustomerRepository.get_customer_by_code(db, code = pre_quote_data.customer_code)
                    if not finding_customer:
                        customer = CustomerRepository.create_customer(db, {
                        "name": pre_quote_data.customer_name,
                        "address": pre_quote_data.customer_address,
                        "code": pre_quote_data.customer_code,
                        "user_id": pre_quote_data.sale_id,
                        "phone": pre_quote_data.customer_phone,
                        "email": pre_quote_data.customer_email,
                        "tax_code": pre_quote_data.customer_tax_code,
                        "province": pre_quote_data.customer_province,
                        "district": pre_quote_data.customer_district,
                        "ward": pre_quote_data.customer_ward,
                        "gender": pre_quote_data.customer_gender
                        })
                        if not customer:
                            raise HTTPException(status_code=500, detail="Failed to create customer")
                        pre_quote_data.customer_id = customer.id
                    if finding_customer:
                        pre_quote_data.customer_id = finding_customer.id
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error creating customer: {str(e)}")
            
            finding_customer_account = None
            try:
                    finding_customer_account = UserRepository.get_user_by_phone(db,phone=pre_quote_data.customer_phone)
                    if not finding_customer_account:
                        newUser = UserRepository.create_user(db, {
                        "role_id": 3,
                        "name": pre_quote_data.customer_name,
                        "email": pre_quote_data.customer_email,
                        "phone": pre_quote_data.customer_phone,
                        "password": "123",
                        "parent_id": pre_quote_data.sale_id,
                        "total_commission": 0,
                        "commission_rate": 0,
                        "address": pre_quote_data.customer_address,
                        "tax_code": pre_quote_data.customer_tax_code,
                    })
                        if not newUser:
                            raise HTTPException(status_code=500, detail="Failed to create user")
            except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

            # Tạo PreQuote
            try:
                buyer_id = None
                if finding_customer_account != None:
                    buyer_id = finding_customer_account.id
                newCombo = PreQuoteRepository.create_pre_quote(db, pre_quote_data={
                    "customer_id": pre_quote_data.customer_id,
                    "code": pre_quote_data.code,
                    "name": pre_quote_data.name,
                    "status": 'accepted',
                    "installation_type": pre_quote_data.installation_type,
                    "total_price": pre_quote_data.total_price,
                    "kind": pre_quote_data.kind,
                    "description": pre_quote_data.description,
                    "image": pre_quote_data.image,
                    "created_at": pre_quote_data.created_at,
                    "buyer_id": buyer_id
                })
                if not newCombo:
                    raise HTTPException(status_code=500, detail="Failed to create PreQuote")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error creating PreQuote: {str(e)}")

            # Tạo PreQuoteMerchandise
            try:
                for pre_quote_merchandise in pre_quote_data.list_pre_quote_merchandise:
                    total_price += pre_quote_merchandise.price * pre_quote_merchandise.quantity * (100 + pre_quote_merchandise.gm) / 100
                    PreQuoteMerchandiseRepository.create_pre_quote_merchandise(db, {
                        "pre_quote_id": newCombo.id,
                        "merchandise_id": pre_quote_merchandise.merchandise_id,
                        "quantity": pre_quote_merchandise.quantity,
                        "price": pre_quote_merchandise.price,
                        "warranty_years": pre_quote_merchandise.warranty_years
                    })
            except Exception as e:
                print("HTTPException occurred:")
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Error creating PreQuoteMerchandise: {str(e)}")

            # Cập nhật total_price nếu cần
            if pre_quote_data.total_price != None and pre_quote_data.total_price != 0.0:
                total_price = pre_quote_data.total_price
            PreQuoteRepository.update_pre_quote(db, newCombo.id, {"total_price": total_price})

            # Cập nhật thông tin hoa hồng cho user
            
            # try:
            #     customer = CustomerRepository.get_customer_by_id(db, newCombo.customer_id)
            #     user = UserRepository.get_user_by_id(db, pre_quote_data.sale_id)
            #     UserRepository.update_user(db, customer.user_id, {
            #         "total_commission": user.total_commission + total_price * user.commission_rate / 100
            #     })
            #     if user.parent_id is not None:
            #         parent = UserRepository.get_user_by_id(db, user.parent_id)
            #         UserRepository.update_user(db, user.parent_id, {
            #             "total_commission": parent.total_commission + total_price / 100
            #         })
            # except Exception as e:
            #     raise HTTPException(status_code=500, detail=f"Error updating user commission: {str(e)}")

            # Tạo user mới nếu cần
            
            
                
        # Nếu không có lỗi, trả về kết quả thành công
        return {"message": "Contract created successfully"}

    except HTTPException as http_exc:
        # Rollback sẽ tự động được thực hiện bởi `db.begin()` nếu có lỗi
        #in lỗi ra terminal
        print("HTTPException occurred:")
        traceback.print_exc()
        raise http_exc
    except Exception as e:
        # Rollback sẽ tự động được thực hiện bởi `db.begin()` nếu có lỗi
        print("HTTPException occurred:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.post("/pre_quote/contract_quote/new", response_model=dict)
def create_contract_quote_new(pre_quote_data: ContractCreateDTO, db: Session = Depends(get_db)):
    """Tạo hợp đồng mới với cơ chế rollback nếu có lỗi."""
    total_price = 0
    customer = None

    try:
        # Bắt đầu giao dịch
        with db.begin():
            # Tạo khách hàng nếu chưa có
            finding_customer = None
            if pre_quote_data.customer_id is None:
                try:
                    finding_customer = CustomerRepository.get_customer_by_code(db, code = pre_quote_data.customer_code)
                    if not finding_customer:
                        customer = CustomerRepository.create_customer(db, {
                        "name": pre_quote_data.customer_name,
                        "address": pre_quote_data.customer_address,
                        "code": pre_quote_data.customer_code,
                        "user_id": pre_quote_data.sale_id,
                        "phone": pre_quote_data.customer_phone,
                        "email": pre_quote_data.customer_email,
                        "tax_code": pre_quote_data.customer_tax_code,
                        "province": pre_quote_data.customer_province,
                        "district": pre_quote_data.customer_district,
                        "ward": pre_quote_data.customer_ward,
                        "gender": pre_quote_data.customer_gender
                        })
                        if not customer:
                            raise HTTPException(status_code=500, detail="Failed to create customer")
                        pre_quote_data.customer_id = customer.id
                    if finding_customer:
                        pre_quote_data.customer_id = finding_customer.id
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error creating customer: {str(e)}")
                
            
            # Tạo user mới nếu cần
            finding_customer_account = None
            try:
                    finding_customer_account = UserRepository.get_user_by_phone(db,phone=pre_quote_data.customer_phone)
                    if not finding_customer_account:
                        newUser = UserRepository.create_user(db, {
                        "role_id": 3,
                        "name": pre_quote_data.customer_name,
                        "email": pre_quote_data.customer_email,
                        "phone": pre_quote_data.customer_phone,
                        "password": "123",
                        "parent_id": pre_quote_data.sale_id,
                        "total_commission": 0,
                        "commission_rate": 0,
                        "address": pre_quote_data.customer_address,
                        "tax_code": pre_quote_data.customer_tax_code
                    })
                        finding_customer_account = newUser
                        if not newUser:
                            raise HTTPException(status_code=500, detail="Failed to create user")
            except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

            # Tạo PreQuote
            newCombo = None
            try:
                buyer_id = None
                if finding_customer_account != None:
                    buyer_id = finding_customer_account.id
                newCombo = PreQuoteRepository.create_pre_quote(db, pre_quote_data={
                    "customer_id": pre_quote_data.customer_id,
                    "code": pre_quote_data.code,
                    "name": pre_quote_data.name,
                    "status": 'accepted',
                    "installation_type": pre_quote_data.installation_type,
                    "total_price": pre_quote_data.total_price,
                    "kind": pre_quote_data.kind,
                    "description": pre_quote_data.description,
                    "image": pre_quote_data.image,
                    "created_at": pre_quote_data.created_at,
                    "buyer_id": buyer_id
                })
                if not newCombo:
                    raise HTTPException(status_code=500, detail="Failed to create PreQuote")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error creating PreQuote: {str(e)}")

            # Tạo PreQuoteMerchandise
            try:
                for pre_quote_merchandise in pre_quote_data.list_pre_quote_merchandise:
                    total_price += pre_quote_merchandise.price * pre_quote_merchandise.quantity * (100 + pre_quote_merchandise.gm) / 100
                    PreQuoteMerchandiseRepository.create_pre_quote_merchandise(db, {
                        "pre_quote_id": newCombo.id,
                        "merchandise_id": pre_quote_merchandise.merchandise_id,
                        "quantity": pre_quote_merchandise.quantity,
                        "price": pre_quote_merchandise.price,
                        "warranty_years": pre_quote_merchandise.warranty_years
                    })
            except Exception as e:
                print("HTTPException occurred:")
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Error creating PreQuoteMerchandise: {str(e)}")

            # Cập nhật total_price nếu cần
            if pre_quote_data.total_price != None and pre_quote_data.total_price != 0.0:
                total_price = pre_quote_data.total_price
            PreQuoteRepository.update_pre_quote(db, newCombo.id, {"total_price": total_price})

            # Cập nhật thông tin hoa hồng cho user
            
            try:
                customer = CustomerRepository.get_customer_by_id(db, newCombo.customer_id)
                user = UserRepository.get_user_by_id(db, pre_quote_data.sale_id)
                UserRepository.update_user(db, customer.user_id, {
                    "total_commission": user.total_commission + total_price * user.commission_rate / 100
                })
                CommissionRepository.create_commission(db=db, commission_data = {
                    "money": total_price * user.commission_rate / 100,
                    "seller": user.id,
                    "sector_id": 1
                })
                if user.parent_id !=None:
                    parent = UserRepository.get_user_by_id(db, user.parent_id)
                    UserRepository.update_user(db, user.parent_id, {
                        "total_commission": parent.total_commission + total_price / 100
                    })
                    CommissionRepository.create_commission(db=db, commission_data = {
                    "money": total_price / 100,
                    "seller": parent.id,
                    "sector_id": 1
                    })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error updating user commission: {str(e)}")

            
                
        # Nếu không có lỗi, trả về kết quả thành công
        return {"message": "Contract created successfully"}

    except HTTPException as http_exc:
        # Rollback sẽ tự động được thực hiện bởi `db.begin()` nếu có lỗi
        #in lỗi ra terminal
        print("HTTPException occurred:")
        traceback.print_exc()
        raise http_exc
    except Exception as e:
        # Rollback sẽ tự động được thực hiện bởi `db.begin()` nếu có lỗi
        print("HTTPException occurred:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/pre_quote/combo", response_model=List[dict])
def get_all_combo(db: Session = Depends(get_db)):
    """Lấy danh sách combo."""
    combos = PreQuoteRepository.get_pre_quotes_by_kind(db, "combo")
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
    
    return combos_dict

@router.get("/pre_quote/combo/best_selling", response_model=List[dict])
def get_all_combo(db: Session = Depends(get_db)):
    """Lấy danh sách combo."""
    combos = PreQuoteRepository.get_best_selling_combos(db)
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
    
    return combos_dict

@router.get("/pre_quote/contract_quote/{buyer_id}", response_model=List[dict])
def get_all_combo(buyer_id:int,db: Session = Depends(get_db)):
    """Lấy danh sách combo."""
    combos = PreQuoteRepository.get_contract_quote_by_buyer_id_and_sector(db=db,buyer_id=buyer_id,sector="SLM")
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
    
    return combos_dict

@router.get("/pre_quote/contracts/{user_id}", response_model=List[dict])
def get_all_combo(user_id:int,db: Session = Depends(get_db)):
    """Lấy danh sách combo."""
    combos = PreQuoteRepository.get_pre_quotes_by_kind(db, "contract_quote")
    # Lọc combo mà có customer.user_id = user_id
    combos = [combo for combo in combos if combo.customer and combo.customer.user_id == user_id]
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
    
    return combos_dict

@router.get("/pre_quote/combo/{id}", response_model=dict)
def get_combo_by_id(id:int,db: Session = Depends(get_db)):
    merchandise_templates = MerchandiseTemplateRepository.get_all_merchandise_templates
    combo = PreQuoteRepository.get_pre_quote_by_id(db=db,pre_quote_id=id)
    if not combo:
        raise HTTPException(status_code=404, detail="Combo not found")

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
        merchandise_template_dict = pre_quote_merchandise.merchandise.template.__dict__.copy()
        merchandise_template_dict.pop("_sa_instance_state", None)
        merchandise_dict["template"] = merchandise_template_dict
        pre_quote_merchandise_dict["merchandise"] = merchandise_dict
        pre_quote_merchandise_dict["merchandise"].pop("_sa_instance_state", None)
        pre_quote_merchandise_dict.pop("_sa_instance_state", None)
        combo_dict["pre_quote_merchandises"].append(pre_quote_merchandise_dict)

    if combo.customer:
        combo_dict["customer"] = combo.customer.__dict__.copy()
        combo_dict["customer"].pop("_sa_instance_state", None)

    combo_dict.pop("_sa_instance_state", None)
    # Nhóm pre_quote_merchandise theo merchandise_templates
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
    return combo_dict



@router.get("/pre_quote/combo/installation_type/{installation_type}", response_model=List[dict])
def get_combo_by_installation_type(installation_type: str, db: Session = Depends(get_db)):
    """Lấy danh sách combo theo loại lắp đặt."""
    combos = PreQuoteRepository.get_pre_quotes_by_kind_and_installation_type(db, "combo", installation_type)
    combos_dict = []

    for combo in combos:
        combo_dict = {
            "id": combo.id,
            "code": combo.code,
            "name": combo.name,
            "description": combo.description,
            "total_price": combo.total_price,
            "kind": combo.kind,
            "status": combo.status,
            "customer": {
                "id": combo.customer.id,
                "name": combo.customer.name,
                "address": combo.customer.address,
                "phone": combo.customer.phone,
                "email": combo.customer.email,
            } if combo.customer else None,
            "pre_quote_merchandises": [
                {
                    "id": pre_quote_merchandise.id,
                    "quantity": pre_quote_merchandise.quantity,
                    "price": pre_quote_merchandise.price,
                    "merchandise": {
                        "id": pre_quote_merchandise.merchandise.id,
                        "name": pre_quote_merchandise.merchandise.name,
                        "data_json": json.loads(pre_quote_merchandise.merchandise.data_json)
                    }
                } for pre_quote_merchandise in combo.pre_quote_merchandises
            ]
        }
        combos_dict.append(combo_dict)
    return combos_dict
