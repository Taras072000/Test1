import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

def calculate_support_resistance(
    df: pd.DataFrame,
    order: int = 5
) -> dict:
    """
    Вычисляет уровни поддержки и сопротивления на основе локальных минимумов и максимумов.

    df: DataFrame с колонками ['high', 'low', 'close']
    order: количество свечей с каждой стороны для поиска локальных экстремумов

    Возвращает словарь с ключами:
    - 'support': список уровней поддержки (локальные минимумы)
    - 'resistance': список уровней сопротивления (локальные максимумы)
    """

    # Найдем локальные максимумы (сопротивления)
    resistance_idx = argrelextrema(df['high'].values, np.greater, order=order)[0]
    resistance_levels = df['high'].iloc[resistance_idx].values

    # Найдем локальные минимумы (поддержки)
    support_idx = argrelextrema(df['low'].values, np.less, order=order)[0]
    support_levels = df['low'].iloc[support_idx].values

    # Сгруппируем близкие уровни (чтобы убрать шум)
    def merge_levels(levels, threshold=0.01):
        levels = np.sort(levels)
        merged = []
        prev = None
        for lvl in levels:
            if prev is None:
                prev = lvl
            elif abs(lvl - prev)/prev < threshold:
                # среднее между уровнями, сглаживание
                prev = (prev + lvl) / 2
            else:
                merged.append(prev)
                prev = lvl
        if prev is not None:
            merged.append(prev)
        return merged

    support = merge_levels(support_levels)
    resistance = merge_levels(resistance_levels)

    return {
        'support': support,
        'resistance': resistance
    }