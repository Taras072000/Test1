# config.py

# Telegram Bot настройки
TELEGRAM_TOKEN = '7887367082:AAH2tycjDRRulFKAdq0357xuZQ44rb-KrdA'
TELEGRAM_CHAT_ID = '7887367082'

# Таймфреймы для анализа
TIMEFRAMES = {
    '15s': '15S',
    '30s': '30S',
    '1m': '1Min',
    '5m': '5Min',
    '15m': '15Min',
    '1h': '1H',
    '4h': '4H',
    '1d': '1D',
}

# Настройки обновления данных (в секундах)
UPDATE_INTERVAL = 60  # проверка данных каждую минуту

# Другие параметры, например, параметры стратегии
STRATEGY_SETTINGS = {
    'ema_period': 20,
    'adx_period': 14,
    'atr_period': 14,
    'stop_loss_multiplier': 1.5,
    'take_profit_multiplier': 3.0,
}

# Пути к ресурсам
ASSETS_PATH = 'assets/'

# Логи (опционально)
LOG_FILE = 'logs/app.log'

class Settings:
    def __init__(self):
        from config import (
            TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TIMEFRAMES,
            UPDATE_INTERVAL, STRATEGY_SETTINGS, ASSETS_PATH, LOG_FILE
        )

        self.telegram_token = TELEGRAM_TOKEN
        self.telegram_chat_id = TELEGRAM_CHAT_ID
        self.timeframes = TIMEFRAMES
        self.update_interval = UPDATE_INTERVAL
        self.strategy_settings = STRATEGY_SETTINGS
        self.assets_path = ASSETS_PATH
        self.log_file = LOG_FILE