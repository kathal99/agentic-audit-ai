import requests
from config import DISCORD_WEBHOOK_URL, SLACK_WEBHOOK_URL

class AlertDispatcher:
    @staticmethod
    def send_discord(message: str) -> None:
        if not DISCORD_WEBHOOK_URL:
            return
        payload = {"content": message}
        try:
            requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        except requests.RequestException:
            pass

    @staticmethod
    def send_slack(message: str) -> None:
        if not SLACK_WEBHOOK_URL:
            return
        payload = {"text": message}
        try:
            requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        except requests.RequestException:
            pass

    @staticmethod
    def notify(message: str) -> None:
        AlertDispatcher.send_discord(message)
        AlertDispatcher.send_slack(message)
