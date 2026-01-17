# color_selector.py
# Manual color selection for iPhone models

# Complete iPhone color database based on official Apple colors
IPHONE_COLORS = {
    "iPhone 6": ["Space Gray", "Silver", "Gold"],
    "iPhone 6 Plus": ["Space Gray", "Silver", "Gold"],
    "iPhone 6s": ["Space Gray", "Silver", "Gold", "Rose Gold"],
    "iPhone 6s Plus": ["Space Gray", "Silver", "Gold", "Rose Gold"],
    "iPhone 7": ["Jet Black", "Black", "Silver", "Gold", "Rose Gold", "Red"],
    "iPhone 7 Plus": ["Jet Black", "Black", "Silver", "Gold", "Rose Gold", "Red"],
    "iPhone 8": ["Space Gray", "Silver", "Gold", "Red"],
    "iPhone 8 Plus": ["Space Gray", "Silver", "Gold", "Red"],
    "iPhone X": ["Space Gray", "Silver"],
    "iPhone XR": ["White", "Black", "Blue", "Yellow", "Coral", "Red"],
    "iPhone XS": ["Space Gray", "Silver", "Gold"],
    "iPhone XS Max": ["Space Gray", "Silver", "Gold"],
    "iPhone SE (1st generation)": ["Space Gray", "Silver", "Gold", "Rose Gold"],
    "iPhone SE (2nd generation)": ["White", "Black", "Red"],
    "iPhone SE (3rd generation)": ["Midnight", "Starlight", "Red"],
    "iPhone 11": ["White", "Black", "Green", "Yellow", "Purple", "Red"],
    "iPhone 11 Pro": ["Space Gray", "Silver", "Gold", "Midnight Green"],
    "iPhone 11 Pro Max": ["Space Gray", "Silver", "Gold", "Midnight Green"],
    "iPhone 12": ["White", "Black", "Blue", "Green", "Red", "Purple"],
    "iPhone 12 mini": ["White", "Black", "Blue", "Green", "Red", "Purple"],
    "iPhone 12 Pro": ["Graphite", "Silver", "Gold", "Pacific Blue"],
    "iPhone 12 Pro Max": ["Graphite", "Silver", "Gold", "Pacific Blue"],
    "iPhone 13": ["Starlight", "Midnight", "Blue", "Pink", "Green", "Red"],
    "iPhone 13 mini": ["Starlight", "Midnight", "Blue", "Pink", "Green", "Red"],
    "iPhone 13 Pro": ["Graphite", "Silver", "Gold", "Sierra Blue", "Alpine Green"],
    "iPhone 13 Pro Max": ["Graphite", "Silver", "Gold", "Sierra Blue", "Alpine Green"],
    "iPhone 14": ["Midnight", "Starlight", "Blue", "Purple", "Yellow", "Red"],
    "iPhone 14 Plus": ["Midnight", "Starlight", "Blue", "Purple", "Yellow", "Red"],
    "iPhone 14 Pro": ["Space Black", "Silver", "Gold", "Deep Purple"],
    "iPhone 14 Pro Max": ["Space Black", "Silver", "Gold", "Deep Purple"],
    "iPhone 15": ["Black", "Blue", "Green", "Yellow", "Pink"],
    "iPhone 15 Plus": ["Black", "Blue", "Green", "Yellow", "Pink"],
    "iPhone 15 Pro": ["Black Titanium", "White Titanium", "Blue Titanium", "Natural Titanium"],
    "iPhone 15 Pro Max": ["Black Titanium", "White Titanium", "Blue Titanium", "Natural Titanium"],
    "iPhone 16": ["Black", "White", "Green", "Pink", "Blue"],
    "iPhone 16 Plus": ["Black", "White", "Green", "Pink", "Blue"],
    "iPhone 16 Pro": ["Desert Titanium", "Gray Titanium", "White Titanium", "Black Titanium"],
    "iPhone 16 Pro Max": ["Desert Titanium", "Gray Titanium", "White Titanium", "Black Titanium"],
}

def get_colors_for_model(product_name: str) -> list:
    """Get available colors for a specific iPhone model"""
    return IPHONE_COLORS.get(product_name, [])

def display_color_selection(product_name: str) -> str:
    """Display color selection menu and return selected color"""
    from colors import Colors, Icons
    
    colors = get_colors_for_model(product_name)
    
    if not colors:
        print(f"{Colors.BRIGHT_YELLOW}⚠️  No color database found for {product_name}{Colors.RESET}")
        return "N/A"
    
    print(f"\n{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BRIGHT_WHITE}{Icons.PALETTE} SELECT DEVICE COLOR{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
    print(f"\n{Colors.BRIGHT_WHITE}📱 Product: {product_name}{Colors.RESET}\n")
    
    # Display available colors
    for i, color in enumerate(colors, 1):
        # Format display color (RED instead of PRODUCT RED)
        display_color = color.replace("Red", "RED")
        print(f"{Colors.BRIGHT_GREEN}[{i}]{Colors.RESET} {display_color}")
    
    print()
    
    # Get user selection
    while True:
        try:
            choice = input(f"{Colors.BRIGHT_GREEN}🎨 Select color (1-{len(colors)}): {Colors.RESET}").strip()
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(colors):
                selected_color = colors[choice_num - 1]
                # Format output (RED instead of PRODUCT RED)
                output_color = selected_color.replace("Red", "RED")
                print(f"\n{Colors.BRIGHT_GREEN}✅ Selected: {output_color}{Colors.RESET}\n")
                return output_color
            else:
                print(f"{Colors.BRIGHT_RED}❌ Invalid choice. Please select 1-{len(colors)}.{Colors.RESET}")
        except ValueError:
            print(f"{Colors.BRIGHT_RED}❌ Please enter a valid number.{Colors.RESET}")

def is_color_valid(product_name: str, color: str) -> bool:
    """Check if color is valid for product"""
    colors = get_colors_for_model(product_name)
    return color in colors
