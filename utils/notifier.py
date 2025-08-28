import requests
from rich.console import Console

console = Console()

class Notifier:
    def __init__(self):
        self.webhook_url = None
        self.notification_types = {
            "new_session": True,
            "command_executed": False,
            "important_event": True,
            "scan_completed": True
        }
        
    def set_webhook(self, webhook_url):
        self.webhook_url = webhook_url
        console.print(f"[green]✓ Webhook definido: {webhook_url}[/green]")
        
    def send_notification(self, title, message, level="info"):
        if level == "success":
            emoji = "✅"
            color = "#00ff00"
        elif level == "error":
            emoji = "❌"
            color = "#ff0000"
        elif level == "warning":
            emoji = "⚠️"
            color = "#ffff00"
        else:
            emoji = "ℹ️"
            color = "#0000ff"
            
        # Integração com Discord
        if self.webhook_url and "discord" in self.webhook_url:
            self._send_discord_webhook(f"{emoji} {title}", message, color)
            
        console.print(f"[blue][NOTIFICAÇÃO] {title}: {message}[/blue]")
            
    def _send_discord_webhook(self, title, message, color):
        try:
            payload = {
                "embeds": [{
                    "title": title,
                    "description": message,
                    "color": int(color[1:], 16)
                }]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            if response.status_code != 204:
                console.print(f"[yellow]⚠️  Erro ao enviar notificação: {response.status_code}[/yellow]")
                
        except Exception as e:
            console.print(f"[yellow]⚠️  Erro ao enviar notificação: {e}[/yellow]")
