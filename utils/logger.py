import logging
from datetime import datetime
from pathlib import Path

class AdvancedLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configurar logging
        log_file = self.log_dir / f"metaseed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("metaseed")
        
    def log_command(self, command, session_id=None):
        if session_id:
            self.logger.info(f"Session {session_id}: {command}")
        else:
            self.logger.info(f"Global: {command}")
            
    def log_event(self, event_type, message):
        self.logger.info(f"{event_type}: {message}")
        
    def log_error(self, error_message):
        self.logger.error(error_message)
        
    def log_warning(self, warning_message):
        self.logger.warning(warning_message)
