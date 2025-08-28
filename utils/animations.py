import random
import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner

console = Console()

# Definindo spinners disponíveis
SPINNERS = {
    "dots": "dots",
    "dots2": "dots2",
    "dots3": "dots3",
    "dots4": "dots4",
    "dots5": "dots5",
    "dots6": "dots6",
    "dots7": "dots7",
    "dots8": "dots8",
    "dots9": "dots9",
    "dots10": "dots10",
    "dots11": "dots11",
    "dots12": "dots12",
    "line": "line",
    "pipe": "pipe",
    "simpleDots": "simpleDots",
    "simpleDotsScrolling": "simpleDotsScrolling",
    "star": "star",
    "star2": "star2",
    "flip": "flip",
    "hamburger": "hamburger",
    "growVertical": "growVertical",
    "growHorizontal": "growHorizontal",
    "balloon": "balloon",
    "balloon2": "balloon2",
    "noise": "noise",
    "bounce": "bounce",
    "boxBounce": "boxBounce",
    "boxBounce2": "boxBounce2",
    "triangle": "triangle",
    "arc": "arc",
    "circle": "circle",
    "squareCorners": "squareCorners",
    "circleQuarters": "circleQuarters",
    "circleHalves": "circleHalves",
    "squish": "squish",
    "toggle": "toggle",
    "toggle2": "toggle2",
    "toggle3": "toggle3",
    "toggle4": "toggle4",
    "toggle5": "toggle5",
    "toggle6": "toggle6",
    "toggle7": "toggle7",
    "toggle8": "toggle8",
    "toggle9": "toggle9",
    "toggle10": "toggle10",
    "toggle11": "toggle11",
    "toggle12": "toggle12",
    "toggle13": "toggle13",
    "arrow": "arrow",
    "arrow2": "arrow2",
    "arrow3": "arrow3",
    "bouncingBar": "bouncingBar",
    "bouncingBall": "bouncingBall",
    "smiley": "smiley",
    "monkey": "monkey",
    "hearts": "hearts",
    "clock": "clock",
    "earth": "earth",
    "moon": "moon",
    "runner": "runner",
    "pong": "pong",
    "shark": "shark",
    "dqpb": "dqpb",
    "weather": "weather",
    "christmas": "christmas",
    "grenade": "grenade",
    "point": "point",
    "layer": "layer",
    "betaWave": "betaWave",
    "fingerDance": "fingerDance",
    "fistBump": "fistBump",
    "soccerHeader": "soccerHeader",
    "mindblown": "mindblown",
    "speaker": "speaker",
    "orangePulse": "orangePulse",
    "bluePulse": "bluePulse",
    "orangeBluePulse": "orangeBluePulse",
    "timeTravel": "timeTravel",
    "aesthetic": "aesthetic"
}

def loading_animation(message, duration=3):
    """Animação de carregamento estilo Metasploit"""
    spinner_names = list(SPINNERS.keys())
    spinner_name = random.choice(spinner_names)
    
    end_time = time.time() + duration
    
    with console.status(f"[bold green]{message}", spinner=spinner_name) as status:
        while time.time() < end_time:
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
    
    banner = random.choice(banners)
    console.print(Panel.fit(banner, title="[bold red]METASEED FRAMEWORK[/bold red]", border_style="red"))
    
    warning = Text("⚠️  USE APENAS PARA FINS EDUCACIONAIS E TESTES AUTORIZADOS! ⚠️", style="bold yellow")
    console.print(Panel.fit(warning, border_style="yellow"))
