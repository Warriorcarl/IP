# iPhone Device Scanner Pro v5.2.0

**Real Data Only - Professional iPhone Information Extraction Tool**

## 📋 Overview

iPhone Device Scanner Pro is a powerful command-line application for extracting real device information from connected iPhones via USB. The tool automatically detects, extracts, and saves critical device data including IMEI, model information, storage capacity, color, and UPC codes.

## 🎯 Key Features

- **📱 Real-Time Device Monitoring** - Automatically detect newly connected iPhones
- **🔍 Comprehensive Data Extraction**:
  - IMEI 1 & IMEI 2 (International Mobile Equipment Identity)
  - Device Model & Product Type
  - Serial Number & Part Number
  - Storage Capacity (16GB, 32GB, 64GB, 128GB, 256GB, 512GB, 1TB)
  - Device Color
  - Model ID (A-series)
  - UPC Code (Universal Product Code)
  - iOS Version
  - Device Name
  
- **💾 Multi-Format Output**:
  - CSV Format (iphone_data.csv)
  - Excel Format (BC.xlsx)
  
- **🔄 Smart Duplicate Detection** - Detects and alerts when same device reconnects
- **🛑 Auto-Shutdown** - Optional automatic device shutdown after data extraction
- **📋 IMEI Tracking** - Maintains history of processed devices
- **🎨 Beautiful CLI Interface** - Color-coded, emoji-enhanced terminal UI

## 📋 Main Menu Options

```
[1] 📱 Monitor & Extract       Extract info from new devices
[2] 📱⏻ Monitor + Shutdown     Extract then shutdown device
[3] 🔍 Scan Current Devices    Scan all connected devices
[4] 🔍🔄 Scan with Reset        Reset data first, then scan
[5] 📋 View Seen IMEIs         Show all processed IMEIs
[6] 🗑️  Clear Seen IMEIs       Reset seen IMEI list
[7] 🗑️  Reset All Data         Delete all output files and IMEI list
[8] 🚪 Exit                    Close application
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- libimobiledevice (idevice tools)
- pandas library
- openpyxl library

### Installation

```bash
# Install required packages
pip install pandas openpyxl

# Ensure libimobiledevice is installed
# On Windows: Download from https://libimobiledevice.org/
# On macOS: brew install libimobiledevice
# On Linux: apt-get install libimobiledevice-utils
```

### Running the Application

```bash
python main.py
```

## 📁 Project Structure

```
IPHONEDUL/
├── main.py                      # Main application entry point
├── config.py                    # Configuration and constants
├── utils.py                     # Utility functions and helpers
├── colors.py                    # Color and icon definitions
├── data_manager.py              # Data management and storage
├── file_manager.py              # File I/O operations
├── device_scanner.py            # Device detection and info extraction
├── storage_extractor.py         # Storage capacity detection
├── color_detector.py            # Device color detection
├── color_selector.py            # Color mapping utilities
├── model_mapping.json           # iPhone model ID mappings
├── upc_mapping.json             # UPC code database
├── color_mapping_database.json  # Device color database
└── README.md                    # This file
```

## 🔧 Core Modules

### main.py
The main application controller. Manages the CLI menu, device monitoring loop, and user interactions.

### data_manager.py
Handles data persistence, IMEI tracking, UPC lookup, and model ID mapping.

### device_scanner.py
Manages device detection via `idevice_id` and extracts device information using `ideviceinfo`.

### file_manager.py
Handles CSV and Excel file operations for saving extracted device data.

### storage_extractor.py
Advanced storage capacity detection using multiple methods:
- Direct device info keys
- System profiler queries
- Intelligent capacity rounding

### color_detector.py
Device color detection with comprehensive color mapping for all iPhone models.

## 📊 Output Format

### CSV Format (iphone_data.csv)
```
IMEI1,IMEI2,Serial,Part,Product,Storage,ModelID,UPC
35288811...9218,35288811...8694,GQRD10WBKXKW,NT362LL/A,iPhone XR,128 GB,A1984,000813012801
```

### Excel Format (BC.xlsx)
Same data structure as CSV with formatted cells in Excel workbook.

## 🎯 Usage Examples

### Monitor and Extract (Auto-Save)
```
Select option: 1
- Application enters monitoring mode
- Automatically extracts data when new device connects
- Saves to CSV and Excel
- Press Ctrl+C to stop
```

### Monitor with Auto-Shutdown
```
Select option: 2
- Same as option 1, but automatically shuts down device after extraction
- Useful for batch processing
```

### View Processed Devices
```
Select option: 5
- Displays all IMEI numbers that have been processed
- Useful for tracking which devices have been scanned
```

## ⚙️ Configuration

Edit `config.py` to customize:
- Output file names and paths
- Product mappings
- Default settings

## 🔍 Duplicate Device Detection

When a previously scanned device reconnects:
```
⚠️  Device already scanned!
────────────────────────────────────────────────────
📱 Product: iPhone XR
📊 Storage: 128 GB
📋 IMEI 1: 35288811...8694
────────────────────────────────────────────────────

💡 This device has already been processed and saved.
✅ Please connect a DIFFERENT device to continue.
```

## 📝 Error Handling

The application includes comprehensive error handling for:
- Device not trusted (pairing issues)
- Connection timeouts
- Missing data fields
- File I/O errors
- Invalid device responses

## 🛠️ Troubleshooting

### Device Not Detected
```
1. Ensure USB cable is properly connected
2. Trust the computer on the iOS device (tap "Trust")
3. Try reconnecting the device
4. Ensure libimobiledevice is properly installed
```

### ideviceinfo Errors
```
1. Device may not be in developer mode
2. Try disconnecting and reconnecting USB
3. Update libimobiledevice tools
4. Check device trust status
```

### UPC/Storage Not Found
```
1. Device data may not be in the mapping database
2. Storage detection uses intelligent rounding
3. UPC falls back to Global region if specific region not found
```

## 📈 Performance

- Device detection: ~100ms
- Data extraction: ~300-500ms per device
- File operations: <500ms per device
- Real-time monitoring refresh: Every 2 seconds

## 🔐 Data Security

- All extracted data stored locally
- No external API calls
- IMEI history kept in `seen_imei.json`
- No data encryption (ensure secure file storage)

## 📄 License

This tool is for professional device management and testing purposes.

## 👨‍💻 Version History

**v5.2.0** (2026-01-17)
- Improved storage capacity detection
- Enhanced UPC code matching
- Better color detection
- Duplicate device warning messages
- Cleaned up test files and documentation

## 📞 Support

For issues or feature requests, please ensure:
1. libimobiledevice is correctly installed
2. All dependencies are installed (`pip install -r requirements.txt`)
3. Device is properly connected and trusted
4. Python version is 3.7 or higher

---

**Last Updated**: 2026-01-17
**Maintainer**: iPhone Device Scanner Team
