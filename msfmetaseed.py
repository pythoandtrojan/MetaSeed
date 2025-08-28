#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import random
import readline
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from utils.animations import loading_animation, show_banner, show_version
from utils.helpers import clear_screen, print_status, print_error, print_success, print_info, get_input
from utils.autocomplete import setup_autocomplete
from utils.history import CommandHistory
from utils.themes import ThemeManager
from utils.logger import AdvancedLogger
from utils.macros import MacroSystem
from utils.notifier import Notifier
from utils.cache import ExploitCache
from config.settings import Config
from config.database import Database
from core.server import C2Server
from core.handler import MultiHandler
from core.payload_generator import PayloadGenerator
from core.exploit_manager import ExploitManager
from core.connection_manager import ConnectionManager
from core.profile_manager import ProfileManager
from modules.exploits.scanner import ScannerModule
from modules.post.camera import CameraModule
from modules.integration.cep_api import CEPAPI
from modules.integration.ip_api import IPAPI
from modules.integration.cnpj_api import CNPJAPI
from modules.integration.holehe import HoleheIntegration
from modules.integration.whois import WhoisIntegration

class MetaseedFramework:
    def __init__(self):
        # Carregar configurações
        self.config = Config()
        
        # Inicializar componentes de utilidade
        self.logger = AdvancedLogger()
        self.cache = ExploitCache()
        self.history = CommandHistory()
        self.theme_manager = ThemeManager()
        self.macro_system = MacroSystem()
        self.notifier = Notifier()
        
        # Inicializar banco de dados
        self.db = Database(self.config.get("DATABASE_PATH"))
        
        # Inicializar componentes principais
        self.server = C2Server(self.config, self.db)
        self.handler = MultiHandler(self.config)
        self.payload_generator = PayloadGenerator()
        self.exploit_manager = ExploitManager(self.config.get("DATABASE_PATH"))
        self.scanner = ScannerModule()
        self.camera = CameraModule(self.server)
        self.connection_manager = ConnectionManager()
        self.profile_manager = ProfileManager()
        
        # Inicializar integrações
        self.cep_api = CEPAPI(self.cache)
        self.ip_api = IPAPI(self.cache)
        self.cnpj_api = CNPJAPI(self.cache)
        self.holehe = HoleheIntegration(self.cache)
        self.whois = WhoisIntegration(self.cache)
        
        # Estado atual
        self.current_module = None
        self.current_session = None
        self.prompt = "metaseed"
        
        # Configurar autocomplete
        self.commands = [
            "help", "clear", "version", "update", "use", "show", "set", 
            "run", "exploit", "sessions", "handler", "search", "exit",
            "connection", "macro", "theme", "api", "listener", "connector"
        ]
        setup_autocomplete(self.commands)
        
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
                    
                # Registrar no histórico
                self.history.save_history()
                
                # Registrar no log
                self.logger.log_command(command, self.current_session)
                
                self.handle_command(command)
                
            except KeyboardInterrupt:
                print("\n")
                print_status("Use 'exit' para sair")
            except Exception as e:
                print_error(f"Erro: {e}")
                self.logger.log_error(f"Erro no comando: {e}")
                
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
            
        elif command == "show connections":
            self.connection_manager.list_connections()
            
        elif command == "show macros":
            self.macro_system.list_macros()
            
        elif command == "show themes":
            self.handle_show_themes()
            
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
            
        elif command.startswith("connection"):
            self.handle_connection_command(command)
            
        elif command.startswith("listener"):
            self.handle_listener_command(command)
            
        elif command.startswith("connector"):
            self.handle_connector_command(command)
            
        elif command.startswith("macro"):
            self.handle_macro_command(command)
            
        elif command.startswith("theme"):
            self.handle_theme_command(command)
            
        elif command.startswith("api"):
            self.handle_api_command(command)
            
        elif command == "exit":
            print_status("Saindo do Metaseed Framework...")
            self.connection_manager.close_all_connections()
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
  show connections     - Listar conexões ativas
  show macros          - Listar macros disponíveis
  show themes          - Listar temas disponíveis
  run / exploit        - Executar o módulo atual
  sessions             - Gerenciar sessões
  handler              - Gerenciar handlers
  connection           - Gerenciar conexões
  listener             - Gerenciar listeners
  connector            - Conectar a hosts remotos
  macro                - Gerenciar macros
  theme                - Gerenciar temas
  api                  - Consultas a APIs
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

APIs disponíveis:
  api cep [número]     - Consultar CEP
  api ip [endereço]    - Consultar IP
  api cnpj [número]    - Consultar CNPJ
  api email [email]    - Verificar email (Holehe)
  api whois [domínio]  - Consultar WHOIS

Exemplos:
  use payload/windows/meterpreter/reverse_tcp
  set LHOST 192.168.1.100
  set LPORT 4444
  set CONNECTION_MODE listener
  exploit
  listener start 0.0.0.0 4444
  connector start 192.168.1.50 4444
  sessions -l
  sessions -i 1
  api cep 12345678
  api ip 8.8.8.8
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
            print(f"  CONNECTION_MODE - {self.config.get('CONNECTION_MODE')}")
            
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
            
    def handle_show_themes(self):
        themes = self.theme_manager.list_themes()
        print("Temas disponíveis:")
        for theme in themes:
            print(f"  {theme}")
            
    def handle_set_command(self, command):
        parts = command.split()
        if len(parts) < 3:
            print_error("Uso: set [opção] [valor]")
            return
            
        option = parts[1].upper()
        value = " ".join(parts[2:])
        
        # Configurações globais
        if option in ["LHOST", "LPORT", "PROTOCOL", "ENCODING", "CONNECTION_MODE", "RHOST", "RPORT", "THEME"]:
            self.config.set(option, value)
            print_success(f"{option} => {value}")
            
            # Atualizar também nos componentes relevantes
            if option == "PROTOCOL":
                self.payload_generator.set_protocol(value)
            elif option == "ENCODING":
                self.payload_generator.set_encoding(value)
            elif option == "CONNECTION_MODE":
                self.connection_manager.set_mode(value)
            elif option == "THEME":
                if self.theme_manager.set_theme(value):
                    print_success(f"Tema alterado para: {value}")
                else:
                    print_error(f"Tema não encontrado: {value}")
                
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
            
    def handle_connection_command(self, command):
        parts = command.split()
        
        if len(parts) == 1:
            self.connection_manager.list_connections()
            
        elif len(parts) >= 2 and parts[1] == "send":
            if len(parts) < 4:
                print_error("Uso: connection send [id] [dados]")
                return
                
            conn_id = parts[2]
            data = " ".join(parts[3:])
            self.connection_manager.send_data(conn_id, data)
            
        elif len(parts) >= 2 and parts[1] == "close":
            if len(parts) < 3:
                print_error("Uso: connection close [id]")
                return
                
            conn_id = parts[2]
            self.connection_manager.close_connection(conn_id)
            
        elif len(parts) >= 2 and parts[1] == "closeall":
            self.connection_manager.close_all_connections()
            
        else:
            print_error("Uso: connection [list | send id data | close id | closeall]")
            
    def handle_listener_command(self, command):
        parts = command.split()
        
        if len(parts) >= 3 and parts[1] == "start":
            lhost = parts[2] if len(parts) > 2 else self.config.get("LHOST")
            lport = int(parts[3]) if len(parts) > 3 else self.config.get("LPORT")
            protocol = parts[4] if len(parts) > 4 else self.config.get("PROTOCOL")
            
            self.connection_manager.start_listener(lhost, lport, protocol)
            
        else:
            print_error("Uso: listener start [lhost] [lport] [protocol]")
            
    def handle_connector_command(self, command):
        parts = command.split()
        
        if len(parts) >= 3 and parts[1] == "start":
            rhost = parts[2]
            rport = int(parts[3]) if len(parts) > 3 else self.config.get("LPORT")
            protocol = parts[4] if len(parts) > 4 else self.config.get("PROTOCOL")
            
            self.connection_manager.start_connector(rhost, rport, protocol)
            
        else:
            print_error("Uso: connector start [rhost] [rport] [protocol]")
            
    def handle_macro_command(self, command):
        parts = command.split()
        
        if len(parts) == 1:
            self.macro_system.list_macros()
            
        elif len(parts) >= 3 and parts[1] == "create":
            macro_name = parts[2]
            macro_commands = input("Digite os comandos da macro (separados por ;): ").split(";")
            self.macro_system.create_macro(macro_name, macro_commands)
            
        elif len(parts) >= 2 and parts[1] == "execute":
            if len(parts) < 3:
                print_error("Uso: macro execute [nome]")
                return
                
            macro_name = parts[2]
            self.macro_system.execute_macro(macro_name, self)
            
        elif len(parts) >= 2 and parts[1] == "delete":
            if len(parts) < 3:
                print_error("Uso: macro delete [nome]")
                return
                
            macro_name = parts[2]
            self.macro_system.delete_macro(macro_name)
            
        else:
            print_error("Uso: macro [list | create name | execute name | delete name]")
            
    def handle_theme_command(self, command):
        parts = command.split()
        
        if len(parts) == 1:
            self.handle_show_themes()
            
        elif len(parts) >= 2 and parts[1] == "set":
            if len(parts) < 3:
                print_error("Uso: theme set [nome]")
                return
                
            theme_name = parts[2]
            if self.theme_manager.set_theme(theme_name):
                self.config.set("THEME", theme_name)
                print_success(f"Tema alterado para: {theme_name}")
            else:
                print_error(f"Tema não encontrado: {theme_name}")
                
        else:
            print_error("Uso: theme [list | set name]")
            
    def handle_api_command(self, command):
        parts = command.split()
        
        if len(parts) < 3:
            print_error("Uso: api [tipo] [consulta]")
            return
            
        api_type = parts[1].lower()
        query = " ".join(parts[2:])
        
        if api_type == "cep":
            self.cep_api.search_cep(query)
            
        elif api_type == "ip":
            if query == "meu" or query == "my":
                my_ip = self.ip_api.get_my_ip()
                if my_ip:
                    self.ip_api.search_ip(my_ip)
            else:
                self.ip_api.search_ip(query)
                
        elif api_type == "cnpj":
            self.cnpj_api.search_cnpj(query)
            
        elif api_type == "email":
            self.holehe.check_email(query)
            
        elif api_type == "whois":
            self.whois.domain_info(query)
            
        else:
            print_error(f"Tipo de API não suportado: {api_type}")
            
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
