import readline
import os
from pathlib import Path

class CommandHistory:
    def __init__(self, history_file=".metaseed_history"):
        self.history_file = Path(history_file)
        self.load_history()
        
    def load_history(self):
        try:
            if self.history_file.exists():
                readline.read_history_file(str(self.history_file))
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass
            
    def save_history(self):
        self.history_file.parent.mkdir(exist_ok=True)
        readline.write_history_file(str(self.history_file))
        
    def search_history(self, pattern):
        history_items = []
        for i in range(1, readline.get_current_history_length() + 1):
            item = readline.get_history_item(i)
            if pattern.lower() in item.lower():
                history_items.append(item)
        return history_items
        
    def clear_history(self):
        readline.clear_history()
        if self.history_file.exists():
            self.history_file.unlink()
