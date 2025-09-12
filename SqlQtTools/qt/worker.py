import abc
from SqlQtTools.qt.compat import QObject, Signal, Slot, QThread


class Worker(QObject):
    """
    Класс для выполнения длительной операции в отдельном потоке.
    """
    progress = Signal(int)  # Сигнал для обновления прогресса (0-100)
    message = Signal(str)  # Сигнал для текстовых сообщений
    finished = Signal()  # Сигнал о завершении работы
    error = Signal(str)  # Сигнал об ошибке

    def __init__(self, task, *args, **kwargs):
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self._is_running = True

    @Slot()
    def run(self):
        """Основной метод, выполняющийся в отдельном потоке."""
        try:
            # Проверяем, является ли task классом или функцией
            if isinstance(self.task, type):
                # Если это класс, создаем экземпляр и вызываем run
                instance = self.task(
                    *self.args,
                    progress_callback=self.progress.emit,
                    message_callback=self.message.emit,
                    is_running=lambda: self._is_running,
                    **self.kwargs
                )
                instance.run()
            else:
                # Если это функция, вызываем напрямую
                self.task(
                    *self.args,
                    progress_callback=self.progress.emit,
                    message_callback=self.message.emit,
                    is_running=lambda: self._is_running,
                    **self.kwargs
                )
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        """Запрос на остановку выполнения задачи."""
        self._is_running = False


class ThreadManager(QObject):
    """
    Менеджер для запуска и управления фоновыми потоками.
    """

    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

    def start_task(self, task_func, *args, **kwargs):
        """Запуск задачи в отдельном потоке."""
        # Останавливаем предыдущий поток, если он есть
        self.stop_task()

        # Создаем новый поток и воркер
        self.thread = QThread()
        self.worker = Worker(task_func, *args, **kwargs)

        # Перемещаем воркер в поток
        self.worker.moveToThread(self.thread)

        # Подключаем сигналы
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.error.connect(self.handle_error)

        # Запускаем поток
        self.thread.start()

        return self.worker

    def stop_task(self):
        """Остановка текущей задачи."""
        try:
            if self.worker is not None:
                self.worker.stop()
            if self.thread is not None:
                self.thread.quit()
                self.thread.wait()
        except:
            pass
        finally:
            self.thread = None
            self.worker = None

    def handle_error(self, error_msg):
        """Обработка ошибок в потоке."""
        print(f"Ошибка в фоновом потоке: {error_msg}")
        self.stop_task()


class BaseTask:
    """
    Базовый класса, который будет выполняться в отдельном потоке.
    Должен содержать метод run().
    """

    def __init__(self, *args, progress_callback=None, message_callback=None, is_running=None, **kwargs):
        self.progress_callback = progress_callback
        self.message_callback = message_callback
        self._is_running = is_running if is_running is not None else lambda: True

    @abc.abstractmethod
    def run(self):
        """Основной метод, который будет выполняться в потоке."""
        pass

    def _progress(self, value):
        if self.progress_callback:
            self.progress_callback(value)

    def _message(self, value):
        if self.message_callback:
            self.message_callback(value)
