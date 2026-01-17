# file_manager.py
import csv
import pandas as pd
import os
from openpyxl import load_workbook
from config import CSV_FILE, BC_FILE, CSV_FILE_COLOR, BC_FILE_COLOR

class FileManager:
    def __init__(self, use_color_session=False):
        """
        Initialize FileManager
        use_color_session: True untuk session dengan warna manual, False untuk session tanpa warna
        """
        self.use_color_session = use_color_session
        
        if use_color_session:
            self.csv_file = CSV_FILE_COLOR
            self.bc_file = BC_FILE_COLOR
        else:
            self.csv_file = CSV_FILE
            self.bc_file = BC_FILE
    
    def save_device_info(self, device_info) -> bool:
        """Save device information with color"""
        try:
            self._save_to_csv(device_info)
            self._save_to_bc_excel(device_info)
            return True
        except Exception as e:
            from utils import print_error
            print_error("Kesalahan simpan: {}".format(str(e)))
            return False
    
    def _save_to_csv(self, device_info):
        """Save complete info to CSV"""
        data_row = [
            device_info['imei1'],
            device_info['imei2'],
            device_info['serial'],
            device_info['part'],
            device_info['product_name'],
            device_info['storage'],
            device_info['color'],
            device_info['model_id'],
            device_info['upc'],
            device_info['device_name'],
            device_info['ios_version'],
            device_info['timestamp']
        ]
        
        file_exists = os.path.exists(self.csv_file)
        
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            if not file_exists:
                headers = [
                    'IMEI1', 'IMEI2', 'Serial', 'Part', 'Product',
                    'Storage', 'Color', 'ModelID', 'UPC',
                    'DeviceName', 'iOSVersion', 'Timestamp'
                ]
                writer.writerow(headers)
            
            writer.writerow(data_row)
        
        from utils import print_success
        print_success("Tersimpan di {}".format(self.csv_file))
    
    def _save_to_bc_excel(self, device_info):
        """Save BC data with color"""
        df_new = pd.DataFrame([[
            device_info['product_name'],
            device_info['storage'],
            device_info['color'],
            device_info['imei1'],
            device_info['imei2']
        ]], columns=['Product Name', 'Storage', 'Color', 'IMEI1', 'IMEI2'])
        
        if os.path.exists(self.bc_file):
            try:
                df_existing = pd.read_excel(self.bc_file, engine='openpyxl')
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            except:
                df_combined = df_new
        else:
            df_combined = df_new
        
        with pd.ExcelWriter(self.bc_file, engine='openpyxl', mode='w') as writer:
            df_combined.to_excel(writer, sheet_name='BC Data', index=False)
        
        from utils import print_success
        print_success("Tersimpan di {}".format(self.bc_file))