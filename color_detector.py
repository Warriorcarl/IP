# color_detector.py
import subprocess
import re

def extract_device_color(udid: str, device_info: dict) -> str:
    """
    Extract device color from device info
    Returns color name or 'N/A' if not found
    """
    
    # Method 1: Check for Color in device info (multiple possible keys)
    color_keys = [
        'DeviceColor',
        'Color',
        'EnclosureColor',
        'CaseColor',
        'ProductColor',
        'ExternalColor'
    ]
    
    for key in color_keys:
        if key in device_info and device_info[key]:
            color_value = device_info[key].strip()
            if color_value and color_value != 'N/A' and color_value != '':
                formatted = format_color_name(color_value)
                if formatted != 'N/A':
                    return formatted
    
    # Method 2: Query color directly from device
    color = query_device_color_directly(udid)
    if color and color != 'N/A' and color != '':
        return color
    
    # Method 3: Try alternative query method
    color = query_device_color_alternative(udid)
    if color and color != 'N/A' and color != '':
        return color
    
    return "N/A"

def query_device_color_directly(udid: str) -> str:
    """Query device color directly using ideviceinfo"""
    try:
        result = subprocess.run(
            ['ideviceinfo', '-u', udid, '-k', 'DeviceColor'],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        
        if result.returncode == 0 and result.stdout.strip():
            color = result.stdout.strip()
            if color and color != 'N/A' and color != '':
                return format_color_name(color)
    except:
        pass
    
    return None

def query_device_color_alternative(udid: str) -> str:
    """Try alternative color query methods"""
    queries = [
        ['ideviceinfo', '-u', udid, '-k', 'Color'],
        ['ideviceinfo', '-u', udid, '-q', 'com.apple.product.model.marketing-name']
    ]
    
    for cmd in queries:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
            
            if result.returncode == 0 and result.stdout.strip():
                color = result.stdout.strip()
                if color and color != 'N/A' and color != '':
                    return format_color_name(color)
        except:
            continue
    
    return None

def format_color_name(color_value: str) -> str:
    """Format color name to readable format"""
    if not color_value or color_value == 'N/A' or color_value == '':
        return "N/A"
    
    # Clean color string - remove leading/trailing non-alphabetic characters
    color_clean = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z\s]+$', '', color_value)
    color_clean = color_clean.strip()
    
    if not color_clean:
        return "N/A"
    
    # Comprehensive color mappings for all iPhone models
    color_map = {
        # Basic colors
        'black': 'Black',
        'spacegray': 'Space Gray',
        'spacegrey': 'Space Gray',
        'silver': 'Silver',
        'white': 'White',
        'gold': 'Gold',
        'rosegold': 'Rose Gold',
        'rose gold': 'Rose Gold',
        
        # iPhone 11 Series
        'purple': 'Purple',
        'green': 'Green',
        'yellow': 'Yellow',
        'red': 'Red',
        'productred': 'Product Red',
        'blue': 'Blue',
        
        # iPhone 12 Series
        'midnight': 'Midnight',
        'starlight': 'Starlight',
        'bluesky': 'Blue',
        'darkblue': 'Blue',
        
        # iPhone 13 Series
        'sierra': 'Sierra Blue',
        'sierrablue': 'Sierra Blue',
        'alpinegreen': 'Alpine Green',
        'alpine': 'Alpine Green',
        'greenish': 'Green',
        
        # iPhone 14 Series
        'deepviolet': 'Deep Purple',
        'indigo': 'Indigo',
        'maroon': 'Maroon',
        'darkred': 'Red',
        
        # iPhone 15 Series
        'natural': 'Natural Titanium',
        'titanium': 'Natural Titanium',
        'blacktitanium': 'Black Titanium',
        'whitetitanium': 'White Titanium',
        'bluetitanium': 'Blue Titanium',
    }
    
    color_lower = color_clean.lower()
    
    # Check for exact matches first
    if color_lower in color_map:
        return color_map[color_lower]
    
    # Check for partial matches
    for key, value in color_map.items():
        if key in color_lower or color_lower in key:
            return value
    
    # If no match found, capitalize each word
    formatted = ' '.join(word.capitalize() for word in color_clean.split())
    
    # Validate that it's a reasonable color name (not too short, contains letters)
    if len(formatted) >= 2 and any(c.isalpha() for c in formatted):
        return formatted
    
    return "N/A"