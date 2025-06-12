from dominio.repositorios.tarea_repositorio import TareaRepositorio

class ListarTareas:
    def __init__(self, repositorio: TareaRepositorio):
        self.repositorio = repositorio

    def ejecutar(self):
        return self.repositorio.listar()
