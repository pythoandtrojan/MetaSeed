# Módulo de payloads para diferentes plataformas
from .windows import WindowsPayloads
from .linux import LinuxPayloads
from .android import AndroidPayloads
from .multi import MultiPayloads

class PayloadModule:
    def __init__(self):
        self.windows = WindowsPayloads()
        self.linux = LinuxPayloads()
        self.android = AndroidPayloads()
        self.multi = MultiPayloads()
        
    def list_payloads(self, platform=None):
        if platform == "windows" or platform is None:
            print("Windows Payloads:")
            for payload in self.windows.get_payloads():
                print(f"  {payload}")
                
        if platform == "linux" or platform is None:
            print("Linux Payloads:")
            for payload in self.linux.get_payloads():
                print(f"  {payload}")
                
        if platform == "android" or platform is None:
            print("Android Payloads:")
            for payload in self.android.get_payloads():
                print(f"  {payload}")
                
        if platform == "multi" or platform is None:
            print("Multi Payloads:")
            for payload in self.multi.get_payloads():
                print(f"  {payload}")
