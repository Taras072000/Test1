import requests

class TelegramAlert:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, text: str) -> bool:
        """Отправить сообщение в Telegram. Возвращает True если успешно."""
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        try:
            response = requests.post(self.api_url, data=payload, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Ошибка отправки Telegram сообщения: {e}")
            return False

# Пример использования:
# alert = TelegramAlert(bot_token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")
# alert.send_message("Тестовое уведомление")