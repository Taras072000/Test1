import asyncio
from typing import Callable, Coroutine

class Scheduler:
    def __init__(self, interval_sec: int, task: Callable[[], Coroutine]):
        """
        :param interval_sec: интервал в секундах между запусками задачи
        :param task: асинхронная функция без параметров, которая будет вызываться циклично
        """
        self.interval_sec = interval_sec
        self.task = task
        self._running = False
        self._task_handle = None

    async def _runner(self):
        while self._running:
            try:
                await self.task()
            except Exception as e:
                print(f"Ошибка в Scheduled task: {e}")
            await asyncio.sleep(self.interval_sec)

    def start(self):
        if not self._running:
            self._running = True
            self._task_handle = asyncio.create_task(self._runner())

    def stop(self):
        self._running = False
        if self._task_handle:
            self._task_handle.cancel()
            self._task_handle = None

# Пример использования:
# async def update_data():
#     print("Обновляю данные...")
#     # тут логика обновления
#
# scheduler = Scheduler(interval_sec=60, task=update_data)
# scheduler.start()
#
# # В вашем asyncio event loop не забудьте await asyncio.sleep(...) или run_forever()