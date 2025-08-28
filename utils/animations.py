import random
import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def loading_animation(message, duration=3):
    symbols = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    end_time = time.time() + duration
    
    with console.status("[bold green]Carregando...") as status:
        while time.time() < end_time:
            for symbol in symbols:
                status.update(status=f"[bold green]{symbol} {message}", spinner=symbol)
                time.sleep(0.1)

def show_random_banner():
    banners = [
        """
███████╗███████╗██████╗ ███████╗███████╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗
█████╗  █████╗  ██║  ██║█████╗  █████╗  █████╗  ██║  ██║
██╔══╝  ██╔══╝  ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║  ██║
███████╗███████╗██████╔╝███████╗███████╗███████╗██████╔╝
╚══════╝╚══════╝╚═════╝ ╚══════╝╚══════╝╚══════╝╚═════╝ 
        Advanced Penetration Testing Framework v4.0
        """,
        """
┌────────────────────────────────────────────────────────┐
│ ███╗   ███╗███████╗████████╗ █████╗ ███████╗███████╗██████╗ │
│ ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔══██╗│
│ ██╔████╔██║█████╗     ██║   ███████║███████╗█████╗  ██║  ██║│
│ ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║╚════██║██╔══╝  ██║  ██║│
│ ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║███████║███████╗██████╔╝│
│ ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝ │
└────────────────────────────────────────────────────────┘
        """,
        """
╔════════════════════════════════════════════════════════╗
║  __  __ ______ _____  ______  _____  _    _   _______ ║
║ |  \/  |  ____|  __ \|  ____|/ ____|| |  | | |__   __|║
║ | \  / | |__  | |__) | |__  | (___  | |  | |    | |   ║
║ | |\/| |  __| |  _  /|  __|  \___ \ | |  | |    | |   ║
║ | |  | | |____| | \ \| |____ ____) || |__| |    | |   ║
║ |_|  |_|______|_|  \_\______|_____/  \____/     |_|   ║
║                                                       ║
╚════════════════════════════════════════════════════════╝
        """
    ]
    
    banner = random.choice(banners)
    console.print(Panel.fit(banner, title="[bold red]METASEED FRAMEWORK[/bold red]", border_style="red"))
    
    warning = Text("⚠️  USE APENAS PARA FINS EDUCACIONAIS E TESTES AUTORIZADOS! ⚠️", style="bold yellow")
    console.print(Panel.fit(warning, border_style="yellow"))
