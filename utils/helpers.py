import os
from rich.console import Console

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_status(message):
    console.print(f"[blue][*][/blue] {message}")

def print_success(message):
    console.print(f"[green][+][/green] {message}")

def print_error(message):
    console.print(f"[red][-][/red] {message}")

def print_warning(message):
    console.print(f"[yellow][!][/yellow] {message}")
