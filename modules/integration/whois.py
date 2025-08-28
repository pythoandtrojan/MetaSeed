import whois
import pythonwhois
from rich.console import Console
from rich.table import Table

console = Console()

class WhoisIntegration:
    def __init__(self, cache):
        self.cache = cache
        
    def domain_info(self, domain):
        # Verificar cache primeiro
        cached_data = self.cache.get_api_data("whois", domain)
        if cached_data:
            console.print("[yellow]Dados obtidos do cache[/yellow]")
            return cached_data
            
        try:
            console.print(f"[blue]Consultando WHOIS: {domain}[/blue]")
            
            # Tentar com python-whois primeiro
            try:
                domain_info = whois.whois(domain)
            except:
                # Fallback para pythonwhois
                domain_info = pythonwhois.get_whois(domain)
                
            if domain_info:
                # Salvar no cache
                self.cache.store_api_data("whois", domain, domain_info)
                
                table = Table(title=f"Informações WHOIS para {domain}")
                table.add_column("Campo", style="cyan")
                table.add_column("Valor", style="green")
                
                # Converter para dict se necessário
                if hasattr(domain_info, '__dict__'):
                    domain_info = domain_info.__dict__
                    
                for key, value in domain_info.items():
                    if value and str(value).strip():
                        table.add_row(key.upper(), str(value))
                        
                console.print(table)
                return domain_info
            else:
                console.print("[red]✗ Não foi possível obter informações WHOIS[/red]")
                
        except Exception as e:
            console.print(f"[red]✗ Erro ao consultar WHOIS: {e}[/red]")
            
        return None
