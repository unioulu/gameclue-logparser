from abc import ABC, abstractmethod


class LogFileSanitizer(ABC):
    """
    LogFileSanitizer, abstract base class for different kind of log sanitizers.
    """

    def __init__(self):
        super(LogFileSanitizer, self).__init__()

    @abstractmethod
    def sanitize(self, LogFile):
        pass
