import logging


class ValueException(Exception):
    """ExceptionClass"""


class WholeValue:
    def __init__(self, min_value, max_value, initialized_value=None) -> None:
        self._min = min_value
        self._max = max_value
        if initialized_value is None:
            self.value = min_value
        elif initialized_value is not None:
            self.value = initialized_value
        self.normalize()

    @property
    def max(self):
        logging.debug("entering max")
        return self._max

    @max.setter
    def max(self, value):
        logging.debug("entering max setter")
        if self._min > value:
            raise ValueException(self)
        self._max = value
        self.normalize()

    @property
    def min(self):
        logging.debug("entering min")
        return self._min

    @min.setter
    def min(self, value):
        logging.debug("entering min setter")
        if self._max < value:
            raise ValueException(self)
        self._min = value
        self.normalize()

    @property
    def value(self):
        logging.debug("entering value")
        return self._value

    @value.setter
    def value(self, value):
        logging.debug("entering value setter")
        self._value = value
        if self._value > self.max:
            self._value = self.max
        elif self._value < self.min:
            self._value = self.min

    def normalize(self):
        logging.debug("entering normalize")
        self.value = round(self.value)


class Value:
    def __init__(
        self, min_value, max_value, initialized_value=None, initialized_percent=None
    ) -> None:
        self._min = min_value
        self._max = max_value
        if initialized_value is None and initialized_percent is None:
            self.value = min_value
        elif initialized_value is not None:
            self.value = initialized_value
        elif initialized_percent is not None:
            print(
                f"max: {max_value} min: {min_value} initialized: {initialized_percent} "
            )
            self.value = (max_value - min_value) * initialized_percent + min_value
            print(
                f"max: {max_value} min: {min_value} initialized: {initialized_percent} value: {self.value} percent: {self.value_percent}"
            )
        else:
            raise ValueException(self)

    @property
    def max(self):
        logging.debug("entering max")
        return self._max

    @max.setter
    def max(self, value):
        logging.debug("entering max setter")
        if self._min > value:
            raise ValueException(self)
        self._max = value
        self.normalize()

    @property
    def min(self):
        logging.debug("entering min")
        return self._min

    @min.setter
    def min(self, value):
        logging.debug("entering min setter")
        if self._max < value:
            raise ValueException(self)
        self._min = value
        self.normalize()

    @property
    def value(self):
        logging.debug("entering value")
        return self._value

    @property
    def value_percent(self):
        logging.debug("entering value_percent")
        return (self.value - self.min) / (self.max - self.min)

    @value.setter
    def value(self, value):
        logging.debug("entering value setter")
        self._value = value
        if self._value > self.max:
            self._value = self.max
        elif self._value < self.min:
            self._value = self.min

    def normalize(self):
        logging.debug("entering normalize")
        self.value = self.value
