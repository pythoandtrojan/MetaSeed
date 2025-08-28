import socket
import time
from rich.console import Console

console = Console()

class ConnectionPool:
    def __init__(self):
        self.connections = {}
        self.retry_attempts = 3
        self.retry_delay = 2
        
    def get_connection(self, session_id):
        if session_id in self.connections:
            # Verificar se a conexão ainda está ativa
            if self._check_connection(session_id):
                return self.connections[session_id]
            else:
                # Tentar reconectar
                if self._reconnect(session_id):
                    return self.connections[session_id]
        return None
        
    def _check_connection(self, session_id):
        try:
            # Tentar enviar um ping
            self.connections[session_id]["socket"].send(b"\x00")
            return True
        except:
            return False
            
    def _reconnect(self, session_id):
        conn_info = self.connections[session_id]
        for attempt in range(self.retry_attempts):
            try:
                console.print(f"[yellow]Tentando reconectar ({attempt + 1}/{self.retry_attempts})...[/yellow]")
                
                if conn_info["protocol"] == "tcp":
                    new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    new_sock.connect((conn_info["host"], conn_info["port"]))
                else:
                    new_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    
                self.connections[session_id]["socket"] = new_sock
                console.print("[green]✓ Reconexão bem-sucedida[/green]")
                return True
                
            except Exception as e:
                console.print(f"[red]✗ Falha na reconexão: {e}[/red]")
                time.sleep(self.retry_delay)
                
        return False
        
    def add_connection(self, session_id, socket_obj, host, port, protocol):
        self.connections[session_id] = {
            "socket": socket_obj,
            "host": host,
            "port": port,
            "protocol": protocol
        }
        
    def remove_connection(self, session_id):
        if session_id in self.connections:
            try:
                self.connections[session_id]["socket"].close()
            except:
                pass
            del self.connections[session_id]
