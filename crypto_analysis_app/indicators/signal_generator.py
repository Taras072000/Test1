import pandas as pd
import numpy as np

def generate_signals(
    df: pd.DataFrame,
    indicators: dict,
    patterns: pd.DataFrame,
    volume_threshold: float = 0,
    ema_period: int = 20,
    adx_period: int = 14,
    atr_period: int = 14,
    atr_multiplier_sl: float = 1.5,
    atr_multiplier_tp: float = 3.0
) -> pd.DataFrame:
    """
    Генерирует сигналы входа/выхода с SL и TP.
    
    df: DataFrame с историей свечей (обязательные колонки: open, high, low, close, volume)
    indicators: словарь с ключами: 'ema', 'adx', 'atr' (серии с соответствующими значениями)
    patterns: DataFrame с распознанными свечными паттернами (например, из pattern_recognition.py)
    
    Возвращает DataFrame с колонками:
    - signal: 'buy', 'sell' или None
    - sl: уровень стоп-лосса
    - tp: уровень тейк-профита
    - reason: краткое описание причины сигнала
    """

    signals = pd.DataFrame(index=df.index)
    signals['signal'] = None
    signals['sl'] = np.nan
    signals['tp'] = np.nan
    signals['reason'] = None

    ema = indicators.get('ema')
    adx = indicators.get('adx')
    atr = indicators.get('atr')

    # Простая фильтрация по объему — входить только если объем больше threshold
    high_volume = df['volume'] > volume_threshold

    for i in range(1, len(df)):
        # Берем текущие значения индикаторов и паттернов
        price_close = df['close'].iloc[i]
        price_open = df['open'].iloc[i]
        price_low = df['low'].iloc[i]
        price_high = df['high'].iloc[i]

        current_ema = ema.iloc[i] if ema is not None else None
        current_adx = adx.iloc[i] if adx is not None else None
        current_atr = atr.iloc[i] if atr is not None else None

        current_patterns = patterns.iloc[i] if patterns is not None else None
        current_volume = df['volume'].iloc[i]

        # Фильтрация по тренду: EMA как фильтр направления
        trend_up = current_ema is not None and price_close > current_ema
        trend_down = current_ema is not None and price_close < current_ema

        # ADX для силы тренда
        strong_trend = current_adx is not None and current_adx > 25

        # Проверка свечных паттернов
        bullish_pattern = current_patterns is not None and any(
            str(current_patterns[col]).lower().find('bull') != -1 for col in current_patterns.index
        )
        bearish_pattern = current_patterns is not None and any(
            str(current_patterns[col]).lower().find('bear') != -1 for col in current_patterns.index
        )

        # Объем
        volume_ok = current_volume > volume_threshold

        # Сигналы на покупку
        if (trend_up and strong_trend and bullish_pattern and volume_ok):
            signals.at[df.index[i], 'signal'] = 'buy'
            signals.at[df.index[i], 'reason'] = 'Uptrend + bullish pattern + volume'

            # SL ниже минимальной точки свечи минус ATR * multiplier
            signals.at[df.index[i], 'sl'] = price_low - atr_multiplier_sl * current_atr if current_atr else price_low * 0.99
            # TP на уровне с запасом ATR вверх
            signals.at[df.index[i], 'tp'] = price_close + atr_multiplier_tp * current_atr if current_atr else price_close * 1.02

        # Сигналы на продажу
        elif (trend_down and strong_trend and bearish_pattern and volume_ok):
            signals.at[df.index[i], 'signal'] = 'sell'
            signals.at[df.index[i], 'reason'] = 'Downtrend + bearish pattern + volume'

            # SL выше максимальной точки свечи плюс ATR * multiplier
            signals.at[df.index[i], 'sl'] = price_high + atr_multiplier_sl * current_atr if current_atr else price_high * 1.01
            # TP ниже цены с запасом ATR вниз
            signals.at[df.index[i], 'tp'] = price_close - atr_multiplier_tp * current_atr if current_atr else price_close * 0.98

        else:
            signals.at[df.index[i], 'signal'] = None
            signals.at[df.index[i], 'sl'] = np.nan
            signals.at[df.index[i], 'tp'] = np.nan
            signals.at[df.index[i], 'reason'] = None

    return signals