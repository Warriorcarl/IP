# data_manager.py
import json
import os
from utils import print_success, print_error, print_warning, format_upc_for_output
from config import MODEL_MAPPING_FILE, UPC_MAPPING_FILE, SEEN_IMEI_FILE, CSV_FILE, BC_FILE

class DataManager:
    def __init__(self):
        self.model_mapping = self.load_json(MODEL_MAPPING_FILE)
        self.upc_mapping = self.load_json(UPC_MAPPING_FILE)
        self.seen_imei = self.load_seen_imei()
        
    def load_json(self, filepath: str) -> dict:
        """Load JSON file"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                print_success(f"Loaded {len(data)} entries from {os.path.basename(filepath)}")
                return data
            except Exception as e:
                print_error(f"Error loading {filepath}: {e}")
        return {}
    
    def load_seen_imei(self) -> set:
        """Load seen IMEI from file"""
        seen = set()
        if os.path.exists(SEEN_IMEI_FILE):
            try:
                with open(SEEN_IMEI_FILE, 'r') as f:
                    loaded = json.load(f)
                if isinstance(loaded, list):
                    seen = set(loaded)
                print_success(f"Loaded {len(seen)} seen IMEIs")
            except Exception as e:
                print_error(f"Error loading seen IMEIs: {e}")
        return seen
    
    def save_seen_imei(self):
        """Save seen IMEI to file"""
        try:
            with open(SEEN_IMEI_FILE, 'w') as f:
                json.dump(list(self.seen_imei), f)
        except Exception as e:
            print_error(f"Error saving seen IMEIs: {e}")
    
    def get_model_ids(self, product_name: str, device_part: str = "N/A") -> str:
        """Get specific model ID based on product name and device part/region"""
        models = self.model_mapping.get(product_name, [])
        
        if len(models) <= 1:
            return ", ".join(models) if models else "N/A"
        
        return self._determine_specific_model(models, device_part)

    def _determine_specific_model(self, model_list: list, device_part: str) -> str:
        """Determine the specific model ID based on region/part information"""
        if device_part == "N/A" or not device_part:
            return model_list[0]
        
        device_part_upper = device_part.upper()
        
        # Simple region detection
        if "LL/A" in device_part_upper or "US/" in device_part_upper:
            # US model
            for model in model_list:
                if model.endswith('4'):
                    return model
        elif "CH/A" in device_part_upper or "CN/A" in device_part_upper:
            # China model
            for model in model_list:
                if model.endswith('8'):
                    return model
        elif "J/A" in device_part_upper or "JP/A" in device_part_upper:
            # Japan model
            for model in model_list:
                if model.endswith('6'):
                    return model
        
        return model_list[0]
    
    def get_upc(self, product_name: str, storage: str, part: str) -> str:
        """Get UPC code based on product, storage, and region"""
        upc_data = self.upc_mapping.get(product_name, {})
        
        if not upc_data:
            return "N/A"
        
        # Parse storage value
        storage_num = None
        if storage != "N/A" and "GB" in storage:
            try:
                storage_num = int(storage.split()[0])
            except:
                pass
        
        if not storage_num:
            return "N/A"
        
        # Find matching storage key in UPC data
        storage_key = None
        for key in upc_data.keys():
            try:
                key_num = int(key.split()[0])
                if key_num == storage_num:
                    storage_key = key
                    break
            except:
                continue
        
        # Fallback: if storage not found and has data, use closest or first
        if not storage_key:
            # Try to find closest storage option
            available_storages = []
            for key in upc_data.keys():
                try:
                    key_num = int(key.split()[0])
                    available_storages.append((key_num, key))
                except:
                    continue
            
            if available_storages:
                available_storages.sort(key=lambda x: abs(x[0] - storage_num))
                storage_key = available_storages[0][1]
        
        if not storage_key:
            return "N/A"
        
        # Determine region from part number
        region = "Global"
        if part != "N/A":
            part_upper = part.upper()
            if "LL/A" in part_upper or "US/" in part_upper:
                region = "US"
            elif "CH/A" in part_upper or "CN/A" in part_upper:
                region = "China"
            elif "J/A" in part_upper or "JP/A" in part_upper:
                region = "Japan"
        
        # Get UPC for region
        upc_value = upc_data.get(storage_key, {}).get(region)
        
        # Fallback to Global if region not found
        if not upc_value:
            upc_value = upc_data.get(storage_key, {}).get("Global")
        
        # Fallback to first available region
        if not upc_value:
            region_dict = upc_data.get(storage_key, {})
            if region_dict:
                upc_value = list(region_dict.values())[0]
        
        return format_upc_for_output(upc_value) if upc_value else "N/A"
    
    def reset_all_data(self) -> bool:
        """Reset all stored data"""
        try:
            files_deleted = []
            
            if os.path.exists(CSV_FILE):
                os.remove(CSV_FILE)
                files_deleted.append(CSV_FILE)
                print_success(f"Deleted: {CSV_FILE}")
            
            if os.path.exists(BC_FILE):
                os.remove(BC_FILE)
                files_deleted.append(BC_FILE)
                print_success(f"Deleted: {BC_FILE}")
            
            self.seen_imei.clear()
            self.save_seen_imei()
            print_success("Cleared seen IMEI list")
            
            print_success(f"Reset completed. {len(files_deleted)} files deleted.")
            return True
            
        except Exception as e:
            print_error(f"Error resetting data: {e}")
            return False