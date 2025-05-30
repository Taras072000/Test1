from enum import Enum

class Interval(Enum):
    IN_15_SEC = '15s'
    IN_30_SEC = '30s'
    IN_1_MIN = '1m'
    IN_5_MIN = '5m'
    IN_15_MIN = '15m'
    IN_30_MIN = '30m'
    IN_1_HOUR = '1h'
    IN_4_HOUR = '4h'
    IN_1_DAY = '1d'

# Настройки используемых таймфреймов
# Можно расширять или менять здесь
DEFAULT_TIMEFRAMES = [
    Interval.IN_1_MIN,
    Interval.IN_5_MIN,
    Interval.IN_15_MIN,
    Interval.IN_1_HOUR,
]

# Функции для преобразования Enum в строку или обратно
def interval_to_str(interval: Interval) -> str:
    return interval.value

def str_to_interval(s: str) -> Interval | None:
    for interval in Interval:
        if interval.value == s:
            return interval
    return None