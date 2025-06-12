from dominio.repositorios.tarea_repositorio import TareaRepositorio

class EliminarTarea:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def ejecutar(self, tarea_id: str):
        self.repositorio.eliminar(tarea_id)
