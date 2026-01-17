# main.py - VERSION 5.4.0 DENGAN TRUST RETRY CEPAT DAN VALIDASI DATA
import subprocess
import pandas as pd
import os
import time
import sys
import csv
import platform
import json
from datetime import datetime

# Import modules
from colors import Colors, Icons
from utils import *
from config import PRODUCT_MAPPING, CSV_FILE, BC_FILE, CSV_FILE_COLOR, BC_FILE_COLOR, SEEN_IMEI_FILE, SEEN_IMEI_FILE_COLOR
from data_manager import DataManager
from file_manager import FileManager
from storage_extractor import extract_storage_capacity_real
from color_detector import extract_device_color
from color_selector import display_color_selection
from localization import *

class DeviceScanner:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.connected_devices = set()
        self.device_retry_count = {}
        self.max_retries = 3
        self.untrusted_devices = set()
        self.pending_trust_devices = set()
        self.failed_extractions = set()  # ✅ Device dengan ekstraksi gagal
    
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
            print_error(f"{ERROR_GET_UDIDS}: {e}")
        return set()
    
    def check_device_trust_status(self, udid: str) -> dict:
        """Check if device has trusted the computer"""
        trust_status = {
            'is_trusted': False,
            'error_type': None,
            'message': ''
        }
        
        try:
            # Coba akses info dasar untuk cek trust status
            result = subprocess.run(
                ['ideviceinfo', '-u', udid, '-k', 'DeviceName'],
                capture_output=True,
                text=True,
                timeout=3,  # ✅ Timeout lebih cepat
                check=False
            )
            
            # Jika returncode 0 dan ada output, device sudah trust
            if result.returncode == 0 and result.stdout.strip():
                trust_status['is_trusted'] = True
                trust_status['message'] = f"Device {udid[:8]}... sudah trust"
                
            # Jika error atau tidak ada output, device belum trust
            else:
                error_output = result.stderr.lower() if result.stderr else ""
                
                if "not paired" in error_output or "pairing" in error_output:
                    trust_status['error_type'] = 'not_paired'
                    trust_status['message'] = f"Device {udid[:8]}... belum dipasangkan"
                elif "not found" in error_output or "timed out" in error_output:
                    trust_status['error_type'] = 'not_found'
                    trust_status['message'] = f"Device {udid[:8]}... tidak ditemukan"
                elif "denied" in error_output or "lockdown" in error_output:
                    trust_status['error_type'] = 'not_trusted'
                    trust_status['message'] = f"Device {udid[:8]}... belum trust komputer ini"
                else:
                    trust_status['error_type'] = 'unknown'
                    trust_status['message'] = f"Device {udid[:8]}... error: {error_output[:50]}"
                    
        except subprocess.TimeoutExpired:
            trust_status['error_type'] = 'timeout'
            trust_status['message'] = f"Device {udid[:8]}... timeout - belum trust"
        except Exception as e:
            trust_status['error_type'] = 'exception'
            trust_status['message'] = f"Device {udid[:8]}... exception: {str(e)[:50]}"
        
        return trust_status
    
    def wait_for_device_trust(self, udid: str, max_attempts: int = 20, delay: int = 5) -> bool:
        """Wait for device to be trusted by user - dengan delay pendek"""
        print_info(f"{WAITING_FOR_TRUST} {udid[:8]}...")
        print(f"{Colors.BRIGHT_YELLOW}{Icons.INFO} {TRUST_INSTRUCTION}{Colors.RESET}")
        print(f"{Colors.DIM}  • {TRUST_STEP_1}")
        print(f"  • {TRUST_STEP_2}")
        print(f"  • {TRUST_STEP_3}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'─'*60}{Colors.RESET}")
        
        # Tambahkan ke pending list
        self.pending_trust_devices.add(udid)
        
        for attempt in range(1, max_attempts + 1):
            # Progress bar sederhana
            progress = int((attempt / max_attempts) * 50)
            progress_bar = f"[{'█' * progress}{'░' * (50 - progress)}]"
            print(f"{Colors.DIM}{progress_bar} Attempt {attempt}/{max_attempts}{Colors.RESET}")
            
            trust_status = self.check_device_trust_status(udid)
            
            if trust_status['is_trusted']:
                print_success(f"{TRUST_SUCCESS} {udid[:8]}...")
                if udid in self.untrusted_devices:
                    self.untrusted_devices.remove(udid)
                if udid in self.pending_trust_devices:
                    self.pending_trust_devices.remove(udid)
                return True
            else:
                if attempt == 1 or attempt % 3 == 0:  # Tampilkan pesan setiap 3 percobaan
                    print_warning(f"{TRUST_NOT_YET}: {trust_status['message']}")
                
                if attempt < max_attempts:
                    print_info(f"{WAITING_RETRY} {delay} detik...")
                    time.sleep(delay)  # ✅ Delay pendek 5 detik
                else:
                    print_error(f"{TRUST_TIMEOUT} {udid[:8]}...")
                    self.untrusted_devices.add(udid)
                    if udid in self.pending_trust_devices:
                        self.pending_trust_devices.remove(udid)
                    return False
        
        return False
    
    def validate_device_info(self, info: dict) -> tuple:
        """Validasi data device - return (is_valid, error_message)"""
        critical_fields = [
            ('imei1', IMEI_1),
            ('serial', SERIAL),
            ('product_name', PRODUCT),
            ('storage', STORAGE)
        ]
        
        missing_fields = []
        for field_key, field_name in critical_fields:
            if info.get(field_key) == 'N/A' or not info.get(field_key):
                missing_fields.append(field_name)
        
        if missing_fields:
            error_msg = f"{VALIDATION_FAILED}: {', '.join(missing_fields)}"
            return False, error_msg
        
        # Validasi IMEI format
        imei1 = info.get('imei1', '')
        if imei1 != 'N/A' and len(imei1) != 15:
            return False, f"{INVALID_IMEI_FORMAT}: {imei1[:15]}"
        
        return True, f"{VALIDATION_SUCCESS}"
    
    def extract_device_info_with_retry(self, udid: str):
        """Extract device info with trust check and data validation"""
        # Cek apakah device ini sedang menunggu trust
        if udid in self.pending_trust_devices:
            print_info(f"{DEVICE_WAITING_TRUST} {udid[:8]}...")
            # Coba lagi secara otomatis
            if self.wait_for_device_trust(udid):
                return self.extract_and_validate_device_info(udid)
            else:
                return None
        
        # Cek status trust dulu
        trust_status = self.check_device_trust_status(udid)
        
        if not trust_status['is_trusted']:
            print_warning(f"{DEVICE_NOT_TRUSTED} {udid[:8]}...")
            print(f"{Colors.BRIGHT_YELLOW}{trust_status['message']}{Colors.RESET}")
            
            # Tunggu device di-trust secara OTOMATIS
            print_info(f"{AUTO_WAITING_TRUST} {udid[:8]}...")
            if self.wait_for_device_trust(udid):
                # Jika sudah trust, ekstrak dan validasi data
                return self.extract_and_validate_device_info(udid)
            else:
                print_error(f"{EXTRACTION_FAILED_TRUST} {udid[:8]}...")
                return None
        
        # Jika sudah trust, ekstrak dan validasi data
        return self.extract_and_validate_device_info(udid)
    
    def extract_and_validate_device_info(self, udid: str):
        """Extract and validate device information"""
        max_retries = 3
        retry_delay = 2  # ✅ Delay pendek untuk retry
        
        for attempt in range(1, max_retries + 1):
            print_info(f"{ATTEMPT_EXTRACTION} {attempt}/{max_retries} untuk {udid[:8]}...")
            
            info = self.extract_device_info_real(udid)
            
            if not info:
                print_error(f"{EXTRACTION_FAILED} {udid[:8]}...")
                if attempt < max_retries:
                    print_info(f"{RETRYING_EXTRACTION} {retry_delay} detik...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print_error(f"{EXTRACTION_MAX_RETRY} {udid[:8]}...")
                    self.failed_extractions.add(udid)
                    return None
            
            # Validasi data
            is_valid, validation_msg = self.validate_device_info(info)
            
            if is_valid:
                print_success(validation_msg)
                if udid in self.failed_extractions:
                    self.failed_extractions.remove(udid)
                return info
            else:
                print_error(validation_msg)
                
                # Tampilkan data yang didapat untuk debugging
                print(f"{Colors.BRIGHT_YELLOW}{Icons.INFO} {DEBUG_INFO}:{Colors.RESET}")
                critical_fields = ['imei1', 'imei2', 'serial', 'product_name', 'storage']
                for field in critical_fields:
                    value = info.get(field, 'N/A')
                    if value == 'N/A' or not value:
                        print(f"  • {field}: {Colors.BRIGHT_RED}{value}{Colors.RESET}")
                    else:
                        print(f"  • {field}: {Colors.BRIGHT_GREEN}{value}{Colors.RESET}")
                
                if attempt < max_retries:
                    print_warning(f"{RETRYING_EXTRACTION} {retry_delay} detik...")
                    time.sleep(retry_delay)
                else:
                    print_error(f"{VALIDATION_MAX_RETRY} {udid[:8]}...")
                    self.failed_extractions.add(udid)
                    return None
        
        return None
    
    def extract_device_info_real(self, udid: str):
        """Extract REAL device information"""
        print_info(f"{EXTRACTING_DEVICE} {udid[:8]}...")
        start_time = time.time()
        
        try:
            # Get device info dengan timeout lebih pendek
            result = subprocess.run(
                ['ideviceinfo', '-u', udid],
                capture_output=True,
                text=True,
                check=False,
                timeout=8  # ✅ Timeout lebih pendek
            )
            
            if result.returncode != 0:
                print_error(f"{EXTRACTION_ERROR} {udid[:8]}...")
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
                print_warning(WARNING_IMEI_NOT_ACCESSIBLE)
            
            # Get basic info
            serial = device_info.get('SerialNumber', 'N/A')
            model_number = device_info.get('ModelNumber', '')
            region_info = device_info.get('RegionInfo', '')
            part = model_number + region_info if model_number or region_info else 'N/A'
            product_type = device_info.get('ProductType', 'N/A')
            product_name = PRODUCT_MAPPING.get(product_type, f'{UNKNOWN} ({product_type})')
            
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
            
            elapsed_time = time.time() - start_time
            print_success(f"{EXTRACTION_COMPLETED} {elapsed_time:.2f}s")
            return info
            
        except subprocess.TimeoutExpired:
            print_error(f"{EXTRACTION_TIMEOUT} {udid[:8]}...")
            return None
        except Exception as e:
            print_error(f"{ERROR_EXTRACTION}: {e}")
            return None
    
    def shutdown_device(self, udid: str):
        """Shutdown the device"""
        print_info(f"{SHUTDOWN_DEVICE} {udid[:8]}...")
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
    
    def retry_untrusted_devices(self):
        """Retry extraction for previously untrusted devices"""
        retried = []
        if self.untrusted_devices:
            print_info(f"{RETRYING_UNTRUSTED_DEVICES} {len(self.untrusted_devices)} device(s)...")
            
            for udid in list(self.untrusted_devices):
                print_info(f"{RETRYING_DEVICE} {udid[:8]}...")
                trust_status = self.check_device_trust_status(udid)
                
                if trust_status['is_trusted']:
                    print_success(f"{DEVICE_NOW_TRUSTED} {udid[:8]}...")
                    self.untrusted_devices.remove(udid)
                    retried.append(udid)
                else:
                    print_warning(f"{DEVICE_STILL_NOT_TRUSTED} {udid[:8]}...")
        
        return retried
    
    def retry_failed_extractions(self):
        """Retry extraction for previously failed devices"""
        retried = []
        if self.failed_extractions:
            print_info(f"{RETRYING_FAILED_EXTRACTIONS} {len(self.failed_extractions)} device(s)...")
            
            for udid in list(self.failed_extractions):
                print_info(f"{RETRYING_DEVICE} {udid[:8]}...")
                
                # Cek trust status dulu
                trust_status = self.check_device_trust_status(udid)
                
                if trust_status['is_trusted']:
                    # Jika sudah trust, coba ekstrak lagi
                    info = self.extract_and_validate_device_info(udid)
                    if info:
                        print_success(f"{RETRY_SUCCESS} {udid[:8]}...")
                        self.failed_extractions.remove(udid)
                        retried.append((udid, info))
                    else:
                        print_warning(f"{RETRY_FAILED} {udid[:8]}...")
                else:
                    print_warning(f"{DEVICE_STILL_NOT_TRUSTED} {udid[:8]}...")
        
        return retried

class iPhoneScannerApp:
    def __init__(self):
        self.data_manager = DataManager()
        self.device_scanner = DeviceScanner(self.data_manager)
        self.file_manager = None
        self.running = False
    
    def display_banner(self):
        """Display application banner"""
        clear_screen()
        print_header(f"{APP_TITLE} v5.4.0", 80)
        print(f"\n{Colors.BRIGHT_CYAN}{Icons.DEVICE}  {VERSION}: 5.4.0 - Enhanced Validation")
        print(f"{Icons.COMPUTER}  {SYSTEM}: {platform.system()} {platform.release()}")
        print(f"{Icons.CLOCK}  {TIME}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Icons.LIST}  {SEEN_IMEIS}: {len(self.data_manager.seen_imei)}")
        
        # Tampilkan status devices
        if self.device_scanner.untrusted_devices:
            print(f"{Colors.BRIGHT_YELLOW}{Icons.WARNING}  {UNTESTED_DEVICES}: {len(self.device_scanner.untrusted_devices)}{Colors.RESET}")
        
        if self.device_scanner.failed_extractions:
            print(f"{Colors.BRIGHT_RED}{Icons.ERROR}  {FAILED_EXTRACTIONS}: {len(self.device_scanner.failed_extractions)}{Colors.RESET}")
        
        # Tampilkan kedua session files
        print(f"{Icons.SAVE}  {SESSION_FILES}:")
        print(f"    • {SESSION_NO_COLOR}: {CSV_FILE} (CSV), {BC_FILE} (Excel)")
        print(f"    • {SESSION_WITH_COLOR}: {CSV_FILE_COLOR} (CSV), {BC_FILE_COLOR} (Excel)")
        
        print(f"{Colors.BRIGHT_CYAN}{'─'*80}{Colors.RESET}")
    
    def display_menu(self):
        """Display main menu"""
        print(f"\n{Colors.BRIGHT_WHITE}{Icons.LIST}  {MENU_TITLE}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'─'*50}{Colors.RESET}")
        
        for key in sorted(MENU_OPTIONS.keys(), key=lambda x: int(x)):
            title, desc = MENU_OPTIONS[key]
            print(f"{Colors.BRIGHT_GREEN}[{key}]{Colors.RESET} {Colors.BOLD}{title:<30}{Colors.RESET} {Colors.DIM}{desc}{Colors.RESET}")
        
        print(f"{Colors.BRIGHT_CYAN}{'─'*50}{Colors.RESET}")
    
    def scan_current_devices(self, manual_color=False):
        """Scan all currently connected devices"""
        print_header(SCAN_CURRENT_DEVICES)
        
        devices = self.device_scanner.get_connected_devices()
        if not devices:
            print_warning(NO_DEVICES_CONNECTED)
            time.sleep(2)
            self.return_to_menu()
            return
        
        print_success(f"{FOUND_DEVICES} {len(devices)} {DEVICE_SINGULAR_PLURAL}")
        
        # Inisialisasi FileManager dengan session type
        self.file_manager = FileManager(use_color_session=manual_color)
        
        for i, udid in enumerate(devices, 1):
            print(f"\n{Colors.BRIGHT_WHITE}{Icons.DEVICE} [{i}/{len(devices)}] {SCANNING_DEVICE} {udid[:8]}...{Colors.RESET}")
            
            # Gunakan fungsi baru dengan auto-retry dan validasi
            info = self.device_scanner.extract_device_info_with_retry(udid)
            
            if info:
                print_device_info(info)
                
                # Validasi final sebelum menyimpan
                is_valid, validation_msg = self.device_scanner.validate_device_info(info)
                
                if not is_valid:
                    print_error(f"{SAVE_VALIDATION_FAILED}: {validation_msg}")
                    print_warning(f"{DEVICE_NOT_SAVED} {udid[:8]}...")
                    continue
                
                if info['imei1'] != 'N/A' and info['imei1'] not in self.data_manager.seen_imei:
                    if manual_color:
                        # Pilih warna manual jika mode warna diaktifkan
                        selected_color = display_color_selection(info['product_name'])
                        info['color'] = selected_color
                    
                    # Konfirmasi save
                    confirm = input(f"\n{Colors.BRIGHT_YELLOW}{SAVE_CONFIRMATION} {Colors.RESET}").lower()
                    if confirm == 'y' or confirm == '':
                        if self.file_manager.save_device_info(info):
                            # Update data_manager dengan session yang sesuai
                            if manual_color:
                                self.data_manager.load_seen_imei(color_session=True)
                                self.data_manager.seen_imei.add(info['imei1'])
                                self.data_manager.save_seen_imei(color_session=True)
                            else:
                                self.data_manager.seen_imei.add(info['imei1'])
                                self.data_manager.save_seen_imei()
                            
                            print_success(DEVICE_SAVED)
                    else:
                        print_warning(f"{SAVE_CANCELLED} {udid[:8]}...")
        
        self.return_to_menu()
    
    def monitor_devices_with_retry(self, auto_shutdown: bool = False, manual_color: bool = False):
        """Monitor for device connections with automatic trust retry and validation"""
        self.running = True
        
        # Inisialisasi FileManager dengan session type
        self.file_manager = FileManager(use_color_session=manual_color)
        
        # Load seen IMEI untuk session yang sesuai
        if manual_color:
            self.data_manager.seen_imei = self.data_manager.load_seen_imei(color_session=True)
        else:
            self.data_manager.seen_imei = self.data_manager.load_seen_imei(color_session=False)
        
        mode_text = ""
        if manual_color:
            mode_text += f" + {MANUAL_COLOR_MODE}"
        if auto_shutdown:
            mode_text += f" + {SHUTDOWN_MODE}"
        
        print_header(f"{DEVICE_MONITORING}{mode_text}")
        print(f"\n{Colors.BRIGHT_WHITE}{Icons.INFO}  {INSTRUCTIONS}:{Colors.RESET}")
        print(f"{Colors.DIM}  • {INSTRUCTION_CONNECT}")
        print(f"  • {INSTRUCTION_TRUST_REMINDER}")
        
        if manual_color:
            print(f"  • {INSTRUCTION_COLOR_PROMPT}")
        else:
            print(f"  • {INSTRUCTION_AUTO_EXTRACT}")
        
        if auto_shutdown:
            print(f"  • {INSTRUCTION_AUTO_SHUTDOWN}")
        
        print(f"  • {INSTRUCTION_STOP}{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_CYAN}{'─'*80}{Colors.RESET}")
        
        previous_devices = set()
        last_retry_time = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                
                # Retry untrusted dan failed devices setiap 10 detik
                if current_time - last_retry_time > 10:
                    if self.device_scanner.untrusted_devices:
                        print_info(f"{CHECKING_UNTRUSTED_DEVICES}...")
                        retried = self.device_scanner.retry_untrusted_devices()
                        if retried:
                            print_success(f"{RETRIED_SUCCESS} {len(retried)} device(s)")
                    
                    if self.device_scanner.failed_extractions:
                        print_info(f"{RETRYING_FAILED_EXTRACTIONS}...")
                        retried = self.device_scanner.retry_failed_extractions()
                        if retried:
                            print_success(f"{RETRY_SUCCESS_COUNT} {len(retried)} device(s)")
                    
                    last_retry_time = current_time
                
                current_devices = self.device_scanner.get_connected_devices()
                
                new_devices = current_devices - previous_devices
                for udid in new_devices:
                    print_success(f"{NEW_DEVICE_DETECTED} {udid[:8]}...")
                    
                    # Gunakan extract dengan auto-retry dan validasi
                    info = self.device_scanner.extract_device_info_with_retry(udid)
                    
                    if info:
                        # Validasi data
                        is_valid, validation_msg = self.device_scanner.validate_device_info(info)
                        
                        if not is_valid:
                            print_error(f"{SAVE_VALIDATION_FAILED}: {validation_msg}")
                            print_warning(f"{SKIPPING_DEVICE} {udid[:8]}...")
                            continue
                        
                        # Check if IMEI already exists
                        if info['imei1'] != 'N/A' and info['imei1'] in self.data_manager.seen_imei:
                            print_warning(DEVICE_ALREADY_SCANNED)
                            print(f"{Colors.BRIGHT_YELLOW}")
                            print(f"{'─'*60}")
                            print(f"{LABEL_PRODUCT}: {info['product_name']}")
                            print(f"{LABEL_STORAGE}: {info['storage']}")
                            print(f"{LABEL_IMEI1}: {info['imei1'][:8]}...{info['imei1'][-4:]}")
                            print(f"{'─'*60}")
                            print(f"{Colors.RESET}")
                            print(f"{Colors.BRIGHT_CYAN}{DEVICE_ALREADY_PROCESSED}{Colors.RESET}")
                            print(f"{Colors.BRIGHT_GREEN}{CONNECT_DIFFERENT_DEVICE}{Colors.RESET}")
                            print()
                        else:
                            # New device - process it
                            print_device_info(info)
                            
                            # Manual color selection if enabled
                            if manual_color:
                                selected_color = display_color_selection(info['product_name'])
                                info['color'] = selected_color
                            
                            if self.file_manager.save_device_info(info):
                                # Simpan IMEI ke session yang sesuai
                                if info['imei1'] != 'N/A':
                                    self.data_manager.seen_imei.add(info['imei1'])
                                    if manual_color:
                                        self.data_manager.save_seen_imei(color_session=True)
                                    else:
                                        self.data_manager.save_seen_imei()
                                
                                print_success(DEVICE_SAVED)
                            
                            if auto_shutdown:
                                self.device_scanner.shutdown_device(udid)
                
                previous_devices = current_devices
                time.sleep(2)
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BRIGHT_YELLOW}{Icons.STOP} {MONITORING_STOPPED}{Colors.RESET}")
            self.running = False
        
        # Reset ke default session setelah monitoring selesai
        self.data_manager.seen_imei = self.data_manager.load_seen_imei(color_session=False)
        
        # Return to menu
        self.return_to_menu()
    
    def return_to_menu(self):
        """Prompt user to return to menu"""
        print(f"\n{Colors.BRIGHT_CYAN}{'─'*80}{Colors.RESET}")
        input(f"{Colors.BRIGHT_GREEN}{PRESS_ENTER_TO_RETURN}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}{'─'*80}{Colors.RESET}\n")
    
    def scan_with_reset(self):
        """Scan current devices after resetting seen IMEIs"""
        print_header(SCAN_WITH_RESET)
        
        confirm = input(f"{Colors.BRIGHT_YELLOW}{RESET_CONFIRMATION} {Colors.RESET}").lower()
        if confirm == 'y' or confirm == '':
            self.data_manager.seen_imei.clear()
            self.data_manager.save_seen_imei()
            print_success(SEEN_IMEI_CLEARED)
            time.sleep(1)
            self.scan_current_devices(manual_color=False)
        else:
            print_warning(SCAN_CANCELLED)
            self.return_to_menu()
            time.sleep(1)
    
    def view_seen_imeis(self):
        """Display all seen IMEIs"""
        print_header(VIEW_SEEN_IMEIS)
        
        if not self.data_manager.seen_imei:
            print_warning(NO_IMEIS_PROCESSED)
        else:
            print(f"\n{Colors.BRIGHT_WHITE}{TOTAL_IMEIS}: {len(self.data_manager.seen_imei)}{Colors.RESET}\n")
            for i, imei in enumerate(sorted(self.data_manager.seen_imei), 1):
                print(f"{Colors.BRIGHT_GREEN}[{i:3d}]{Colors.RESET} {imei}")
        
        self.return_to_menu()
    
    def clear_seen_imeis(self):
        """Clear the seen IMEIs list"""
        print_header(CLEAR_SEEN_IMEIS)
        
        confirm = input(f"{Colors.BRIGHT_YELLOW}{DELETE_CONFIRMATION} {len(self.data_manager.seen_imei)} {IMEIS_QUESTION} {Colors.RESET}").lower()
        if confirm == 'y' or confirm == '':
            self.data_manager.seen_imei.clear()
            self.data_manager.save_seen_imei()
            print_success(SEEN_IMEI_CLEARED)
        else:
            print_warning(CLEAR_CANCELLED)
        
        self.return_to_menu()
    
    def reset_all_data(self):
        """Reset all data - delete ALL files from both sessions"""
        print_header(RESET_ALL_DATA)
        
        print(f"\n{Colors.BRIGHT_RED}{WARNING_RESET}{Colors.RESET}")
        print(f"  • {LABEL_CSV}: {CSV_FILE} ({STANDARD_SESSION})")
        print(f"  • {LABEL_EXCEL}: {BC_FILE} ({STANDARD_SESSION})")
        print(f"  • {LABEL_SEEN_IMEI}: {SEEN_IMEI_FILE} ({STANDARD_SESSION})")
        print(f"  • {SESSION_WITH_COLOR}:")
        print(f"     - {CSV_FILE_COLOR} ({COLOR_SESSION})")
        print(f"     - {BC_FILE_COLOR} ({COLOR_SESSION})")
        print(f"     - {SEEN_IMEI_FILE_COLOR} ({COLOR_SESSION})")
        
        confirm = input(f"\n{Colors.BRIGHT_YELLOW}{CONFIRM_RESET} {Colors.RESET}").lower()
        if confirm == 'y' or confirm == '':
            try:
                files_to_delete = [
                    (CSV_FILE, f"{LABEL_CSV} ({STANDARD_SESSION})"),
                    (BC_FILE, f"{LABEL_EXCEL} ({STANDARD_SESSION})"),
                    (SEEN_IMEI_FILE, f"{LABEL_SEEN_IMEI} ({STANDARD_SESSION})"),
                    (CSV_FILE_COLOR, f"{LABEL_CSV} ({COLOR_SESSION})"),
                    (BC_FILE_COLOR, f"{LABEL_EXCEL} ({COLOR_SESSION})"),
                    (SEEN_IMEI_FILE_COLOR, f"{LABEL_SEEN_IMEI} ({COLOR_SESSION})")
                ]
                
                files_deleted_count = 0
                files_not_found = []
                
                print(f"\n{Colors.BRIGHT_YELLOW}{Icons.INFO} Memulai proses reset...{Colors.RESET}")
                
                for file_path, file_label in files_to_delete:
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                            files_deleted_count += 1
                            print_success(f"🗑️  {DELETED} {file_label}")
                        except Exception as e:
                            print_error(f"Gagal menghapus {file_label}: {e}")
                    else:
                        files_not_found.append(file_label)
                
                # Clear semua data dalam memori
                self.data_manager.seen_imei.clear()
                self.device_scanner.untrusted_devices.clear()
                self.device_scanner.pending_trust_devices.clear()
                self.device_scanner.failed_extractions.clear()
                
                # Buat file IMEI kosong
                print(f"\n{Colors.BRIGHT_YELLOW}{Icons.INFO} Membuat file IMEI kosong...{Colors.RESET}")
                try:
                    with open(SEEN_IMEI_FILE, 'w') as f:
                        json.dump([], f, indent=2)
                    print_success(f"✅ {SEEN_IMEI_FILE} ({STANDARD_SESSION}) dikosongkan")
                    
                    with open(SEEN_IMEI_FILE_COLOR, 'w') as f:
                        json.dump([], f, indent=2)
                    print_success(f"✅ {SEEN_IMEI_FILE_COLOR} ({COLOR_SESSION}) dikosongkan")
                    
                except Exception as e:
                    print_error(f"{ERROR_SAVING_IMEIS}: {e}")
                
                # Reload empty IMEI list
                self.data_manager.seen_imei = self.data_manager.load_seen_imei(color_session=False)
                
                # Tampilkan ringkasan
                print(f"\n{Colors.BRIGHT_CYAN}{'═'*60}{Colors.RESET}")
                print(f"{Colors.BRIGHT_GREEN}✅ {ALL_DATA_RESET}{Colors.RESET}")
                print(f"{Colors.BRIGHT_WHITE}📊 Ringkasan Reset:{Colors.RESET}")
                print(f"  • 📁 File dihapus: {files_deleted_count}")
                if files_not_found:
                    print(f"  • ⚠️  File tidak ditemukan: {len(files_not_found)}")
                print(f"  • 📋 IMEI dalam memori: {len(self.data_manager.seen_imei)}")
                print(f"  • 🎨 Session diproses: {STANDARD_SESSION} & {COLOR_SESSION}")
                print(f"{Colors.BRIGHT_CYAN}{'═'*60}{Colors.RESET}")
                
            except Exception as e:
                print_error(f"{ERROR_RESET}: {e}")
        else:
            print_warning(RESET_CANCELLED)
        
        self.return_to_menu()
    
    def run(self):
        """Main application loop"""
        while True:
            try:
                self.display_banner()
                self.display_menu()
                
                choice = input(f"\n{Colors.BRIGHT_GREEN}{Icons.SEARCH} {SELECT_OPTION} (1-10): {Colors.RESET}").strip()
                
                if choice == '1':
                    self.monitor_devices_with_retry(auto_shutdown=False, manual_color=False)
                elif choice == '2':
                    self.monitor_devices_with_retry(auto_shutdown=False, manual_color=True)
                elif choice == '3':
                    self.monitor_devices_with_retry(auto_shutdown=True, manual_color=False)
                elif choice == '4':
                    self.monitor_devices_with_retry(auto_shutdown=True, manual_color=True)
                elif choice == '5':
                    self.scan_current_devices(manual_color=False)
                elif choice == '6':
                    self.scan_with_reset()
                elif choice == '7':
                    self.view_seen_imeis()
                elif choice == '8':
                    self.clear_seen_imeis()
                elif choice == '9':
                    self.reset_all_data()
                elif choice == '10':
                    print(f"\n{Colors.BRIGHT_GREEN}{Icons.HEART} {THANK_YOU}{Colors.RESET}")
                    break
                else:
                    print_error(INVALID_OPTION)
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                continue
            except Exception as e:
                print_error(f"{ERROR_GENERAL}: {e}")
                time.sleep(2)

if __name__ == "__main__":
    try:
        app = iPhoneScannerApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BRIGHT_RED}{Icons.STOP} {APP_TERMINATED}{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"{APP_ERROR}: {e}")
        sys.exit(1)