import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_path = Path("config/metaseed.conf")
        self.default_config = {
            "LHOST": "0.0.0.0",
            "LPORT": 4444,
            "PROTOCOL": "tcp",
            "PAYLOAD": "windows/meterpreter/reverse_tcp",
            "ENCODING": "plain",
            "AUTO_START": False,
            "ENABLE_LOGGING": True,
            "LOG_FILE": "metaseed.log",
            "DATABASE_PATH": "data/database.db",
            "BANNER_STYLE": "random",
            "CHECK_UPDATES": True,
            "CONNECTION_MODE": "listener",  # listener or connector
            "RHOST": "127.0.0.1",
            "RPORT": 4444,
            "THEME": "default",
            "API_TIMEOUT": 10,
            "NOTIFICATION_WEBHOOK": ""
        }
        self.settings = self.default_config.copy()
        self.load_config()
        
    def load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
            except:
                pass
                
    def save_config(self):
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.settings, f, indent=4)
            
    def get(self, key):
        return self.settings.get(key.upper())
        
    def set(self, key, value):
        self.settings[key.upper()] = value
        self.save_config()
        
    def show(self):
        from rich.console import Console
        from rich.table import Table
        
        console = Console()
        table = Table(title="Configurações Atuais")
        table.add_column("Opção", style="cyan")
        table.add_column("Valor", style="green")
        
        for key, value in self.settings.items():
            table.add_row(key, str(value))
            
        console.print(table)
