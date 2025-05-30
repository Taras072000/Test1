import pandas as pd
import numpy as np

def calculate_ema(df: pd.DataFrame, period: int, price_col='close') -> pd.Series:
    """
    Вычисляет экспоненциальную скользящую среднюю (EMA).
    """
    return df[price_col].ewm(span=period, adjust=False).mean()

def calculate_adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Вычисляет Average Directional Index (ADX) для оценки силы тренда.
    """
    high = df['high']
    low = df['low']
    close = df['close']

    plus_dm = high.diff()
    minus_dm = low.diff().abs()

    plus_dm = np.where((plus_dm > minus_dm) & (plus_dm > 0), plus_dm, 0)
    minus_dm = np.where((minus_dm > plus_dm) & (minus_dm > 0), minus_dm, 0)

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(window=period).mean()

    plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).sum() / atr)
    minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).sum() / atr)
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(window=period).mean()

    return adx

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Вычисляет Average True Range (ATR) — меру волатильности.
    """
    high = df['high']
    low = df['low']
    close = df['close']

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()

    return atr

def detect_candlestick_patterns(df: pd.DataFrame) -> pd.Series:
    """
    Пример детекции паттернов PinBar и Engulfing.
    Возвращает серию с метками паттернов:
    'pinbar_bull', 'pinbar_bear', 'engulfing_bull', 'engulfing_bear' или None.
    """

    patterns = pd.Series(index=df.index, dtype='object')

    # PinBar Bullish: длинный нижний хвост и маленькое тело сверху
    body = abs(df['close'] - df['open'])
    candle_range = df['high'] - df['low']
    lower_shadow = df['open'].where(df['close'] > df['open'], df['close']) - df['low']
    upper_shadow = df['high'] - df['close'].where(df['close'] > df['open'], df['open'])

    # Пример условий для PinBar Bull
    is_pinbar_bull = (lower_shadow > body * 2) & (upper_shadow < body)
    patterns[is_pinbar_bull] = 'pinbar_bull'

    # PinBar Bearish
    is_pinbar_bear = (upper_shadow > body * 2) & (lower_shadow < body)
    patterns[is_pinbar_bear] = 'pinbar_bear'

    # Engulfing Bullish: тело свечи полностью поглощает тело предыдущей и закрытие выше открытия
    engulfing_bull = (df['open'] < df['close'].shift()) & (df['close'] > df['open'].shift()) & (body > body.shift())
    patterns[engulfing_bull] = 'engulfing_bull'

    # Engulfing Bearish: противоположный случай
    engulfing_bear = (df['open'] > df['close'].shift()) & (df['close'] < df['open'].shift()) & (body > body.shift())
    patterns[engulfing_bear] = 'engulfing_bear'

    return patterns

def check_volume_spike(df: pd.DataFrame, volume_col='volume', multiplier=1.5) -> pd.Series:
    """
    Определяет всплески объема — когда текущий объем превышает средний за период * multiplier.
    """
    avg_volume = df[volume_col].rolling(window=20).mean()
    spikes = df[volume_col] > (avg_volume * multiplier)
    return spikes

def detect_levels(df: pd.DataFrame, window=20, tolerance=0.005) -> dict:
    """
    Простейшая детекция уровней поддержки и сопротивления.
    Возвращает словарь с уровнями 'support' и 'resistance'.
    tolerance — относительная погрешность для сглаживания уровней.
    """
    support_levels = []
    resistance_levels = []

    lows = df['low']
    highs = df['high']

    for i in range(window, len(df) - window):
        low_slice = lows[i-window:i+window]
        high_slice = highs[i-window:i+window]
        current_low = lows[i]
        current_high = highs[i]

        if current_low == low_slice.min():
            support_levels.append(current_low)
        if current_high == high_slice.max():
            resistance_levels.append(current_high)

    # Фильтруем близкие уровни
    def filter_levels(levels):
        filtered = []
        for level in levels:
            if not any(abs(level - f) / level < tolerance for f in filtered):
                filtered.append(level)
        return filtered

    return {
        "support": filter_levels(support_levels),
        "resistance": filter_levels(resistance_levels),
    }