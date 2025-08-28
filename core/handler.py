import socket
import threading
import time
from rich.console import Console
from rich.panel import Panel

class MultiHandler:
    def __init__(self, config):
        self.config = config
        self.console = Console()
        self.handlers = {}
        
    def start_handler(self, name, payload_type, lhost, lport, protocol="tcp"):
        handler_id = f"{name}_{int(time.time())}"
        
        if protocol.lower() == "tcp":
            handler = TCPHandler(lhost, lport, payload_type)
        elif protocol.lower() == "udp":
            handler = UDPHandler(lhost, lport, payload_type)
        else:
            self.console.print(f"[red]✗ Protocolo não suportado: {protocol}[/red]")
            return None
            
        if handler.start():
            self.handlers[handler_id] = handler
            self.console.print(f"[green]✓ Handler iniciado: {handler_id}[/green]")
            return handler_id
        else:
            self.console.print(f"[red]✗ Falha ao iniciar handler[/red]")
            return None
            
    def stop_handler(self, handler_id):
        if handler_id in self.handlers:
            self.handlers[handler_id].stop()
            del self.handlers[handler_id]
            self.console.print(f"[green]✓ Handler parado: {handler_id}[/green]")
            return True
        else:
            self.console.print(f"[red]✗ Handler não encontrado: {handler_id}[/red]")
            return False
            
    def list_handlers(self):
        if not self.handlers:
            self.console.print("[yellow]Nenhum handler ativo[/yellow]")
            return
            
        from rich.table import Table
        table = Table(title="Handlers Ativos")
        table.add_column("ID", style="cyan")
        table.add_column("Tipo", style="green")
        table.add_column("Endereço", style="yellow")
        table.add_column("Protocolo")
        
        for handler_id, handler in self.handlers.items():
            table.add_row(
                handler_id,
                handler.payload_type,
                f"{handler.lhost}:{handler.lport}",
                handler.protocol.upper()
            )
            
        self.console.print(table)

class TCPHandler:
    def __init__(self, lhost, lport, payload_type):
        self.lhost = lhost
        self.lport = lport
        self.payload_type = payload_type
        self.protocol = "tcp"
        self.socket = None
        self.running = False
        
    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.lhost, self.lport))
            self.socket.listen(5)
            self.running = True
            
            # Thread para aceitar conexões
            thread = threading.Thread(target=self.accept_connections)
            thread.daemon = True
            thread.start()
            
            return True
        except Exception as e:
            print(f"Erro ao iniciar handler TCP: {e}")
            return False
            
    def accept_connections(self):
        console = Console()
        console.print(f"[green]✓ Aguardando conexão {self.payload_type} em {self.lhost}:{self.lport} (TCP)...[/green]")
        
        while self.running:
            try:
                client_socket, client_address = self.socket.accept()
                console.print(f"[green]✓ Conexão recebida de {client_address[0]}:{client_address[1]}[/green]")
                
                # Aqui você pode adicionar lógica para interagir com a sessão
                
            except:
                if self.running:
                    console.print("[red]✗ Erro ao aceitar conexão[/red]")
                    
    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()

class UDPHandler:
    def __init__(self, lhost, lport, payload_type):
        self.lhost = lhost
        self.lport = lport
        self.payload_type = payload_type
        self.protocol = "udp"
        self.socket = None
        self.running = False
        
    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.lhost, self.lport))
            self.running = True
            
            # Thread para receber dados
            thread = threading.Thread(target=self.receive_data)
            thread.daemon = True
            thread.start()
            
            return True
        except Exception as e:
            print(f"Erro ao iniciar handler UDP: {e}")
            return False
            
    def receive_data(self):
        console = Console()
        console.print(f"[green]✓ Aguardando dados {self.payload_type} em {self.lhost}:{self.lport} (UDP)...[/green]")
        
        while self.running:
            try:
                data, address = self.socket.recvfrom(1024)
                console.print(f"[green]✓ Dados recebidos de {address[0]}:{address[1]}[/green]")
                console.print(f"[blue]Dados: {data.decode()}[/blue]")
            except:
                if self.running:
                    console.print("[red]✗ Erro ao receber dados[/red]")
                    
    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()
