from abc import ABC, abstractmethod, abstractproperty


class Stock(ABC):
    service_name = None

    @abstractmethod
    def upload(self, model):
        pass

    def get_name(self):
        return self.service_name
