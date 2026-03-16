# Menu configuration file
import json
import os

MENU_CONFIG_FILE = 'menu_items.json'

def load_menu_items():
    """Load menu items from config file"""
    abs_path = os.path.abspath(MENU_CONFIG_FILE)
    
    if os.path.exists(abs_path):
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Error loading menu items: {e}")
    
    # Return default menu items
    return [
        {"name": "dashboard", "display_name": "الرئيسية", "icon": "fas fa-home", "url": "/dashboard", "order": 1, "is_visible": True, "is_admin_only": False},
        {"name": "faults", "display_name": "الأعطال", "icon": "fas fa-list-check", "url": "/faults", "order": 2, "is_visible": True, "is_admin_only": False},
        {"name": "devices", "display_name": "إدارة الأجهزة", "icon": "fas fa-server", "url": "/devices", "order": 3, "is_visible": True, "is_admin_only": True},
        {"name": "device_faults", "display_name": "أعطال الأجهزة", "icon": "fas fa-exclamation-triangle", "url": "/device-faults", "order": 4, "is_visible": True, "is_admin_only": False},
        {"name": "ping_store", "display_name": "Ping On Store", "icon": "fas fa-satellite-dish", "url": "/ping-store", "order": 5, "is_visible": True, "is_admin_only": True},
        {"name": "import_excel", "display_name": "استيراد من Excel", "icon": "fas fa-file-excel", "url": "/faults/import-excel", "order": 6, "is_visible": True, "is_admin_only": True},
        {"name": "reports", "display_name": "التقارير", "icon": "fas fa-chart-bar", "url": "/reports", "order": 7, "is_visible": True, "is_admin_only": False},
        {"name": "chains", "display_name": "السلاسل", "icon": "fas fa-link", "url": "/chains", "order": 8, "is_visible": True, "is_admin_only": True},
        {"name": "regions", "display_name": "المناطق", "icon": "fas fa-map-marked-alt", "url": "/regions", "order": 9, "is_visible": True, "is_admin_only": True},
        {"name": "closed_branches", "display_name": "الفروع المغلقة", "icon": "fas fa-lock", "url": "/closed-branches", "order": 10, "is_visible": True, "is_admin_only": True},
        {"name": "technicians", "display_name": "الفنيين", "icon": "fas fa-users-gear", "url": "/technicians", "order": 11, "is_visible": True, "is_admin_only": True},
        {"name": "upload_document", "display_name": "رفع المستندات", "icon": "fas fa-file-upload", "url": "/upload-document", "order": 12, "is_visible": True, "is_admin_only": True},
        {"name": "settings", "display_name": "الإعدادات", "icon": "fas fa-cog", "url": "/settings", "order": 13, "is_visible": True, "is_admin_only": True},
    ]

def save_menu_items(menu_items):
    """Save menu items to config file"""
    try:
        # Get absolute path to ensure we're saving to the right location
        abs_path = os.path.abspath(MENU_CONFIG_FILE)
        print(f"💾 Saving menu items to: {abs_path}")
        
        # Create backup of current file
        if os.path.exists(abs_path):
            backup_path = abs_path + '.backup'
            import shutil
            shutil.copy2(abs_path, backup_path)
            print(f"📋 Created backup at: {backup_path}")
        
        # Sort items by order before saving
        sorted_items = sorted(menu_items, key=lambda x: x.get('order', 999))
        
        # Write to temporary file first, then move to final location
        temp_path = abs_path + '.tmp'
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_items, f, ensure_ascii=False, indent=2)
        
        # Verify the file was written correctly
        with open(temp_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        # Move temporary file to final location
        if os.path.exists(abs_path):
            os.remove(abs_path)
        os.rename(temp_path, abs_path)
        
        print(f"✅ Successfully saved {len(sorted_items)} menu items")
        print(f"📊 File verification passed: {len(saved_data)} items loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving menu items: {e}")
        import traceback
        traceback.print_exc()
        
        # Try to restore from backup if available
        backup_path = abs_path + '.backup'
        if os.path.exists(backup_path):
            try:
                import shutil
                shutil.copy2(backup_path, abs_path)
                print(f"🔄 Restored from backup: {backup_path}")
            except Exception as restore_error:
                print(f"❌ Failed to restore from backup: {restore_error}")
        
        return False

def update_menu_item(name, updates):
    """Update a specific menu item"""
    menu_items = load_menu_items()
    for item in menu_items:
        if item['name'] == name:
            item.update(updates)
            break
    return save_menu_items(menu_items)
