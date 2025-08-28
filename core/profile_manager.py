#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from pathlib import Path

class ProfileManager:
    def __init__(self, profiles_dir=None):
        """
        Gerenciador de perfis de configuração do framework
        """
        if profiles_dir is None:
            self.profiles_dir = Path(__file__).parent.parent / "profiles"
        else:
            self.profiles_dir = Path(profiles_dir)
            
        # Criar diretório de perfis se não existir
        self.profiles_dir.mkdir(exist_ok=True)
        
        self.current_profile = "default"
        self.profiles = self.load_profiles()
        
    def load_profiles(self):
        """Carregar todos os perfis do diretório"""
        profiles = {}
        
        for profile_file in self.profiles_dir.glob("*.json"):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                    profile_name = profile_file.stem
                    profiles[profile_name] = profile_data
            except (json.JSONDecodeError, IOError) as e:
                print(f"Erro ao carregar perfil {profile_file}: {e}")
                
        return profiles
        
    def create_profile(self, profile_name, config_data):
        """Criar um novo perfil"""
        profile_path = self.profiles_dir / f"{profile_name}.json"
        
        try:
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
                
            self.profiles[profile_name] = config_data
            return True
        except IOError as e:
            print(f"Erro ao criar perfil {profile_name}: {e}")
            return False
            
    def delete_profile(self, profile_name):
        """Excluir um perfil"""
        if profile_name == "default":
            print("Não é possível excluir o perfil padrão")
            return False
            
        profile_path = self.profiles_dir / f"{profile_name}.json"
        
        if profile_path.exists():
            try:
                profile_path.unlink()
                if profile_name in self.profiles:
                    del self.profiles[profile_name]
                return True
            except IOError as e:
                print(f"Erro ao excluir perfil {profile_name}: {e}")
                return False
        else:
            print(f"Perfil {profile_name} não encontrado")
            return False
            
    def load_profile(self, profile_name):
        """Carregar um perfil específico"""
        if profile_name in self.profiles:
            self.current_profile = profile_name
            return self.profiles[profile_name]
        else:
            print(f"Perfil {profile_name} não encontrado")
            return None
            
    def get_profile(self, profile_name=None):
        """Obter dados de um perfil"""
        if profile_name is None:
            profile_name = self.current_profile
            
        return self.profiles.get(profile_name, {})
        
    def update_profile(self, profile_name, config_data):
        """Atualizar um perfil existente"""
        if profile_name not in self.profiles:
            print(f"Perfil {profile_name} não encontrado")
            return False
            
        return self.create_profile(profile_name, config_data)
        
    def list_profiles(self):
        """Listar todos os perfis disponíveis"""
        return list(self.profiles.keys())
        
    def export_profile(self, profile_name, export_path):
        """Exportar perfil para um arquivo"""
        if profile_name not in self.profiles:
            print(f"Perfil {profile_name} não encontrado")
            return False
            
        export_path = Path(export_path)
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.profiles[profile_name], f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Erro ao exportar perfil: {e}")
            return False
            
    def import_profile(self, import_path, profile_name=None):
        """Importar perfil de um arquivo"""
        import_path = Path(import_path)
        
        if not import_path.exists():
            print(f"Arquivo {import_path} não encontrado")
            return False
            
        if profile_name is None:
            profile_name = import_path.stem
            
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            return self.create_profile(profile_name, config_data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao importar perfil: {e}")
            return False

# Exemplo de uso
if __name__ == "__main__":
    # Teste básico do gerenciador de perfis
    pm = ProfileManager()
    
    # Criar um perfil de exemplo
    example_config = {
        "LHOST": "192.168.1.100",
        "LPORT": 4444,
        "PROTOCOL": "tcp",
        "ENCODING": "base64",
        "AUTO_START": True,
        "THEME": "dark"
    }
    
    if pm.create_profile("test_profile", example_config):
        print("Perfil criado com sucesso!")
        
    print("Perfis disponíveis:", pm.list_profiles())
    
    # Carregar perfil
    config = pm.get_profile("test_profile")
    print("Configuração do perfil:", config)
