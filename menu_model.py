from datetime import datetime

class MenuItem:
    """Simple class for controlling sidebar menu items"""
    
    def __init__(self, id, name, display_name, icon, url, order=0, is_visible=True, is_admin_only=False):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.icon = icon
        self.url = url
        self.order = order
        self.is_visible = is_visible
        self.is_admin_only = is_admin_only
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<MenuItem {self.display_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'icon': self.icon,
            'url': self.url,
            'order': self.order,
            'is_visible': self.is_visible,
            'is_admin_only': self.is_admin_only
        }
