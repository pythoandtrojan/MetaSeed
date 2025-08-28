import requests
from rich.console import Console
from rich.table import Table

console = Console()

class CNPJAPI:
    def __init__(self, cache):
        self.cache = cache
        self.base_url = "https://receitaws.com.br/v1/cnpj"
        
    def search_cnpj(self, cnpj):
        # Limpar CNPJ (remover caracteres não numéricos)
        cnpj_clean = ''.join(filter(str.isdigit, cnpj))
        
        # Verificar cache primeiro
        cached_data = self.cache.get_api_data("cnpj", cnpj_clean)
        if cached_data:
            console.print("[yellow]Dados obtidos do cache[/yellow]")
            return cached_data
            
        try:
            console.print(f"[blue]Consultando CNPJ: {cnpj_clean}[/blue]")
            response = requests.get(f"{self.base_url}/{cnpj_clean}", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data["status"] == "OK":
                    # Salvar no cache
                    self.cache.store_api_data("cnpj", cnpj_clean, data)
                    
                    table = Table(title=f"Informações do CNPJ {cnpj_clean}")
                    table.add_column("Campo", style="cyan")
                    table.add_column("Valor", style="green")
                    
                    # Informações básicas
                    basic_info = {
                        "Nome": data.get("nome", ""),
                        "Fantasia": data.get("fantasia", ""),
                        "Situação": data.get("situacao", ""),
                        "Tipo": data.get("tipo", ""),
                        "Porte": data.get("porte", ""),
                        "Abertura": data.get("abertura", ""),
                    }
                    
                    for key, value in basic_info.items():
                        table.add_row(key, str(value))
                        
                    console.print(table)
                    
                    # Atividade principal
                    if data.get("atividade_principal"):
                        console.print("\n[bold]Atividade Principal:[/bold]")
                        for atividade in data["atividade_principal"]:
                            console.print(f"  {atividade['code']} - {atividade['text']}")
                    
                    return data
                else:
                    console.print(f"[red]✗ CNPJ não encontrado ou inválido[/red]")
            else:
                console.print(f"[red]✗ Erro na API: {response.status_code}[/red]")
                
        except Exception as e:
            console.print(f"[red]✗ Erro ao consultar CNPJ: {e}[/red]")
            
        return None
