import random
import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner

console = Console()

BANNERS = [
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
    """,
    """
 .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. |
| |  _________   | || | _____  _____ | || |      __      | || |  _______     | |
| | |  _   _  |  | || ||_   _||_   _|| || |     /  \     | || | |_   __ \    | |
| | |_/ | | \_|  | || |  | |    | |  | || |    / /\ \    | || |   | |__) |   | |
| |     | |      | || |  | '    ' |  | || |   / ____ \   | || |   |  __ /    | |
| |    _| |_     | || |   \ `--' /   | || | _/ /    \ \_ | || |  _| |  \ \_  | |
| |   |_____|    | || |    `.__.'    | || ||____|  |____|| || | |____| |___| | |
| |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------' 
    """,
    """
╦ ╦┌─┐┌┬┐┌─┐  ┌─┐┌─┐┌┬┐┬┌─┐┌┐┌┌─┐
║║║├┤  │ ├┤   ├┤ │ │││││ ││││└─┐
╚╩╝└─┘ ┴ └─┘  └  └─┘┴ ┴└─┘┘└┘└─┘
    """
]

def loading_animation(message, duration=3):

    spinners = [
        "dots", "dots2", "dots3", "dots4", "dots5", "dots6", "dots7", "dots8", 
        "dots9", "dots10", "dots11", "dots12", "line", "pipe", "simpleDots", 
        "simpleDotsScrolling", "star", "star2", "flip", "hamburger", "growVertical", 
        "growHorizontal", "balloon", "balloon2", "noise", "bounce", "boxBounce", 
        "boxBounce2", "triangle", "arc", "circle", "squareCorners", "circleQuarters", 
        "circleHalves", "squish", "toggle", "toggle2", "toggle3", "toggle4", "toggle5", 
        "toggle6", "toggle7", "toggle8", "toggle9", "toggle10", "toggle11", "toggle12", 
        "toggle13", "arrow", "arrow2", "arrow3", "bouncingBar", "bouncingBall", 
        "smiley", "monkey", "hearts", "clock", "earth", "moon", "runner", "pong", 
        "shark", "dqpb", "weather", "christmas", "grenade", "point", "layer", 
        "betaWave", "fingerDance", "fistBump", "soccerHeader", "mindblown", "speaker", 
        "orangePulse", "bluePulse", "orangeBluePulse", "timeTravel", "aesthetic"
    ]
    
    spinner_name = random.choice(spinners)
    end_time = time.time() + duration
    
    with console.status(f"[bold green]{message}", spinner=spinner_name) as status:
        while time.time() < end_time:
            time.sleep(0.1)

def show_banner(style="random"):

    if style == "random":
        banner = random.choice(BANNERS)
    else:
        try:
            index = int(style)
            banner = BANNERS[index % len(BANNERS)]
        except:
            banner = random.choice(BANNERS)
    
    console.print(Panel.fit(banner, title="[bold red]METASEED FRAMEWORK[/bold red]", border_style="red"))
    
    warning = Text("⚠️  USE APENAS PARA FINS EDUCACIONAIS E TESTES AUTORIZADOS! ⚠️", style="bold yellow")
    console.print(Panel.fit(warning, border_style="yellow"))
    
def show_version():

    from utils.updater import check_updates
    version = "4.0"
    
    console.print(Panel.fit(f"Metaseed Framework v{version}", title="[bold green]Versão[/bold green]"))
    
    # Verificar atualizações
    if check_updates(version):
        console.print("[yellow]⚠️  Uma nova versão está disponível! Use 'update' para atualizar.[/yellow]")
