# localization.py - LENGKAP DENGAN SEMUA STRING
# Lokalisasi teks Bahasa Indonesia

# Application Info
APP_TITLE = "iPhone Device Scanner Pro"

# Session-related strings
SESSION_FILES = "File Session"
SESSION_NO_COLOR = "Session Tanpa Warna"
SESSION_WITH_COLOR = "Session Dengan Warna"
COLOR_SESSION = "Warna Manual"
STANDARD_SESSION = "Standar"

# IMEI loading/saving
LOADED_IMEIS = "Memuat"
SEEN_IMEIS_FROM = "IMEI yang sudah dilihat dari"
SESSION = "session"
NO_IMEI_FILE = "File IMEI tidak ditemukan untuk"
CREATING_NEW = "Membuat file baru"
SAVED_IMEIS = "Menyimpan"
IMEIS_TO = "IMEI ke"
ERROR_LOADING_IMEIS = "Gagal memuat IMEI"
ERROR_SAVING_IMEIS = "Gagal menyimpan IMEI"
ERROR_SAVING = "Gagal menyimpan"

# Reset operations
CLEARED_IMEI_LIST = "Daftar IMEI dibersihkan"
RESET_COMPLETED = "Reset selesai"
FILES_DELETED = "file dihapus"
ERROR_RESETTING_DATA = "Gagal mereset data"

# File operations
LOADED_ENTRIES = "Memuat"
ENTRIES_FROM = "entri dari"
DELETED = "Dihapus"

# Device scanning
FOUND_DEVICES = "Ditemukan"
DEVICE_SINGULAR_PLURAL = "perangkat"
SCANNING_DEVICE = "Memindai perangkat"
SAVE_CONFIRMATION = "Simpan perangkat ini? (y/n, enter=y): "

# Monitoring
MANUAL_COLOR_MODE = "Warna Manual"
SHUTDOWN_MODE = "Shutdown"
DEVICE_MONITORING = "Monitoring Perangkat"
INSTRUCTION_CONNECT = "Hubungkan iPhone baru via USB"
INSTRUCTION_COLOR_PROMPT = "Anda akan diminta untuk memilih warna perangkat"
INSTRUCTION_AUTO_EXTRACT = "Informasi akan diekstrak secara otomatis"
INSTRUCTION_AUTO_SHUTDOWN = "Perangkat akan dimatikan setelah ekstraksi"
INSTRUCTION_STOP = "Tekan Ctrl+C untuk berhenti"
MONITORING_STOPPED = "Monitoring dihentikan"

# Labels
LABEL_CSV = "File CSV"
LABEL_EXCEL = "File Excel"
LABEL_SEEN_IMEI = "Daftar IMEI"
LABEL_PRODUCT = "📱 Produk"
LABEL_STORAGE = "📊 Penyimpanan"
LABEL_IMEI1 = "📋 IMEI 1"

# Status messages
APP_ERROR = "Kesalahan aplikasi"
APP_TERMINATED = "Aplikasi dihentikan"
ERROR_GENERAL = "Kesalahan"
ERROR_GET_UDIDS = "Gagal mendapatkan UDID"
ERROR_EXTRACTION = "Kesalahan ekstraksi"

# Main Menu
MENU_TITLE = "MENU UTAMA"
SELECT_OPTION = "🔎 Pilih opsi"

MENU_OPTIONS = {
    "1": ("📱 Pantau & Ekstrak", "Ekstrak info (tanpa warna manual)"),
    "2": ("🎨 Pantau & Ekstrak + Warna", "Ekstrak + pilih warna manual"),
    "3": ("📱⏻ Pantau + Matikan", "Ekstrak lalu matikan perangkat"),
    "4": ("🎨 Pantau + Matikan + Warna", "Ekstrak + warna + matikan"),
    "5": ("🔍 Pindai Perangkat Aktif", "Pindai semua perangkat terhubung"),
    "6": ("🔍🔄 Pindai dengan Reset", "Reset data terlebih dahulu"),
    "7": ("📋 Lihat IMEI Tersimpan", "Tampilkan daftar IMEI yang diproses"),
    "8": ("🗑️  Hapus IMEI Tersimpan", "Reset daftar IMEI"),
    "9": ("🗑️  Reset Semua Data", "Hapus semua file output dan IMEI"),
    "10": ("🚪 Keluar", "Tutup aplikasi")
}

# Device Monitoring
DEVICE_MONITORING = "PEMANTAUAN PERANGKAT"
DEVICE_MONITORING_WITH_COLOR = "PEMANTAUAN PERANGKAT + WARNA MANUAL"
DEVICE_MONITORING_WITH_SHUTDOWN = "PEMANTAUAN PERANGKAT + MATIKAN"
DEVICE_MONITORING_WITH_BOTH = "PEMANTAUAN PERANGKAT + WARNA + MATIKAN"

INSTRUCTIONS = "Petunjuk:"
CONNECT_IPHONE = "• Hubungkan iPhone baru melalui USB"
AUTOMATICALLY_EXTRACTED = "• Informasi akan diekstrak secara otomatis"
COLOR_SELECTION_INFO = "• Anda akan diminta memilih warna perangkat"
PRESS_CTRL_C = "• Tekan Ctrl+C untuk berhenti"

# Device Detection and Extraction
NEW_DEVICE_DETECTED = "✅ Perangkat baru terdeteksi"
EXTRACTING_DEVICE = "ℹ️ Mengekstrak perangkat"
EXTRACTION_COMPLETED = "✅ Ekstraksi selesai dalam"
DEVICE_ALREADY_SCANNED = "⚠️  Perangkat sudah dipindai!"

DEVICE_INFO_HEADER = "INFORMASI PERANGKAT"
PRODUCT = "📱 Produk"
MODEL = "⚙️ Model"
COLOR = "🎨 Warna"
SERIAL = "🔒 Serial"
PART = "🏁 Part"
STORAGE = "📊 Penyimpanan"
MODEL_ID = "📋 ID Model"
UPC = "⭐ UPC"
IMEI_1 = "📱 IMEI 1"
IMEI_2 = "📱 IMEI 2"
DEVICE_NAME = "🏷️ Nama Perangkat"
IOS_VERSION = "⚙️ Versi iOS"

ALREADY_PROCESSED = "💡 Perangkat ini sudah diproses dan tersimpan."
CONNECT_DIFFERENT = "✅ Hubungkan PERANGKAT LAIN untuk melanjutkan."

# Color Selection
SELECT_COLOR = "🎨 PILIH WARNA PERANGKAT"
SELECTED_COLOR = "✅ Warna Terpilih"
SELECT_COLOR_PROMPT = "🎨 Pilih warna"
INVALID_CHOICE = "❌ Pilihan tidak valid. Silakan pilih"

# File Operations
SAVED_CSV = "✅ Tersimpan di"
SAVED_EXCEL = "✅ Tersimpan di"
SAVED_BOTH = "✅ Tersimpan di kedua file"
DEVICE_SAVED = "✅ 🏆 PERANGKAT TERSIMPAN!"

# Monitoring Status
MONITORING = "⏳ Pemantauan"
DEVICES = "Perangkat"
NO_DEVICES = "❌ Tidak ada perangkat yang terhubung"
MONITORING_STOPPED = "🛑 Pemantauan dihentikan"

# Scan Operations
SCAN_CURRENT_DEVICES = "PINDAI PERANGKAT AKTIF"
FOUND_DEVICES = "✅ Ditemukan"
DEVICE = "perangkat"
SCAN_WITH_RESET = "PINDAI DENGAN RESET"
RESET_IMEI_LIST = "Reset daftar IMEI tersimpan. Lanjutkan?"
IMEI_LIST_CLEARED = "✅ Daftar IMEI berhasil dihapus"
SCAN_RESET_CANCELLED = "⚠️ Pindai dengan reset dibatalkan"
SAVE_DEVICE = "Simpan perangkat ini?"

# View and Clear IMEI
SEEN_IMEIS = "IMEI TERSIMPAN"
NO_IMEIS_PROCESSED = "⚠️ Belum ada IMEI yang diproses"
TOTAL_IMEIS = "Total IMEI"

CLEAR_SEEN_IMEIS = "HAPUS IMEI TERSIMPAN"
DELETE_IMEIS = "Hapus semua"
IMEIS = "IMEI tersimpan?"
SEEN_IMEI_CLEARED = "✅ Daftar IMEI berhasil dihapus"
CLEAR_CANCELLED = "⚠️ Penghapusan dibatalkan"

# Reset All Data
RESET_ALL_DATA = "RESET SEMUA DATA"
WILL_DELETE = "⚠️  Akan menghapus:"
CSV_FILE_TEXT = "• File CSV"
EXCEL_FILE_TEXT = "• File Excel"
IMEI_LIST_TEXT = "• Daftar IMEI"
ARE_YOU_SURE = "Apakah Anda yakin?"
DELETED = "✅ Dihapus"
CLEARED = "✅ Dihapus"
ALL_DATA_RESET = "✅ Semua data berhasil direset"
RESET_CANCELLED = "⚠️ Reset dibatalkan"
ERROR_LOADING = "Gagal memuat"
NO_FILE_FOUND = "tidak ditemukan"
IMEI_FILES_CLEARED = "File IMEI dikosongkan"

# Return to Menu
RETURN_TO_MENU = "Tekan ENTER untuk kembali ke menu..."
PRESS_ENTER = "Tekan ENTER untuk melanjutkan..."
PRESS_ENTER_TO_RETURN = "Tekan ENTER untuk kembali ke menu..."

# Banner
VERSION = "Versi"
SYSTEM = "Sistem"
TIME = "Waktu"
SEEN_IMEIS_COUNT = "IMEI Tersimpan"
OUTPUT_FILES = "File Output"

# Errors and Warnings
ERROR = "❌ Kesalahan"
WARNING = "⚠️ Peringatan"
SUCCESS = "✅ Berhasil"
INFO = "ℹ️ Informasi"

THANK_YOU = "❤️ Terima kasih!"
INVALID_OPTION = "❌ Opsi tidak valid"
ERROR_OCCURRED = "Kesalahan terjadi"

# Shutdown
SHUTTING_DOWN = "⏻ Mematikan"
SHUTDOWN_OK = "✅ Perangkat berhasil dimatikan"
SHUTDOWN_FAILED = "⚠️ Matikan mungkin gagal (perangkat mungkin sudah mati)"
SHUTDOWN_TIMEOUT = "⏱️ Waktu matikan habis (normal jika perangkat mati dengan cepat)"
SHUTDOWN_DEVICE = "Mematikan perangkat"

# Warnings
WARNING_IMEI_NOT_ACCESSIBLE = "IMEI tidak dapat diakses"
WARNING_RESET = "⚠️  Ini akan menghapus:"
CONFIRM_RESET = "Apakah Anda yakin? (y/n): "
RESET_CONFIRMATION = "Ini akan mereset daftar IMEI yang sudah dilihat. Lanjutkan? (y/n): "
SCAN_CANCELLED = "Pemindaian dibatalkan"
DEVICE_ALREADY_PROCESSED = "💡 Perangkat ini sudah diproses dan tersimpan."
CONNECT_DIFFERENT_DEVICE = "✅ Silakan hubungkan PERANGKAT LAIN untuk melanjutkan."

# Confirmation
DELETE_CONFIRMATION = "Hapus semua"
IMEIS_QUESTION = "IMEI tersimpan? (y/n): "

# Misc
UNKNOWN = "Tidak Diketahui"
ENTRIES = "entri"
NO_DEVICES_CONNECTED = "Tidak ada perangkat terhubung"
VIEW_SEEN_IMEIS = "LIHAT IMEI TERSIMPAN"
NO_IMEIS_PROCESSED = "Belum ada IMEI diproses"
CLEAR_SEEN_IMEIS = "HAPUS IMEI TERSIMPAN"
DELETE_CONFIRMATION = "Hapus semua"
IMEIS_QUESTION = "IMEI tersimpan? (y/n): "
ERROR_RESET = "Kesalahan saat reset"