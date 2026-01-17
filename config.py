# config.py
PRODUCT_MAPPING = {
    "iPhone7,2": "iPhone 6", "iPhone7,1": "iPhone 6 Plus", "iPhone8,1": "iPhone 6s",
    "iPhone8,2": "iPhone 6s Plus", "iPhone8,4": "iPhone SE (1st generation)",
    "iPhone9,1": "iPhone 7", "iPhone9,2": "iPhone 7 Plus", "iPhone9,3": "iPhone 7",
    "iPhone9,4": "iPhone 7 Plus", "iPhone10,1": "iPhone 8", "iPhone10,2": "iPhone 8 Plus",
    "iPhone10,3": "iPhone X", "iPhone10,4": "iPhone 8", "iPhone10,5": "iPhone 8 Plus",
    "iPhone10,6": "iPhone X", "iPhone11,8": "iPhone XR", "iPhone11,2": "iPhone XS",
    "iPhone11,6": "iPhone XS Max", "iPhone12,1": "iPhone 11", "iPhone12,3": "iPhone 11 Pro",
    "iPhone12,5": "iPhone 11 Pro Max", "iPhone12,8": "iPhone SE (2nd generation)",
    "iPhone13,1": "iPhone 12 mini", "iPhone13,2": "iPhone 12", "iPhone13,3": "iPhone 12 Pro",
    "iPhone13,4": "iPhone 12 Pro Max", "iPhone14,4": "iPhone 13 mini", "iPhone14,5": "iPhone 13",
    "iPhone14,2": "iPhone 13 Pro", "iPhone14,3": "iPhone 13 Pro Max",
    "iPhone14,6": "iPhone SE (3rd generation)", "iPhone14,7": "iPhone 14",
    "iPhone14,8": "iPhone 14 Plus", "iPhone15,2": "iPhone 14 Pro",
    "iPhone15,3": "iPhone 14 Pro Max", "iPhone15,4": "iPhone 15",
    "iPhone15,5": "iPhone 15 Plus", "iPhone16,1": "iPhone 15 Pro",
    "iPhone16,2": "iPhone 15 Pro Max", "iPhone17,1": "iPhone 16",
    "iPhone17,2": "iPhone 16 Plus", "iPhone17,3": "iPhone 16 Pro",
    "iPhone17,4": "iPhone 16 Pro Max",
}

MODEL_MAPPING_FILE = 'model_mapping.json'
UPC_MAPPING_FILE = 'upc_mapping.json'
SEEN_IMEI_FILE = 'seen_imei.json'

# Default session (tanpa warna manual)
CSV_FILE = 'iphone_data.csv'
BC_FILE = 'BC.xlsx'

# Color session (dengan warna manual)
CSV_FILE_COLOR = 'iphone_data_color.csv'
BC_FILE_COLOR = 'BC_color.xlsx'

SEEN_IMEI_FILE_COLOR = 'seen_imei_color.json'