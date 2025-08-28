import requests
import socket
from rich.console import Console
from rich.table import Table

console = Console()

class IPAPI:
    def __init__(self, cache):
        self.cache = cache
        self.base_url = "http://ip-api.com/json"
        
    def search_ip(self, ip_address):
        # Verificar cache primeiro
        cached_data = self.cache.get_api_data("ip", ip_address)
        if cached_data:
            console.print("[yellow]Dados obtidos do cache[/yellow]")
            return cached_data
            
        try:
            console.print(f"[blue]Consultando IP: {ip_address}[/blue]")
            response = requests.get(f"{self.base_url}/{ip_address}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data["status"] == "success":
                    # Salvar no cache
                    self.cache.store_api_data("ip", ip_address, data)
                    
                    table = Table(title=f"Informações do IP {ip_address}")
                    table.add_column("Campo", style="cyan")
                    table.add_column("Valor", style="green")
                    
                    for key, value in data.items():
                        if key != "status":
                            table.add_row(key.upper(), str(value))
                            
                    console.print(table)
                    return data
                else:
                    console.print(f"[red]✗ Erro: {data.get('message', 'Desconhecido')}[/red]")
            else:
                console.print(f"[red]✗ Erro na API: {response.status_code}[/red]")
                
        except Exception as e:
            console.print(f"[red]✗ Erro ao consultar IP: {e}[/red]")
            
        return None
        
    def get_my_ip(self):
        try:
            response = requests.get("https://api.ipify.org", timeout=10)
            if response.status_code == 200:
                return response.text
        except:
            pass
            
        try:
            # Fallback para método alternativo
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            console.print("[red]✗ Não foi possível obter o IP público[/red]")
            return None
