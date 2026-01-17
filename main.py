# main.py
import subprocess
import pandas as pd
import os
import time
import sys
import csv
from datetime import datetime

# Import modules
from colors import Colors, Icons
from utils import *
from config import PRODUCT_MAPPING, CSV_FILE, BC_FILE
from data_manager import DataManager
from storage_extractor import extract_storage_capacity_real
from color_detector import extract_device_color

class DeviceScanner:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.connected_devices = set()
        self.device_retry_count = {}
        self.max_retries = 3
    
    def get_connected_devices(self):
        """Get list of connected UDIDs"""
        try:
            result = subprocess.run(
                ['idevice_id', '-l'],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0 and result.stdout:
                udids = set(result.stdout.strip().splitlines())
                return udids
        except Exception as e:
            print_error(f"Error getting UDIDs: {e}")
        return set()
    
    def extract_device_info_real(self, udid: str):
        """Extract REAL device information"""
        print_info(f"Extracting device {udid[:8]}...")
        start_time = time.time()
        
        try:
            # Get device info
            result = subprocess.run(
                ['ideviceinfo', '-u', udid],
                capture_output=True,
                text=True,
                check=False,
                timeout=10
            )
            
            if result.returncode != 0:
                return None
            
            # Parse device info
            device_info = {}
            for line in result.stdout.splitlines():
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    device_info[key.strip()] = value.strip()
            
            # Get IMEIs
            imei1 = ensure_full_imei(device_info.get('InternationalMobileEquipmentIdentity', 'N/A'))
            imei2 = ensure_full_imei(device_info.get('InternationalMobileEquipmentIdentity2', 'N/A'))
            
            if imei1 == 'N/A':
                print_warning("IMEI not accessible")
                return None
            
            # Get basic info
            serial = device_info.get('SerialNumber', 'N/A')
            model_number = device_info.get('ModelNumber', '')
            region_info = device_info.get('RegionInfo', '')
            part = model_number + region_info if model_number or region_info else 'N/A'
            product_type = device_info.get('ProductType', 'N/A')
            product_name = PRODUCT_MAPPING.get(product_type, f'Unknown ({product_type})')
            
            # Get storage (REAL only)
            storage = extract_storage_capacity_real(device_info, udid)
            
            # Get color
            color = extract_device_color(udid, device_info)
            
            # Get other info
            model_id = self.data_manager.get_model_ids(product_name, part)
            upc = self.data_manager.get_upc(product_name, storage, part)
            
            # Compile info
            info = {
                'imei1': imei1,
                'imei2': imei2,
                'serial': serial,
                'part': part,
                'product_name': product_name,
                'product_type': product_type,
                'storage': storage,
                'color': color,
                'model_id': model_id,
                'upc': upc,
                'device_name': device_info.get('DeviceName', 'N/A'),
                'ios_version': device_info.get('ProductVersion', 'N/A'),
                'wifi_address': device_info.get('WiFiAddress', 'N/A'),
                'bluetooth_address': device_info.get('BluetoothAddress', 'N/A'),
                'udid': udid,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print_success(f"Extraction completed in {time.time() - start_time:.2f}s")
            return info
            
        except Exception as e:
            print_error(f"Extraction error: {e}")
            return None
    
    def shutdown_device(self, udid: str):
        """Shutdown the device"""
        print_info(f"Shutting down device {udid[:8]}...")
        try:
            subprocess.run(
                ['idevicediagnostics', '-u', udid, 'shutdown'],
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
        except:
            pass

class FileManager:
    def __init__(self):
        self.csv_file = CSV_FILE
        self.bc_file = BC_FILE
    
    def save_device_info(self, device_info: dict):
        """Save device information"""
        try:
            self._save_to_csv(device_info)
            self._save_to_bc_excel(device_info)
            print_success("Saved to both files")
            return True
        except Exception as e:
            print_error(f"Save error: {e}")
            return False
    
    def _save_to_csv(self, device_info: dict):
        """Save to CSV file"""
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
        
        print_success(f"Saved to {self.csv_file}")
    
    def _save_to_bc_excel(self, device_info: dict):
        """Save to BC Excel file"""
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
        
        print_success(f"Saved to {self.bc_file}")

class iPhoneScannerApp:
    def __init__(self):
        self.data_manager = DataManager()
        self.device_scanner = DeviceScanner(self.data_manager)
        self.file_manager = FileManager()
        self.running = False
    
    def display_banner(self):
        """Display application banner"""
        clear_screen()
        print_header("iPhone Device Scanner Pro v5.2.0", 80)
        print(f"\n{Colors.BRIGHT_CYAN}{Icons.DEVICE}  Version: 5.2.0 - Real Data Only")
        print(f"{Icons.COMPUTER}  System: {platform.system()} {platform.release()}")
        print(f"{Icons.CLOCK}  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Icons.LIST}  Seen IMEIs: {len(self.data_manager.seen_imei)}")
        print(f"{Icons.SAVE}  Output Files: {CSV_FILE} (CSV), {BC_FILE} (Excel)")
        print(f"{Colors.BRIGHT_CYAN}{'─'*80}{Colors.RESET}")
    
    def display_menu(self):
        """Display main menu"""
        print(f"\n{Colors.BRIGHT_WHITE}{Icons.LIST}  MAIN MENU{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'─'*50}{Colors.RESET}")
        
        menu_options = [
            ("1", "📱 Monitor & Extract", "Extract info from new devices"),
            ("2", "📱⏻ Monitor + Shutdown", "Extract then shutdown device"),
            ("3", "🔍 Scan Current Devices", "Scan all connected devices"),
            ("4", "🔍🔄 Scan with Reset", "Reset data first, then scan"),
            ("5", "📋 View Seen IMEIs", "Show all processed IMEIs"),
            ("6", "🗑️  Clear Seen IMEIs", "Reset seen IMEI list"),
            ("7", "🗑️  Reset All Data", "Delete all output files and IMEI list"),
            ("8", "🚪 Exit", "Close application")
        ]
        
        for num, title, desc in menu_options:
            print(f"{Colors.BRIGHT_GREEN}[{num}]{Colors.RESET} {Colors.BOLD}{title:<25}{Colors.RESET} {Colors.DIM}{desc}{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_CYAN}{'─'*50}{Colors.RESET}")
    
    def scan_current_devices(self):
        """Scan all currently connected devices"""
        print_header("SCAN CURRENT DEVICES")
        
        devices = self.device_scanner.get_connected_devices()
        if not devices:
            print_warning("No devices connected")
            time.sleep(2)
            return
        
        print_success(f"Found {len(devices)} device(s)")
        
        for i, udid in enumerate(devices, 1):
            print(f"\n{Colors.BRIGHT_WHITE}{Icons.DEVICE} [{i}/{len(devices)}] Device: {udid[:8]}...{Colors.RESET}")
            info = self.device_scanner.extract_device_info_real(udid)
            
            if info:
                print_device_info(info)
                
                if info['imei1'] != 'N/A' and info['imei1'] not in self.data_manager.seen_imei:
                    if input(f"\n{Colors.BRIGHT_YELLOW}Save this device? (y/n): {Colors.RESET}").lower() == 'y':
                        self.file_manager.save_device_info(info)
                        self.data_manager.seen_imei.add(info['imei1'])
                        self.data_manager.save_seen_imei()
                        print_success(f"{Icons.TROPHY} DEVICE SAVED!")
        
        input(f"\n{Colors.BRIGHT_CYAN}Press Enter to continue...{Colors.RESET}")
    
    def monitor_devices(self, auto_shutdown: bool = False):
        """Monitor for device connections"""
        self.running = True
        
        print_header(f"DEVICE MONITORING {'+ SHUTDOWN' if auto_shutdown else ''}")
        print(f"\n{Colors.BRIGHT_WHITE}{Icons.INFO}  Instructions:{Colors.RESET}")
        print(f"{Colors.DIM}  • Connect new iPhone via USB")
        print(f"  • Information will be automatically extracted")
        print(f"  • Press Ctrl+C to stop{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_CYAN}{'─'*80}{Colors.RESET}")
        
        previous_devices = set()
        
        try:
            while self.running:
                current_devices = self.device_scanner.get_connected_devices()
                
                new_devices = current_devices - previous_devices
                for udid in new_devices:
                    print_success(f"New device detected: {udid[:8]}...")
                    
                    info = self.device_scanner.extract_device_info_real(udid)
                    if info and info['imei1'] != 'N/A':
                        # Check if IMEI already exists
                        if info['imei1'] in self.data_manager.seen_imei:
                            print_warning(f"⚠️  Device already scanned!")
                            print(f"{Colors.BRIGHT_YELLOW}")
                            print(f"{'─'*60}")
                            print(f"📱 Product: {info['product_name']}")
                            print(f"📊 Storage: {info['storage']}")
                            print(f"📋 IMEI 1: {info['imei1'][:8]}...{info['imei1'][-4:]}")
                            print(f"{'─'*60}")
                            print(f"{Colors.RESET}")
                            print(f"{Colors.BRIGHT_CYAN}💡 This device has already been processed and saved.{Colors.RESET}")
                            print(f"{Colors.BRIGHT_GREEN}✅ Please connect a DIFFERENT device to continue.{Colors.RESET}")
                            print()
                        else:
                            # New device - process it
                            print_device_info(info)
                            self.file_manager.save_device_info(info)
                            self.data_manager.seen_imei.add(info['imei1'])
                            self.data_manager.save_seen_imei()
                            print_success(f"{Icons.TROPHY} DEVICE SAVED!")
                            
                            if auto_shutdown:
                                self.device_scanner.shutdown_device(udid)
                
                previous_devices = current_devices
                time.sleep(2)
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BRIGHT_YELLOW}{Icons.STOP} Monitoring stopped{Colors.RESET}")
            self.running = False
    
    def scan_with_reset(self):
        """Scan current devices after resetting seen IMEIs"""
        print_header("SCAN WITH RESET")
        
        if input(f"{Colors.BRIGHT_YELLOW}This will reset the seen IMEI list. Continue? (y/n): {Colors.RESET}").lower() == 'y':
            self.data_manager.seen_imei.clear()
            self.data_manager.save_seen_imei()
            print_success("Seen IMEI list cleared")
            time.sleep(1)
            self.scan_current_devices()
        else:
            print_warning("Scan with reset cancelled")
            time.sleep(1)
    
    def view_seen_imeis(self):
        """Display all seen IMEIs"""
        print_header("SEEN IMEIs")
        
        if not self.data_manager.seen_imei:
            print_warning("No IMEIs have been processed yet")
        else:
            print(f"\n{Colors.BRIGHT_WHITE}Total IMEIs: {len(self.data_manager.seen_imei)}{Colors.RESET}\n")
            for i, imei in enumerate(sorted(self.data_manager.seen_imei), 1):
                print(f"{Colors.BRIGHT_GREEN}[{i:3d}]{Colors.RESET} {imei}")
        
        input(f"\n{Colors.BRIGHT_CYAN}Press Enter to continue...{Colors.RESET}")
    
    def clear_seen_imeis(self):
        """Clear the seen IMEIs list"""
        print_header("CLEAR SEEN IMEIs")
        
        if input(f"{Colors.BRIGHT_YELLOW}Delete all {len(self.data_manager.seen_imei)} seen IMEIs? (y/n): {Colors.RESET}").lower() == 'y':
            self.data_manager.seen_imei.clear()
            self.data_manager.save_seen_imei()
            print_success("Seen IMEI list cleared")
        else:
            print_warning("Clear cancelled")
        
        time.sleep(2)
    
    def reset_all_data(self):
        """Reset all data - delete output files and seen IMEIs"""
        print_header("RESET ALL DATA")
        
        print(f"\n{Colors.BRIGHT_RED}⚠️  This will delete:{Colors.RESET}")
        print(f"  • CSV file: {CSV_FILE}")
        print(f"  • Excel file: {BC_FILE}")
        print(f"  • Seen IMEI list ({len(self.data_manager.seen_imei)} entries)")
        
        if input(f"\n{Colors.BRIGHT_YELLOW}Are you sure? (y/n): {Colors.RESET}").lower() == 'y':
            try:
                # Delete CSV file
                if os.path.exists(CSV_FILE):
                    os.remove(CSV_FILE)
                    print_success(f"Deleted {CSV_FILE}")
                
                # Delete Excel file
                if os.path.exists(BC_FILE):
                    os.remove(BC_FILE)
                    print_success(f"Deleted {BC_FILE}")
                
                # Clear seen IMEIs
                self.data_manager.seen_imei.clear()
                self.data_manager.save_seen_imei()
                print_success("Cleared seen IMEI list")
                
                print_success("All data has been reset")
            except Exception as e:
                print_error(f"Error during reset: {e}")
        else:
            print_warning("Reset cancelled")
        
        time.sleep(2)
    
    def run(self):
        """Main application loop"""
        while True:
            try:
                self.display_banner()
                self.display_menu()
                
                choice = input(f"\n{Colors.BRIGHT_GREEN}{Icons.SEARCH} Select option (1-8): {Colors.RESET}").strip()
                
                if choice == '1':
                    self.monitor_devices(auto_shutdown=False)
                elif choice == '2':
                    self.monitor_devices(auto_shutdown=True)
                elif choice == '3':
                    self.scan_current_devices()
                elif choice == '4':
                    self.scan_with_reset()
                elif choice == '5':
                    self.view_seen_imeis()
                elif choice == '6':
                    self.clear_seen_imeis()
                elif choice == '7':
                    self.reset_all_data()
                elif choice == '8':
                    print(f"\n{Colors.BRIGHT_GREEN}{Icons.HEART} Thank you!{Colors.RESET}")
                    break
                else:
                    print_error("Invalid option")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                continue
            except Exception as e:
                print_error(f"Error: {e}")
                time.sleep(2)

if __name__ == "__main__":
    try:
        app = iPhoneScannerApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BRIGHT_RED}{Icons.STOP} Application terminated{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Application error: {e}")
        sys.exit(1)