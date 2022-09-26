from typing import Callable, Dict, List, Any
from toby.value import Value
from threading import Thread
from time import time

_SECONDS_PER_MINUTE = 60


class Clock:
    """ """

    def __init__(self, beats_per_minute):
        self._delete = False
        self._beats_per_minute: Value = Value(1, 500)
        self._seconds_per_tic: Value = Value(1, 100)
        self._index = 0
        self._beat_callback = []
        self._tic_callback = []
        self.tics_per_beat = 4

        self.beats_per_minute = beats_per_minute

        # call main thread
        self._thread = Thread(target=self._func, args=())
        self._thread.start()

    def add_beat_callback(self, callback: Callable):
        self._beat_callback.append(callback)

    def add_tic_callback(self, callback: Callable):
        self._tic_callback.append(callback)

    @property
    def beats_per_second(self):
        return self.beats_per_minute / _SECONDS_PER_MINUTE

    @property
    def seconds_between_beats(self):
        return 1 / self.beats_per_second

    @property
    def seconds_betweeen_tics(self):
        return self.seconds_between_beats / self.tics_per_beat

    @property
    def beats_per_minute(self):
        return self._beats_per_minute.value

    @beats_per_minute.setter
    def beats_per_minute(self, value):
        self._beats_per_minute.value = value

    def __del__(self):
        # print("killing clock")
        self._delete = True

    def _tic(self):
        self._index += 1
        for callback in self._tic_callback:
            callback()

        if self._index == self.tics_per_beat:
            self._index = 0
            for callback in self._beat_callback:
                callback()

    def _func(self):
        start_time_seconds = time()
        while not self._delete:
            # print(self.seconds_betweeen_tics)
            next_tic = start_time_seconds + self.seconds_betweeen_tics

            while time() < next_tic:
                pass

            start_time_seconds = next_tic
            self._tic()
