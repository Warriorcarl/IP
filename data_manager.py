# data_manager.py - VERSION FINAL DENGAN SESSION SEPARATION
import json
import os
from utils import print_success, print_error, print_warning, print_info, format_upc_for_output
from config import (
    MODEL_MAPPING_FILE, 
    UPC_MAPPING_FILE, 
    SEEN_IMEI_FILE, 
    SEEN_IMEI_FILE_COLOR,
    CSV_FILE, 
    BC_FILE,
    CSV_FILE_COLOR,
    BC_FILE_COLOR
)
from localization import *

class DataManager:
    def __init__(self):
        self.model_mapping = self.load_json(MODEL_MAPPING_FILE)
        self.upc_mapping = self.load_json(UPC_MAPPING_FILE)
        # Load default session IMEI
        self.seen_imei = self.load_seen_imei(color_session=False)
        
    def load_json(self, filepath: str) -> dict:
        """Load JSON file"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                print_success(f"{LOADED_ENTRIES} {len(data)} {ENTRIES_FROM} {os.path.basename(filepath)}")
                return data
            except Exception as e:
                print_error(f"{ERROR_LOADING} {filepath}: {e}")
        return {}
    
    def load_seen_imei(self, color_session: bool = False) -> set:
        """Load seen IMEI from file - supports both sessions"""
        seen = set()
        file_path = SEEN_IMEI_FILE_COLOR if color_session else SEEN_IMEI_FILE
        session_name = COLOR_SESSION if color_session else STANDARD_SESSION
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    loaded = json.load(f)
                if isinstance(loaded, list):
                    seen = set(loaded)
                print_success(f"{LOADED_IMEIS} {len(seen)} {SEEN_IMEIS_FROM} {session_name} {SESSION}")
            except Exception as e:
                print_error(f"{ERROR_LOADING_IMEIS}: {e}")
        else:
            print_info(f"{NO_IMEI_FILE} {session_name} {SESSION}. {CREATING_NEW}.")
        
        return seen
    
    def save_seen_imei(self, color_session: bool = False):
        """Save seen IMEI to file - supports both sessions"""
        file_path = SEEN_IMEI_FILE_COLOR if color_session else SEEN_IMEI_FILE
        session_name = COLOR_SESSION if color_session else STANDARD_SESSION
        
        try:
            with open(file_path, 'w') as f:
                json.dump(list(self.seen_imei), f, indent=2)
            print_success(f"{SAVED_IMEIS} {len(self.seen_imei)} {IMEIS_TO} {session_name} {SESSION}")
        except Exception as e:
            print_error(f"{ERROR_SAVING_IMEIS}: {e}")
    
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
    
    def reset_all_data(self, color_session: bool = False) -> bool:
        """Reset all stored data - supports both sessions"""
        try:
            files_to_delete = []
            
            # Determine which files to delete based on session
            if color_session:
                files_to_delete = [
                    (CSV_FILE_COLOR, f"{LABEL_CSV} ({COLOR_SESSION})"),
                    (BC_FILE_COLOR, f"{LABEL_EXCEL} ({COLOR_SESSION})"),
                    (SEEN_IMEI_FILE_COLOR, f"{LABEL_SEEN_IMEI} ({COLOR_SESSION})")
                ]
            else:
                files_to_delete = [
                    (CSV_FILE, f"{LABEL_CSV} ({STANDARD_SESSION})"),
                    (BC_FILE, f"{LABEL_EXCEL} ({STANDARD_SESSION})"),
                    (SEEN_IMEI_FILE, f"{LABEL_SEEN_IMEI} ({STANDARD_SESSION})")
                ]
            
            files_deleted = []
            
            # Delete files
            for file_path, file_label in files_to_delete:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    files_deleted.append(file_label)
                    print_success(f"{DELETED}: {file_label}")
                else:
                    print_warning(f"{file_label} tidak ditemukan")
            
            # Clear seen IMEI in memory
            self.seen_imei.clear()
            
            # Create empty IMEI files
            try:
                if color_session:
                    with open(SEEN_IMEI_FILE_COLOR, 'w') as f:
                        json.dump([], f)
                else:
                    with open(SEEN_IMEI_FILE, 'w') as f:
                        json.dump([], f)
                print_success(f"File IMEI {COLOR_SESSION if color_session else STANDARD_SESSION} dikosongkan")
            except Exception as e:
                print_error(f"Error creating empty IMEI file: {e}")
            
            # Reload seen IMEI for consistency
            self.seen_imei = self.load_seen_imei(color_session=color_session)
            
            print_success(f"{RESET_COMPLETED}. {len(files_deleted)} {FILES_DELETED}.")
            return True
            
        except Exception as e:
            print_error(f"{ERROR_RESETTING_DATA}: {e}")
            return False
    
    def get_session_stats(self) -> dict:
        """Get statistics for both sessions"""
        stats = {
            'standard': {
                'imei_count': len(self.load_seen_imei(color_session=False)),
                'csv_exists': os.path.exists(CSV_FILE),
                'excel_exists': os.path.exists(BC_FILE),
                'imei_file_exists': os.path.exists(SEEN_IMEI_FILE)
            },
            'color': {
                'imei_count': len(self.load_seen_imei(color_session=True)),
                'csv_exists': os.path.exists(CSV_FILE_COLOR),
                'excel_exists': os.path.exists(BC_FILE_COLOR),
                'imei_file_exists': os.path.exists(SEEN_IMEI_FILE_COLOR)
            }
        }
        return stats