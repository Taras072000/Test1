import pandas as pd

def detect_pinbar(df: pd.DataFrame) -> pd.Series:
    """
    Распознает PinBar (Bullish и Bearish).
    Возвращает серию с метками 'pinbar_bull', 'pinbar_bear' или None.
    """
    patterns = pd.Series(index=df.index, dtype='object')

    body = abs(df['close'] - df['open'])
    lower_shadow = df[['open', 'close']].min(axis=1) - df['low']
    upper_shadow = df['high'] - df[['open', 'close']].max(axis=1)

    # Bullish PinBar: длинный нижний хвост, маленькое тело сверху, верхняя тень маленькая
    bull_condition = (lower_shadow > 2 * body) & (upper_shadow < body)

    # Bearish PinBar: длинный верхний хвост, маленькое тело снизу, нижняя тень маленькая
    bear_condition = (upper_shadow > 2 * body) & (lower_shadow < body)

    patterns[bull_condition] = 'pinbar_bull'
    patterns[bear_condition] = 'pinbar_bear'

    return patterns

def detect_engulfing(df: pd.DataFrame) -> pd.Series:
    """
    Распознает Bullish и Bearish Engulfing.
    Возвращает серию с метками 'engulfing_bull', 'engulfing_bear' или None.
    """
    patterns = pd.Series(index=df.index, dtype='object')

    prev_open = df['open'].shift(1)
    prev_close = df['close'].shift(1)

    current_open = df['open']
    current_close = df['close']

    prev_body = abs(prev_close - prev_open)
    curr_body = abs(current_close - current_open)

    # Bullish Engulfing: текущая свеча полностью поглощает тело предыдущей и закрытие выше открытия
    bull_condition = (
        (current_open < prev_close) &
        (current_close > prev_open) &
        (curr_body > prev_body) &
        (current_close > current_open)
    )

    # Bearish Engulfing: текущая свеча полностью поглощает тело предыдущей и закрытие ниже открытия
    bear_condition = (
        (current_open > prev_close) &
        (current_close < prev_open) &
        (curr_body > prev_body) &
        (current_close < current_open)
    )

    patterns[bull_condition] = 'engulfing_bull'
    patterns[bear_condition] = 'engulfing_bear'

    return patterns

def detect_harami(df: pd.DataFrame) -> pd.Series:
    """
    Распознает паттерн Harami (Bullish и Bearish).
    """
    patterns = pd.Series(index=df.index, dtype='object')

    prev_open = df['open'].shift(1)
    prev_close = df['close'].shift(1)
    current_open = df['open']
    current_close = df['close']

    prev_body_high = max(prev_open, prev_close)
    prev_body_low = min(prev_open, prev_close)
    curr_body_high = max(current_open, current_close)
    curr_body_low = min(current_open, current_close)

    # Bullish Harami: тело текущей свечи полностью внутри тела предыдущей и закрытие выше открытия
    bull_condition = (
        (curr_body_high < prev_body_high) &
        (curr_body_low > prev_body_low) &
        (current_close > current_open)
    )

    # Bearish Harami: тело текущей свечи внутри тела предыдущей и закрытие ниже открытия
    bear_condition = (
        (curr_body_high < prev_body_high) &
        (curr_body_low > prev_body_low) &
        (current_close < current_open)
    )

    patterns[bull_condition] = 'harami_bull'
    patterns[bear_condition] = 'harami_bear'

    return patterns

def detect_all_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Детектор всех паттернов. Возвращает DataFrame с отдельным столбцом на каждый паттерн.
    """
    patterns = pd.DataFrame(index=df.index)
    patterns['pinbar'] = detect_pinbar(df)
    patterns['engulfing'] = detect_engulfing(df)
    patterns['harami'] = detect_harami(df)
    return patterns