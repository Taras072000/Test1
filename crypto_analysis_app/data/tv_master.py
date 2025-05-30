from tvDatafeed import TvDatafeed, Interval
import logging
import pandas as pd

class TvDataFeedMaster:
    def __init__(self, username=None, password=None):
        """
        Инициализация TvDatafeed.
        username, password — для авторизации, если нужно (можно None для nologin).
        """
        try:
            if username and password:
                self.tv = TvDatafeed(username, password)
            else:
                # Без авторизации — ограниченный доступ
                self.tv = TvDatafeed()
            logging.info("TvDatafeed успешно инициализирован.")
        except Exception as e:
            logging.error(f"Ошибка инициализации TvDatafeed: {e}")
            self.tv = None

    def get_data(self, symbol: str, exchange: str = 'FX_IDC', interval=Interval.in_1_minute, n_bars=500) -> pd.DataFrame:
        """
        Загрузка исторических данных по инструменту.
        
        :param symbol: тикер валютной пары, например 'EURUSD'
        :param exchange: биржа, например 'FX_IDC' для Forex
        :param interval: таймфрейм из Interval
        :param n_bars: количество баров для загрузки
        :return: pd.DataFrame с историческими данными OHLCV
        """
        if self.tv is None:
            logging.error("TvDatafeed не инициализирован.")
            return pd.DataFrame()

        try:
            data = self.tv.get_hist(symbol, exchange, interval, n_bars)
            logging.info(f"Данные получены: {symbol} {interval} ({len(data)} баров)")
            return data
        except Exception as e:
            logging.error(f"Ошибка при загрузке данных {symbol}: {e}")
            return pd.DataFrame()