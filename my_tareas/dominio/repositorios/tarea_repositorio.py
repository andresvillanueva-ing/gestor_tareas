from abc import ABC, abstractmethod

class TareaRepositorio(ABC):
    @abstractmethod
    def guardar(self, tarea): pass

    @abstractmethod
    def listar(self): pass

    @abstractmethod
    def eliminar(self, id): pass
