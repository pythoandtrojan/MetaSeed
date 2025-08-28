import requests
import subprocess
import sys
from utils.helpers import print_success, print_error, print_status

def check_updates(current_version):
    """Verifica se há atualizações disponíveis"""
    try:
        # URL do repositório (exemplo)
        repo_url = "https://api.github.com/repos/seu-usuario/metaseed/releases/latest"
        
        response = requests.get(repo_url, timeout=5)
        if response.status_code == 200:
            latest_version = response.json()['tag_name']
            
            if latest_version > current_version:
                return True
                
        return False
    except:
        return False
        
def update_framework():
    """Atualiza o framework"""
    print_status("Verificando atualizações...")
    
    try:
        # Comando para atualizar (exemplo com git)
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Framework atualizado com sucesso!")
            print_status("Reiniciando...")
            return True
        else:
            print_error("Erro ao atualizar o framework")
            print_error(result.stderr)
            return False
    except Exception as e:
        print_error(f"Erro durante a atualização: {e}")
        return False
