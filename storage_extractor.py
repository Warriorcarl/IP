# storage_extractor.py
import subprocess
import re

def extract_storage_capacity_real(device_info: dict, udid: str) -> str:
    """
    Extract REAL storage capacity using multiple methods
    Returns storage in GB or 'N/A' if cannot determine
    """
    
    storage_bytes = None
    
    # Method 1: Try from device info keys directly
    storage_keys = [
        'TotalDataCapacity',
        'TotalDiskCapacity',
        'DeviceCapacity',
        'NANDVolumeUsage',
        'DiskUsage'
    ]
    
    for key in storage_keys:
        if key in device_info and device_info[key]:
            value = device_info[key]
            if value and value != '0' and value.isdigit():
                storage_bytes = value
                break
    
    # Method 2: Try using system profiler query (com.apple.disk_usage.factory)
    if not storage_bytes or storage_bytes == '0':
        try:
            result = subprocess.run(
                ['ideviceinfo', '-u', udid, '-q', 'com.apple.disk_usage.factory'],
                capture_output=True,
                text=True,
                check=False,
                timeout=10
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if ': ' in line:
                        key, value = line.split(': ', 1)
                        if 'TotalDiskCapacity' in key or 'TotalDataCapacity' in key:
                            if value.isdigit() and value != '0':
                                storage_bytes = value
                                break
        except:
            pass
    
    # Method 3: Try alternative query for TotalDiskCapacity key
    if not storage_bytes or storage_bytes == '0':
        try:
            result = subprocess.run(
                ['ideviceinfo', '-u', udid, '-k', 'TotalDiskCapacity'],
                capture_output=True,
                text=True,
                check=False,
                timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                value = result.stdout.strip()
                if value.isdigit() and value != '0':
                    storage_bytes = value
        except:
            pass
    
    # Convert bytes to GB
    if storage_bytes and storage_bytes.isdigit():
        try:
            storage_gb = int(storage_bytes) / (1024 ** 3)
            
            # Common iPhone storage capacities
            common_capacities = [16, 32, 64, 128, 256, 512, 1024]
            
            # Find closest capacity with better tolerance
            closest_capacity = min(common_capacities, key=lambda x: abs(x - storage_gb))
            
            # Calculate tolerance as percentage of the closest capacity
            # Use 20% tolerance for better matching
            tolerance_percent = 0.20
            tolerance = closest_capacity * tolerance_percent
            
            # If within tolerance range, use the standard capacity
            if abs(storage_gb - closest_capacity) <= tolerance:
                return f"{closest_capacity} GB"
            
            # Special handling for edge cases
            # If between 32-64: likely 64 GB
            if 32 < storage_gb < 96:
                return "64 GB"
            # If between 64-192: likely 128 GB
            elif 64 < storage_gb < 192:
                return "128 GB"
            # If between 192-384: likely 256 GB
            elif 192 < storage_gb < 384:
                return "256 GB"
            # If between 384-768: likely 512 GB
            elif 384 < storage_gb < 768:
                return "512 GB"
            # If > 768: likely 1 TB
            elif storage_gb >= 768:
                return "1024 GB"
            else:
                # Fallback to closest standard capacity
                return f"{closest_capacity} GB"
                    
        except (ValueError, TypeError):
            return "N/A"
    
    return "N/A"