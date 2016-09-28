from abc import ABCMeta, abstractmethod
from threading import Thread


class Handler(metaclass=ABCMeta):
    def __init__(self):
        self.__start = False

        def target():
            while self.__start: self.handle()

        self._thread = Thread(target=target)

    def start(self):
        self._start()
        self.__start = True
        self._thread.start()

    def stop(self):
        self._stop()
        self.__start = False

    @abstractmethod
    def _start(self): pass

    @abstractmethod
    def _stop(self): pass

    @abstractmethod
    def handle(self): pass
