from indicators.signal_generator import generate_signals
from indicators.ta_engine import calculate_ema, calculate_adx, calculate_atr
from indicators.pattern_recognition import detect_all_patterns  # <-- импорт прямо функции

import pandas as pd

class AnalysisEngine:
    def __init__(self, tv):
        self.tv = tv

    def run_analysis(self, pair: str):
        # Получаем данные
        df = self.tv.get_price_data(pair)

        if df is None or df.empty:
            return []

        # Считаем индикаторы
        ema = calculate_ema(df['close'], period=20)
        adx = calculate_adx(df['high'], df['low'], df['close'], period=14)
        atr = calculate_atr(df, period=14)
        indicators = {'ema': ema, 'adx': adx, 'atr': atr}

        # Распознаём паттерны
        try:
            patterns = detect_all_patterns(df)
        except Exception:
            # Если вдруг recognize_patterns отсутствует — создаём пустую таблицу
            patterns = pd.DataFrame(index=df.index)

        # Генерируем сигналы
        signal_df = generate_signals(df, indicators, patterns)

        # Преобразуем сигналы в список словарей
        result = []
        for i in signal_df.index:
            signal = signal_df.loc[i]
            if signal['signal']:
                result.append({
                    'type': signal['signal'],
                    'message': f"{signal['signal'].upper()} @ {df['close'].loc[i]:.2f} | SL: {signal['sl']:.2f}, TP: {signal['tp']:.2f}"
                })

        return result