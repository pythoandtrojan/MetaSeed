# Configurações padrão do Metaseed
DEFAULT_CONFIG = {
    "LHOST": "0.0.0.0",
    "LPORT": 4444,
    "PAYLOAD": "reverse_shell",
    "ENCODING": "plain",
    "AUTO_START": False,
    "ENABLE_LOGGING": True,
    "LOG_FILE": "metaseed.log"
}

class Config:
    def __init__(self):
        self.settings = DEFAULT_CONFIG.copy()
        
    def get(self, key):
        return self.settings.get(key.upper())
        
    def set(self, key, value):
        self.settings[key.upper()] = value
        
    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                import json
                loaded_settings = json.load(f)
                self.settings.update(loaded_settings)
        except:
            pass
            
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            import json
            json.dump(self.settings, f, indent=4)
