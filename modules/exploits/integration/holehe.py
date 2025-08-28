import requests
import json
from rich.console import Console
from rich.table import Table

console = Console()

class HoleheIntegration:
    def __init__(self, cache):
        self.cache = cache
        self.api_url = "https://api.holehe.tuxify.com/v1/email"
        
    def check_email(self, email):
        # Verificar cache primeiro
        cached_data = self.cache.get_api_data("holehe", email)
        if cached_data:
            console.print("[yellow]Dados obtidos do cache[/yellow]")
            return cached_data
            
        try:
            console.print(f"[blue]Verificando email: {email}[/blue]")
            response = requests.post(self.api_url, json={"email": email}, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Salvar no cache
                self.cache.store_api_data("holehe", email, data)
                
                table = Table(title=f"Resultados Holehe para {email}")
                table.add_column("Serviço", style="cyan")
                table.add_column("Existente", style="green")
                table.add_column("Email", style="yellow")
                
                for service, info in data.items():
                    exists = "✅" if info["exists"] else "❌"
                    email_display = info.get("email", email)
                    table.add_row(service, exists, email_display)
                    
                console.print(table)
                return data
            else:
                console.print(f"[red]✗ Erro na API Holehe: {response.status_code}[/red]")
                
        except Exception as e:
            console.print(f"[red]✗ Erro ao verificar email: {e}[/red]")
            
        return None
