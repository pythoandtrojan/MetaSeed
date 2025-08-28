import socket
import subprocess
import sys
from utils.helpers import print_status, print_success, print_error

class Scanner:
    def __init__(self):
        self.current_module = None
        self.modules = {
            "scanner": self.run_scanner,
            "hydra": self.run_hydra,
            "nmap": self.run_nmap
        }
        
    def select_module(self, module):
        if module in self.modules:
            self.current_module = module
            print_success(f"Módulo selecionado: {module}")
        else:
            print_error(f"Módulo não encontrado: {module}")
            
    def list_exploits(self):
        print("Exploits e scanners disponíveis:")
        print("  scanner - Scanner de rede básico")
        print("  hydra   - Ferramenta de brute force (requer hydra instalado)")
        print("  nmap    - Scanner de portas avançado (requer nmap instalado)")
        
    def run(self, target, **kwargs):
        if not self.current_module:
            print_error("Nenhum módulo selecionado")
            return False
            
        module_func = self.modules[self.current_module]
        return module_func(target, **kwargs)
        
    def run_scanner(self, target, ports="1-1000"):
        print_status(f"Escaneando {target} nas portas {ports}...")
        
        try:
            if "-" in ports:
                start_port, end_port = map(int, ports.split("-"))
                port_list = range(start_port, end_port + 1)
            else:
                port_list = [int(p) for p in ports.split(",")]
                
            open_ports = []
            
            for port in port_list:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.5)
                        result = s.connect_ex((target, port))
                        if result == 0:
                            open_ports.append(port)
                            print_success(f"Porta {port} aberta")
                except:
                    continue
                    
            if open_ports:
                print_success(f"Portas abertas em {target}: {', '.join(map(str, open_ports))}")
            else:
                print_error(f"Nenhuma porta aberta encontrada em {target}")
                
            return open_ports
            
        except Exception as e:
            print_error(f"Erro no scanner: {e}")
            return []
            
    def run_hydra(self, target, service="ssh", user_list="root,admin", password_list="password,123456"):
        print_status(f"Executando Hydra contra {target}...")
        
        try:
            # Verificar se o hydra está instalado
            result = subprocess.run(["which", "hydra"], capture_output=True, text=True)
            if not result.stdout.strip():
                print_error("Hydra não está instalado. Instale com: sudo apt install hydra")
                return False
                
            # Construir comando hydra
            users = user_list.split(",")
            passwords = password_list.split(",")
            
            # Para demonstração, apenas simular
            print_status("Simulando ataque Hydra (para uso real, instale o hydra)")
            print_status(f"Alvo: {target}")
            print_status(f"Serviço: {service}")
            print_status(f"Usuários: {user_list}")
            print_status(f"Senhas: {password_list}")
            
            # Em uma implementação real, você executaria:
            # subprocess.run(["hydra", "-L", user_file, "-P", password_file, f"{target} {service}"])
            
            return True
            
        except Exception as e:
            print_error(f"Erro ao executar Hydra: {e}")
            return False
            
    def run_nmap(self, target, options="-sS -sV -O"):
        print_status(f"Executando Nmap contra {target}...")
        
        try:
            # Verificar se o nmap está instalado
            result = subprocess.run(["which", "nmap"], capture_output=True, text=True)
            if not result.stdout.strip():
                print_error("Nmap não está instalado. Instale com: sudo apt install nmap")
                return False
                
            # Executar nmap
            cmd = ["nmap"] + options.split() + [target]
            print_status(f"Executando: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            
            if result.stderr:
                print_error(result.stderr)
                
            return True
            
        except Exception as e:
            print_error(f"Erro ao executar Nmap: {e}")
            return False
