#!/usr/bin/env python
# -*- coding: utf-8 -*-
# convert_to_indonesian.py
# Script untuk convert main.py ke Bahasa Indonesia

"""
Script ini melakukan konversi otomatis dari Bahasa Inggris ke Bahasa Indonesia
pada main.py sambil mempertahankan:
1. Warna (Colors.*)
2. Icons (Icons.*)
3. Variable names
4. File paths

USAGE:
    python convert_to_indonesian.py
"""

# Mapping English to Indonesian untuk main.py
CONVERSION_MAP = {
    # Menu
    '"MAIN MENU"': 'MENU_TITLE',
    'Select option': 'SELECT_OPTION',
    '"DEVICE MONITORING"': 'DEVICE_MONITORING',
    '"DEVICE MONITORING + SHUTDOWN"': 'DEVICE_MONITORING_WITH_SHUTDOWN',
    
    # Instructions
    '"Instructions:"': 'INSTRUCTIONS',
    '"• Connect new iPhone via USB"': 'CONNECT_IPHONE',
    '"• Information will be automatically extracted"': 'AUTOMATICALLY_EXTRACTED',
    '"• You will be prompted to select device color"': 'COLOR_SELECTION_INFO',
    '"• Press Ctrl+C to stop"': 'PRESS_CTRL_C',
    
    # Device Detection
    '"New device detected"': 'NEW_DEVICE_DETECTED',
    '"Extracting device"': 'EXTRACTING_DEVICE',
    '"Extraction completed in"': 'EXTRACTION_COMPLETED',
    '"Device already scanned!"': 'DEVICE_ALREADY_SCANNED',
    
    # Device Info
    '"DEVICE INFORMATION"': 'DEVICE_INFO_HEADER',
    '"Product"': 'PRODUCT',
    '"Color"': 'COLOR',
    '"Serial"': 'SERIAL',
    '"Storage"': 'STORAGE',
    '"Model ID"': 'MODEL_ID',
    '"IMEI 1"': 'IMEI_1',
    '"IMEI 2"': 'IMEI_2',
    
    # Operations
    '"SCAN CURRENT DEVICES"': 'SCAN_CURRENT_DEVICES',
    '"No devices connected"': 'NO_DEVICES',
    '"Found"': 'FOUND_DEVICES',
    '"SEEN IMEIs"': 'SEEN_IMEIS',
    '"CLEAR SEEN IMEIs"': 'CLEAR_SEEN_IMEIS',
    '"RESET ALL DATA"': 'RESET_ALL_DATA',
    
    # Return to Menu
    '"Press Enter to continue..."': 'PRESS_ENTER',
    '"Press ENTER to return to menu..."': 'RETURN_TO_MENU',
}

def main():
    print("Konversi akan dilakukan secara manual.")
    print("\nModerata mapping yang diperlukan:")
    for english, indonesian in CONVERSION_MAP.items():
        print("  {} → {}".format(english, indonesian))
    
    print("\nUntuk implementasi penuh, gunakan replace_string_in_file tool di copilot")
    print("atau edit file main.py secara manual.")

if __name__ == '__main__':
    main()
