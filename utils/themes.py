class ThemeManager:
    THEMES = {
        "default": {
            "success": "green",
            "error": "red", 
            "warning": "yellow",
            "info": "blue",
            "prompt": "magenta",
            "banner": "red"
        },
        "dark": {
            "success": "#50fa7b",
            "error": "#ff5555",
            "warning": "#f1fa8c",
            "info": "#8be9fd",
            "prompt": "#bd93f9",
            "banner": "#ff79c6"
        },
        "matrix": {
            "success": "#00ff00", 
            "error": "#ff0000",
            "warning": "#ffff00",
            "info": "#00ffff",
            "prompt": "#ff00ff",
            "banner": "#00ff00"
        },
        "blue": {
            "success": "#00bfff",
            "error": "#ff4500",
            "warning": "#ffd700",
            "info": "#1e90ff",
            "prompt": "#9370db",
            "banner": "#4169e1"
        }
    }
    
    def __init__(self):
        self.current_theme = self.THEMES["default"]
        
    def set_theme(self, theme_name):
        if theme_name in self.THEMES:
            self.current_theme = self.THEMES[theme_name]
            return True
        return False
        
    def list_themes(self):
        return list(self.THEMES.keys())
        
    def get_theme_color(self, color_type):
        return self.current_theme.get(color_type, "white")
