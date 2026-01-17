# device_scanner.py
import subprocess
import time
from typing import Dict, Optional, Set
from datetime import datetime

from utils import *
from config import PRODUCT_MAPPING
from storage_extractor import extract_storage_capacity_real
from color_detector import extract_device_color

class DeviceScanner:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.connected_devices = set()
        self.device_retry_count = {}
        self.max_retries = 3
    
    def extract_device_info_real(self, udid: str) -> Optional[Dict]:
        """Extract REAL device information - NO DUMMY DATA"""
        retry_count = self.device_retry_count.get(udid, 0)
        
        if retry_count >= self.max_retries:
            return None
        
        print_info(f"Extracting device {udid[:8]}...")
        start_time = time.time()
        
        try:
            # Get ALL device info
            result = subprocess.run(
                ['ideviceinfo', '-u', udid, '-x'],  # -x for XML/plist format
                capture_output=True,
                text=True,
                check=False,
                timeout=15
            )
            
            if result.returncode != 0:
                return None
            
            # Parse device info
            device_info = self.parse_device_info(result.stdout)
            
            # Get critical information
            imei1 = self.extract_imei_real(device_info, 'InternationalMobileEquipmentIdentity')
            imei2 = self.extract_imei_real(device_info, 'InternationalMobileEquipmentIdentity2')
            
            # Skip if no IMEI (device not fully accessible)
            if imei1 == 'N/A':
                print_warning("Device IMEI not accessible")
                return None
            
            serial = device_info.get('SerialNumber', 'N/A')
            model_number = device_info.get('ModelNumber', '')
            region_info = device_info.get('RegionInfo', '')
            part = model_number + region_info if model_number or region_info else 'N/A'
            product_type = device_info.get('ProductType', 'N/A')
            product_name = PRODUCT_MAPPING.get(product_type, f'Unknown ({product_type})')
            
            # Get REAL storage (no estimation)
            storage = extract_storage_capacity_real(device_info, udid)
            
            # Get color
            color = extract_device_color(udid, device_info)
            
            # Get other info
            model_id = self.data_manager.get_model_ids(product_name, part)
            upc = self.data_manager.get_upc(product_name, storage, part)
            
            # Compile ALL real info
            info = {
                'imei1': imei1,
                'imei2': imei2,
                'serial': serial,
                'part': part,
                'product_name': product_name,
                'product_type': product_type,
                'storage': storage,
                'color': color,  # Added color field
                'model_id': model_id,
                'upc': upc,
                'device_name': device_info.get('DeviceName', 'N/A'),
                'ios_version': device_info.get('ProductVersion', 'N/A'),
                'wifi_address': device_info.get('WiFiAddress', 'N/A'),
                'bluetooth_address': device_info.get('BluetoothAddress', 'N/A'),
                'udid': udid,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print_success(f"Real data extraction completed in {time.time() - start_time:.2f}s")
            return info
            
        except Exception as e:
            print_error(f"Extraction error: {e}")
            return None
    
    def extract_imei_real(self, device_info: Dict, key: str) -> str:
        """Extract and validate IMEI - real data only"""
        imei = device_info.get(key, 'N/A')
        
        if imei == 'N/A' or not imei:
            return 'N/A'
        
        # Clean IMEI - remove spaces and non-digits
        imei_clean = ''.join(filter(str.isdigit, str(imei)))
        
        # Check if it's a valid IMEI (14-16 digits)
        if 14 <= len(imei_clean) <= 16:
            # Standard IMEI is 15 digits, return first 15
            return imei_clean[:15]
        
        return 'N/A'
    
    def parse_device_info(self, output: str) -> Dict:
        """Parse device info from ideviceinfo output"""
        device_info = {}
        
        for line in output.splitlines():
            if ': ' in line:
                key, value = line.split(': ', 1)
                device_info[key.strip()] = value.strip()
        
        return device_info