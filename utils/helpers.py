import os
import sys
from rich.console import Console
from rich.theme import Theme

# Tema personalizado para cores
custom_theme = Theme({
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "status": "cyan",
    "prompt": "magenta"
})

console = Console(theme=custom_theme)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_status(message):
    console.print(f"[status][*][/status] {message}")

def print_success(message):
    console.print(f"[success][+][/success] {message}")

def print_error(message):
    console.print(f"[error][-][/error] {message}")

def print_warning(message):
    console.print(f"[warning][!][/warning] {message}")

def print_info(message):
    console.print(f"[info][i][/info] {message}")

def print_prompt(message):
    console.print(f"[prompt][>][/prompt] {message}")

def get_input(prompt):
    return console.input(f"[prompt][>][/prompt] {prompt}")

def confirm_action(message):
    response = get_input(f"{message} (y/N): ")
    return response.lower() in ['y', 'yes']
