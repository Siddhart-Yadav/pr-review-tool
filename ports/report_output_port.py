from abc import ABC, abstractmethod

class ReportOutputPort(ABC):
    @abstractmethod
    def write(self, report):
        pass 