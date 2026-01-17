# utils.py
import os
import platform
from datetime import datetime
from colors import Colors, Icons

def clear_screen():
    """Clear terminal screen based on OS"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_header(title: str, width: int = 80):
    """Print a styled header"""
    print(f"\n{Colors.BRIGHT_CYAN}{'='*width}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}{title.center(width)}{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'='*width}{Colors.RESET}")

def print_status(message: str, icon: str = Icons.INFO, color: str = Colors.BRIGHT_WHITE):
    """Print status message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} {icon} {color}{message}{Colors.RESET}")

def print_success(message: str):
    """Print success message"""
    print_status(message, Icons.SUCCESS, Colors.BRIGHT_GREEN)

def print_error(message: str):
    """Print error message"""
    print_status(message, Icons.ERROR, Colors.BRIGHT_RED)

def print_warning(message: str):
    """Print warning message"""
    print_status(message, Icons.WARNING, Colors.BRIGHT_YELLOW)

def print_info(message: str):
    """Print info message"""
    print_status(message, Icons.INFO, Colors.BRIGHT_CYAN)

def print_device_info(device_info: dict):
    """Print device information in a formatted way"""
    print(f"\n{Colors.BRIGHT_CYAN}{' DEVICE INFORMATION ':-^60}{Colors.RESET}")
    
    info_items = [
        (f"{Icons.DEVICE} Product", device_info.get('product_name', 'N/A')),
        (f"{Icons.SETTINGS} Model", device_info.get('product_type', 'N/A')),
        (f"{Icons.PALETTE} Color", device_info.get('color', 'N/A')),
        (f"{Icons.LOCK} Serial", device_info.get('serial', 'N/A')),
        (f"{Icons.FLAG} Part", device_info.get('part', 'N/A')),
        (f"{Icons.CHART} Storage", device_info.get('storage', 'N/A')),
        (f"{Icons.LIST} Model ID", device_info.get('model_id', 'N/A')),
        (f"{Icons.STAR} UPC", device_info.get('upc', 'N/A')),
        (f"{Icons.DEVICE} IMEI 1", format_imei(device_info.get('imei1', 'N/A'))),
        (f"{Icons.DEVICE} IMEI 2", format_imei(device_info.get('imei2', 'N/A'))),
        (f"{Icons.TAG} Device Name", device_info.get('device_name', 'N/A')),
        (f"{Icons.GEAR} iOS Version", device_info.get('ios_version', 'N/A')),
    ]
    
    for label, value in info_items:
        print(f"{Colors.BRIGHT_WHITE}{label:<20}{Colors.RESET}: {Colors.BRIGHT_GREEN}{value}{Colors.RESET}")
    
    print(f"{Colors.BRIGHT_CYAN}{'-'*60}{Colors.RESET}")

def format_imei(imei: str) -> str:
    """Format IMEI for display"""
    if imei == 'N/A' or len(imei) < 8:
        return imei
    return f"{imei[:8]}...{imei[-4:] if len(imei) > 12 else ''}"

def ensure_full_imei(imei: str) -> str:
    """Ensure IMEI is full length (15 digits)"""
    if imei == 'N/A' or not imei or imei.strip() == '':
        return 'N/A'
    
    digits = ''.join(filter(str.isdigit, str(imei)))
    
    if len(digits) == 15:
        return digits
    elif len(digits) == 16:
        return digits[:15]
    elif len(digits) < 15:
        return 'N/A'
    else:
        return digits[:15]

def format_upc_for_output(upc_value) -> str:
    """Format UPC code for output"""
    if upc_value == 'N/A' or not upc_value:
        return 'N/A'
    
    upc_str = str(upc_value)
    digits = ''.join(filter(str.isdigit, upc_str))
    
    if len(digits) < 12:
        digits = digits.zfill(12)
    elif len(digits) > 12:
        digits = digits[:12]
    
    return digits