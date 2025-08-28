import requests
from rich.console import Console
from rich.table import Table

console = Console()

class CEPAPI:
    def __init__(self, cache):
        self.cache = cache
        self.base_url = "https://viacep.com.br/ws"
        
    def search_cep(self, cep):
        # Verificar cache primeiro
        cached_data = self.cache.get_api_data("cep", cep)
        if cached_data:
            console.print("[yellow]Dados obtidos do cache[/yellow]")
            return cached_data
            
        try:
            console.print(f"[blue]Consultando CEP: {cep}[/blue]")
            response = requests.get(f"{self.base_url}/{cep}/json/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if "erro" not in data:
                    # Salvar no cache
                    self.cache.store_api_data("cep", cep, data)
                    
                    table = Table(title=f"Informações do CEP {cep}")
                    table.add_column("Campo", style="cyan")
                    table.add_column("Valor", style="green")
                    
                    for key, value in data.items():
                        table.add_row(key.upper(), str(value))
                        
                    console.print(table)
                    return data
                else:
                    console.print("[red]✗ CEP não encontrado[/red]")
            else:
                console.print(f"[red]✗ Erro na API: {response.status_code}[/red]")
                
        except Exception as e:
            console.print(f"[red]✗ Erro ao consultar CEP: {e}[/red]")
            
        return None
