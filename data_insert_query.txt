
insert  into sectors (code,name)
values('SLM','Solarmax');

INSERT INTO merchandise_templates (code, name, sector_id, structure_json)
VALUES 
    ('PIN_PV', 'Solar Panel', 1, '{
        "power_watt": "",
        "width_mm": "",
        "height_mm": "",
        "thickness_mm": "",
        "area_m2": "",
        "weight_kg": "",
        "technology": "",
        "warranty_years": ""
    }');

   INSERT INTO merchandise_templates (
    code, name, sector_id, structure_json
) VALUES (
    'INVERTER_DC_AC', 'INVERTER DC-AC', 1, 
    '{
        "ac_power_kw": {"type": "number", "unit": "kW"},
        "dc_max_power_kw": {"type": "number", "unit": "kW"},
        "installation_type": {"type": "select", "options": ["Ongrid", "Hybrid"]},
        "phase_type": {"type": "select", "options": ["1-phase", "3-phase high voltage", "3-phase low voltage"]},
        "brand_ranking": {"type": "number"}
    }'
);

INSERT INTO merchandise_templates (
    code, name, sector_id, structure_json
) VALUES (
    'BATTERY_STORAGE', 'Pin Lưu Trữ', 1, 
    '{
        "storage_capacity_kwh": {"type": "number", "unit": "kWh"},
        "max_upgrade_kwh": {"type": "number", "unit": "kWh"},
        "installation_type": {"type": "select", "options": ["1-phase", "3-phase high voltage", "3-phase low voltage"]},
        "cell_brand": {"type": "text", "max_length": 80},
        "installation_method": {"type": "text"}
    }'
);

   INSERT INTO merchandise_templates (
    code, name, sector_id, structure_json
) VALUES (
    'ALUMINUM_FRAME', 'Hệ Khung Giá Đỡ Nhôm Cao Cấp', 1, 
    '{
        "installation_type": {"type": "select", "options": ["Áp mái tôn", "Mái ngói", "Khung sắt"]}
    }'
);

INSERT INTO merchandise_templates (
    code, name, sector_id, structure_json
) VALUES (
    'DC_AC_CABLE', 'Hệ Dây Điện DC-AC', 1, 
    '{
        "phase_type": {"type": "select", "options": ["1-phase", "3-phase high voltage", "3-phase low voltage"]},
        "cable_size_mm2": {"type": "select", "options": ["6", "10", "16", "25", "35", "50", "70"]}
    }'
);

INSERT INTO merchandise_templates (
    code, name, sector_id, structure_json
) VALUES (
    'SOLAR_PANEL_CABINET', 'Tủ Điện NLMT', 1, 
    '{
        "installation_type": {"type": "select", "options": ["Ongrid", "Hybrid"]},
        "phase_type": {"type": "select", "options": ["1-phase", "3-phase high voltage", "3-phase low voltage"]},
        "power_capacity_kw": {"type": "number", "unit": "kW"}
    }'
);

INSERT INTO merchandise_templates (
    code, name, sector_id, structure_json
) VALUES (
    'GROUNDING_SYSTEM', 'Hệ Tiếp Địa', 1, 
    '{
        "wire_diameter_mm": {"type": "select", "options": ["4", "6", "10", "16", "25", "35", "50", "70"], "unit": "mm"}
    }'
);
INSERT INTO merchandise_templates (
    code, name, sector_id, structure_json
) VALUES (
    'INSTALLATION_PACKAGE', 'Trọn Gói Lắp Đặt', 1, 
    '{
        "installation_power_kwp": {"type": "number", "unit": "kWp"},
        "price_vnd": {"type": "number", "format": "###,###,###", "unit": "VND"}
    }'
);

insert into brands (code,name)
values('JA_SOLAR','JA Solar');

insert into brands (code,name)
values('SOLIS','Solis');

insert into brands (code,name)
values('DYNESS','Dyness');

insert into brands (code,name)
values('SLM','SLM');

insert into brands (code,name)
values('VIET_NAM','Việt Nam');

insert into brands (code,name)
values('PN_Tech_Leader','PN Tech/ Leader');

insert into brands (code,name)
values('CADIVI','Cadivi');

   INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    1, 1, NULL, 'JA_Solar_610W', 'JA Solar 610W', 
    'https://drive.google.com/file/d/1e_0L3t46ThcxOX_2bebBuuRVOORqHELk/view?usp=sharing',
    'pcs', 
    'Tấm pin mặt trời JA Solar 610Wp mới 100%. Top 1 thế giới về hiệu suất và thương hiệu. Hiệu suất 25 năm đạt trên 80%', 
    '{
        "power_watt": "610",
        "width_mm": "1134",
        "height_mm": "2382",
        "thickness_mm": "30",
        "area_m2": "2.70",
        "weight_kg": "33.1",
        "technology": "N-Type",
        "warranty_years": "10",
        "price_vnd": "1647000"
    }',
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    2, 1, NULL, 'INVERTER_SOLIS_S6_EHIP_5K_L_PRO', 'INVERTER Solis S6-EHIP-5K-L-PRO', 
    'https://drive.google.com/file/d/1-nL7l7Xxcv-Ft7_X8bX0gUnOFURzaf11/view?usp=sharing', 
    'Bộ', 
    'Inverter Solis 5KW, Hybrid 1 pha, 2 chuỗi MPPT, STRINGS cho hiệu suất cao 96.9% (Tiêu chuẩn EU 96.5%), Top 3 thế giới về thương hiệu Inverter, Cấp độ bảo vệ: IP66, Công suất DC max: 10kWp, Đã bao gồm Meter và CT chống phát ngược lưới', 
    '{
        "ac_power_kw": 5,
        "dc_max_power_kw": 10,
        "installation_type": "Hybrid",
        "phase_type": "1-phase",
        "brand_ranking": 3
    }',
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    2, 1, NULL, 'INVERTER_SOLIS_DATA_LOGGER', 'INVERTER Solis Data Logger', 
    NULL, 
    'Bộ', 
    'Bộ ghi dữ liệu Biến tần, Giám sát hoạt động của việc lắp đặt năng lượng mặt trời, Lưu trữ dữ liệu', 
    '{
        "ac_power_kw": 0,
        "dc_max_power_kw": 0,
        "installation_type": "Hybrid",
        "phase_type": "1-phase",
        "brand_ranking": 2
    }',
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    3, 3, NULL, 'PIN_LITHIUM_DYNESS_BX_51100', 'PIN LITHIUM Dyness BX 51100', 
    'https://drive.google.com/file/d/1Buh47oKxYg2CM_M-VOOT2BEqHKYQfxh/view?usp=sharing', 
    'Bộ', 
    'Pin Lithium Dyness 51,2V-100Ah-5,12kWh. Cell Pin từ hãng BYD - Top 4 thế giới về thương hiệu Cell Pin. 
     Bản tiêu chuẩn - màn trắng đen - Rack IP20. Nâng cấp tối đa 30 thiết bị ghép song song.', 
    '{
        "storage_capacity_kwh": 5.12,
        "max_upgrade_kwh": 153.6,
        "installation_type": "1-phase/3-phase low voltage",
        "cell_brand": "BYD",
        "installation_method": "Treo tường/Đặt đứng"
    }',
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    3, 4, NULL, 'PIN_LITHIUM_DAY_TU', 'PIN LITHIUM Dây từ', 
    NULL, 
    'Bộ', 
    'Dây từ nối Pin Lithium lên Inverter đã bấm sẵn đầu cốt.', 
    '{
        "storage_capacity_kwh": null,
        "max_upgrade_kwh": null,
        "installation_type": "3-phase high voltage",
        "cell_brand": null,
        "installation_method": "Dây từ nối"
    }',
    NOW(), TRUE
);
INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active 
) VALUES (
    3, 5, NULL, 'PIN_LITHIUM_DAY_MANG', 'PIN LITHIUM Dây mạng', 
    NULL, 
    'Bộ', 
    'Dây mạng phụ hiệu giao tiếp Inverter - Pin.', 
    '{
        "storage_capacity_kwh": null,
        "max_upgrade_kwh": null,
        "installation_type": "3-phase high voltage",
        "cell_brand": null,
        "installation_method": "Dây mạng phụ"
    }',
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    4, 5, NULL, 'HE_KHUNG_GIA_DO_NHOM_KEP_BIEN_30', 'HỆ KHUNG GIÁ ĐỠ NHÔM Kẹp biên 30', 
    NULL, 
    'Cái', 
    'Kẹp biên PIN năng lượng mặt trời.', 
    '{
        "installation_type": "Tất cả các loại mái",
        "material": "Nhôm cao cấp",
        "size": "30mm",
        "usage": "Cố định pin năng lượng mặt trời"
    }',
    NOW(), TRUE
);
INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    4, 5, NULL, 'HE_KHUNG_GIA_DO_NHOM_KEP_GIUA', 'HỆ KHUNG GIÁ ĐỠ NHÔM Kẹp giữa', 
    NULL, 
    'Cái', 
    'Kẹp giữa PIN năng lượng mặt trời.', 
    '{
        "installation_type": "Tất cả các loại mái",
        "material": "Nhôm cao cấp",
        "usage": "Cố định pin năng lượng mặt trời"
    }',
    NOW(), TRUE
);
INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    4, 5, NULL, 'HE_KHUNG_GIA_DO_NHOM_THANH_FULL_RAIL', 'HỆ KHUNG GIÁ ĐỠ NHÔM Thanh full rail', 
    NULL, 
    'Cái', 
    'Thanh full rail nhôm cao cấp 4.2m.', 
    '{
        "installation_type": "Áp mái tôn",
        "material": "Nhôm cao cấp",
        "length": "4.2m"
    }',
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    4, 5, NULL, 'HE_KHUNG_GIA_DO_NHOM_THANH_NOI_NHOM', 'HỆ KHUNG GIÁ ĐỠ NHÔM Thanh nối nhôm', 
    NULL, 
    'Cái', 
    'Thanh nối nhôm cao cấp đảm bảo lắp đặt tấm pin an toàn.', 
    '{
        "installation_type": ["Áp mái tôn", "Mái ngói"],
        "material": "Nhôm cao cấp"
    }',
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    4, 5, NULL, 'HE_KHUNG_GIA_DO_NHOM_CHAN_L', 'HỆ KHUNG GIÁ ĐỠ NHÔM Chân L', 
    NULL, 
    'Cái', 
    'Chân L - nhôm cao cấp dùng cho hệ khung giá đỡ.', 
    '{
        "installation_type": ["Áp mái tôn", "Mái ngói"],
        "material": "Nhôm cao cấp"
    }',
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    4, 5, NULL, 'HE_KHUNG_GIA_DO_NHOM_KEP_TIEP_DIA', 'HỆ KHUNG GIÁ ĐỠ NHÔM Kẹp tiếp địa', 
    NULL, 
    'Cái', 
    'Kẹp tiếp địa dùng để đảm bảo an toàn điện cho hệ khung giá đỡ.', 
    '{
        "installation_type": ["Tất cả các loại mái"],
        "material": "Nhôm cao cấp"
    }',
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    4, 5, NULL, 'HE_KHUNG_GIA_DO_NHOM_LA_TIEP_DIA', 'HỆ KHUNG GIÁ ĐỠ NHÔM Lá tiếp địa', 
    NULL, 
    'Cái', 
    'Lá tiếp địa dùng để dẫn điện xuống đất, đảm bảo an toàn hệ thống.', 
    '{
        "installation_type": ["Tất cả các loại mái"],
        "material": "Nhôm cao cấp"
    }',
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, 
    description_in_contract, data_json, created_at, active
) VALUES (
    5, 6, NULL, 
    'HE_DAY_DIEN_DAY_DC_DEN_4_0', 
    'HỆ DÂY ĐIỆN Dây DC đen 4,0', 
    NULL, 
    'Mét', 
    'Dây điện DC 4,0 màu đen, cáp điện chuyên dụng DC Solar 1500V.', 
    '{
        "phase_type": "1-phase",
        "cable_size_mm2": "4"
    }', 
    NOW(), TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, description_in_contract, data_json, created_at, active
) VALUES (
    5, 6, NULL, 
    'HE_DAY_DIEN_DC_4_0', 
    'Hệ Dây Điện DC 4.0', 
    NULL, 
    'Mét', 
    'Dây điện DC 4.0 màu đỏ. Cáp điện chuyên dụng DC Solar 1500V', 
    '{"phase_type": "1-phase", "cable_size_mm2": "4"}', 
    NOW(), 
    TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, description_in_contract, data_json, created_at, active
) VALUES (
    5, 6, NULL, 
    'HE_DAY_DIEN_AC_1P_2X6_2X10', 
    'Hệ Dây Điện AC 1P 2x6/2x10', 
    NULL, 
    'Mét', 
    'Dây điện AC 1 pha 2 lõi đồng cao cấp CVV 2x6/2x10mm', 
    '{"phase_type": "1-phase", "cable_size_mm2": "10"}', 
    NOW(), 
    TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, description_in_contract, data_json, created_at, active
) VALUES (
    5, 6, NULL, 
    'HE_DAY_DIEN_DAY_TIN_HIEU', 
    'Hệ Dây Điện - Dây tín hiệu', 
    NULL, 
    'Bộ', 
    'Dây mang tín hiệu đo tải tiêu thụ. Từ CT + Meter đến Inverter. Chống phát ngược lên lưới.', 
    '{"phase_type": "1-phase", "cable_size_mm2": "N/A"}', 
    NOW(), 
    TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, description_in_contract, data_json, created_at, active
) VALUES (
    5, 6, NULL, 
    'HE_DAY_DIEN_JACK_MC4', 
    'Hệ Dây Điện - Jack MC4', 
    NULL, 
    'Bộ', 
    'Jack MC4 chuyên dụng NLMT 1500V', 
    '{"phase_type": "N/A", "cable_size_mm2": "N/A"}', 
    NOW(), 
    TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, description_in_contract, data_json, created_at, active
) VALUES (
    6, 4, NULL, 
    'TU_DIEN_HYBRID_1P_5KW', 
    'Tủ Điện Hybrid 1P 5kW', 
    NULL, 
    'Tủ', 
    'Tủ điện hệ NLMT Hybrid 5kW 1 pha - 2 strings đi theo Inverter đầy đủ ATS của hệ:\n'
    '+ Vỏ tủ sắt chuyên dụng - Sơn tĩnh điện\n'
    '+ ATS 2P-63A: Thương hiệu Aisikai/tương đương\n'
    '+ At AC 2P 63A/At AC 2P 32A: Thương hiệu LS/tương đương\n'
    '+ At DC-800VDC 2 strings: Thương hiệu Suntee/Vaneims/tương đương\n'
    '+ Chống sét AC- SPC lưới lan truyền: Thương hiệu Suntee/tương đương', 
    '{
        "installation_type": "Hybrid",
        "phase_type": "1-phase",
        "power_capacity_kw": 5
    }', 
    NOW(), 
    TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, description_in_contract, data_json, created_at, active
) VALUES (
    7, 6, NULL, 
    'HE_TIEP_DIA_CAP_TIEP_DIA_1X4MM', 
    'Hệ Tiếp Địa_Cáp tiếp địa_1x4mm', 
    NULL, 
    'Mét', 
    'Cáp tiếp địa Cadivi CV-1x4mm²', 
    '{
        "wire_diameter_mm": "4"
    }', 
    NOW(), 
    TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, description_in_contract, data_json, created_at, active
) VALUES (
    7, 5, NULL, 
    'HE_TIEP_DIA_COC_DONG_1_2M', 
    'Hệ Tiếp Địa_Cọc đồng_1.2m', 
    NULL, 
    'Bộ', 
    'Hệ tiếp địa thoát sét cho giàn Pin đến Tủ điện mặt trời và Tủ điện mặt trời vào hệ thống tủ của nhà', 
    '{
        "wire_diameter_mm": "12"
    }', 
    NOW(), 
    TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, description_in_contract, data_json, created_at, active
) VALUES (
    7, 5, NULL, 
    'HE_TIEP_DIA_ONG_NHUA_32MM', 
    'Hệ Tiếp Địa_Ống nhựa 32mm', 
    NULL, 
    'Mét', 
    'Ống nhựa HDPE đường kính 32mm (cuộn 25m)', 
    '{
        "wire_diameter_mm": "32"
    }', 
    NOW(), 
    TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, description_in_contract, data_json, created_at, active
) VALUES (
    8, 4, NULL, 
    'LAP_DAT_PHU_KIEN_LAP_DAT_5KW', 
    'LẮP ĐẶT_Phụ kiện lắp đặt_5kW', 
    NULL, 
    'Gói', 
    'Phụ kiện lắp đặt trọn gói (Bulong, ốc vít, Kẹp dây điện, băng keo điện, vật tư chống thấm thi công,...)', 
    '{
        "installation_power_kwp": "<=5",
        "price_vnd": 800000
    }', 
    NOW(), 
    TRUE
);

INSERT INTO merchandises (
    template_id, brand_id, supplier_id, code, name, data_sheet_link, unit, description_in_contract, data_json, created_at, active
) VALUES (
    8, 4, NULL, 
    'LAP_DAT_DON_GIA_NHAN_CONG_LOAI_1_6_KWP', 
    'LẮP ĐẶT_Đơn giá nhân công loại 1 (<6 kWp)', 
    NULL, 
    'Gói', 
    'Nhân công lắp đặt + Vận chuyển + Kiểm định vận hành', 
    '{
        "installation_power_kwp": "<6",
        "price_vnd": 1500000
    }', 
    NOW(), 
    TRUE
);

insert into customers (name, address,phone, email)
values('doan minh','hai duong','0889156262','minhdhhe171764@gmail.com');
