import socket
import threading
import time
from rich.console import Console
from rich.table import Table

console = Console()

class ConnectionManager:
    def __init__(self):
        self.connection_mode = "listener"  # listener or connector
        self.active_connections = {}
        self.connection_threads = {}
        
    def set_mode(self, mode):
        if mode.lower() in ["listener", "connector"]:
            self.connection_mode = mode.lower()
            console.print(f"[green]✓ Modo de conexão definido para: {self.connection_mode}[/green]")
            return True
        else:
            console.print("[red]✗ Modo deve ser 'listener' ou 'connector'[/red]")
            return False
            
    def start_listener(self, lhost, lport, protocol="tcp"):
        """Inicia um listener na porta especificada"""
        try:
            if protocol.lower() == "tcp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((lhost, lport))
                sock.listen(5)
            elif protocol.lower() == "udp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind((lhost, lport))
            else:
                console.print(f"[red]✗ Protocolo não suportado: {protocol}[/red]")
                return False
                
            console.print(f"[green]✓ Listener iniciado em {lhost}:{lport} ({protocol.upper()})[/green]")
            console.print(f"[yellow][+] Aguardando conexões...[/yellow]")
            
            # Thread para aceitar conexões
            thread = threading.Thread(target=self._accept_connections, args=(sock, protocol))
            thread.daemon = True
            thread.start()
            
            self.active_connections[f"{lhost}:{lport}"] = {
                "socket": sock,
                "thread": thread,
                "protocol": protocol,
                "type": "listener"
            }
            
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Erro ao iniciar listener: {e}[/red]")
            return False
            
    def start_connector(self, rhost, rport, protocol="tcp"):
        """Conecta a um host remoto"""
        try:
            if protocol.lower() == "tcp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                console.print(f"[yellow][+] Conectando a {rhost}:{rport}...[/yellow]")
                sock.connect((rhost, rport))
            elif protocol.lower() == "udp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                console.print(f"[red]✗ Protocolo não suportado: {protocol}[/red]")
                return False
                
            console.print(f"[green]✓ Conectado a {rhost}:{rport} ({protocol.upper()})[/green]")
            
            # Salvar conexão
            conn_id = f"conn_{rhost}:{rport}"
            self.active_connections[conn_id] = {
                "socket": sock,
                "protocol": protocol,
                "type": "connector",
                "remote": (rhost, rport)
            }
            
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Erro ao conectar: {e}[/red]")
            return False
            
    def _accept_connections(self, sock, protocol):
        """Aceita conexões entrantes (para listeners)"""
        while True:
            try:
                if protocol == "tcp":
                    client_socket, client_address = sock.accept()
                    console.print(f"[green]✓ Conexão recebida de {client_address[0]}:{client_address[1]}[/green]")
                    
                    # Adicionar à lista de conexões ativas
                    conn_id = f"listener_{client_address[0]}:{client_address[1]}"
                    self.active_connections[conn_id] = {
                        "socket": client_socket,
                        "protocol": protocol,
                        "type": "accepted",
                        "remote": client_address
                    }
                    
                elif protocol == "udp":
                    data, address = sock.recvfrom(1024)
                    console.print(f"[green]✓ Dados recebidos de {address[0]}:{address[1]}[/green]")
                    console.print(f"[blue]Dados: {data.decode()}[/blue]")
                    
            except Exception as e:
                console.print(f"[red]✗ Erro no listener: {e}[/red]")
                break
                
    def list_connections(self):
        """Lista todas as conexões ativas"""
        if not self.active_connections:
            console.print("[yellow]Nenhuma conexão ativa[/yellow]")
            return
            
        table = Table(title="Conexões Ativas")
        table.add_column("ID", style="cyan")
        table.add_column("Tipo", style="green")
        table.add_column("Endereço", style="yellow")
        table.add_column("Protocolo")
        table.add_column("Status")
        
        for conn_id, conn in self.active_connections.items():
            if conn["type"] == "listener":
                address = f"{conn['socket'].getsockname()[0]}:{conn['socket'].getsockname()[1]}"
                status = "Aguardando"
            elif conn["type"] == "connector":
                address = f"{conn['remote'][0]}:{conn['remote'][1]}"
                status = "Conectado"
            else:
                address = f"{conn['remote'][0]}:{conn['remote'][1]}"
                status = "Ativo"
                
            table.add_row(
                conn_id,
                conn["type"],
                address,
                conn["protocol"].upper(),
                status
            )
            
        console.print(table)
        
    def send_data(self, conn_id, data):
        """Envia dados através de uma conexão"""
        if conn_id not in self.active_connections:
            console.print(f"[red]✗ Conexão não encontrada: {conn_id}[/red]")
            return False
            
        conn = self.active_connections[conn_id]
        
        try:
            if conn["protocol"] == "tcp":
                conn["socket"].send(data.encode())
            elif conn["protocol"] == "udp":
                if conn["type"] == "listener":
                    # UDP listeners não têm conexão específica
                    console.print("[red]✗ UDP listeners requerem endereço específico[/red]")
                    return False
                else:
                    conn["socket"].sendto(data.encode(), conn["remote"])
                    
            console.print(f"[green]✓ Dados enviados para {conn_id}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Erro ao enviar dados: {e}[/red]")
            return False
            
    def close_connection(self, conn_id):
        """Fecha uma conexão específica"""
        if conn_id not in self.active_connections:
            console.print(f"[red]✗ Conexão não encontrada: {conn_id}[/red]")
            return False
            
        conn = self.active_connections[conn_id]
        
        try:
            conn["socket"].close()
            del self.active_connections[conn_id]
            console.print(f"[green]✓ Conexão {conn_id} fechada[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Erro ao fechar conexão: {e}[/red]")
            return False
            
    def close_all_connections(self):
        """Fecha todas as conexões ativas"""
        for conn_id in list(self.active_connections.keys()):
            self.close_connection(conn_id)
