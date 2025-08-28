import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

class MacroSystem:
    def __init__(self):
        self.macros = {}
        self.macros_file = Path("config/macros.json")
        self.load_macros()
        
    def load_macros(self):
        if self.macros_file.exists():
            try:
                with open(self.macros_file, 'r') as f:
                    self.macros = json.load(f)
            except:
                self.macros = {}
                
    def save_macros(self):
        self.macros_file.parent.mkdir(exist_ok=True)
        with open(self.macros_file, 'w') as f:
            json.dump(self.macros, f, indent=4)
        
    def create_macro(self, name, commands):
        if not isinstance(commands, list):
            commands = [commands]
            
        self.macros[name] = commands
        self.save_macros()
        console.print(f"[green]✓ Macro '{name}' criada com {len(commands)} comandos[/green]")
        
    def execute_macro(self, name, framework):
        if name in self.macros:
            console.print(f"[blue]Executando macro: {name}[/blue]")
            for command in self.macros[name]:
                console.print(f"[yellow]>> {command}[/yellow]")
                framework.handle_command(command)
            return True
        else:
            console.print(f"[red]✗ Macro não encontrada: {name}[/red]")
            return False
            
    def list_macros(self):
        if not self.macros:
            console.print("[yellow]Nenhuma macro definida[/yellow]")
            return
            
        table = Table(title="Macros Disponíveis")
        table.add_column("Nome", style="cyan")
        table.add_column("Comandos", style="green")
        table.add_column("Ações")
        
        for name, commands in self.macros.items():
            table.add_row(name, str(len(commands)), f"[red]delete {name}[/red]")
            
        console.print(table)
        
    def delete_macro(self, name):
        if name in self.macros:
            del self.macros[name]
            self.save_macros()
            console.print(f"[green]✓ Macro '{name}' excluída[/green]")
            return True
        else:
            console.print(f"[red]✗ Macro não encontrada: {name}[/red]")
            return False
