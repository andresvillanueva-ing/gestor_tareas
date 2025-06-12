import uuid
from dominio.modelos.tarea import Tarea


class CrearTarea:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def ejecutar(self, titulo, descripcion, fecha_limite, prioridad):
        tarea = Tarea(
            id=str(uuid.uuid4()),
            titulo= titulo,
            descripcion = descripcion, 
            fecha_limite = fecha_limite,
            prioridad = prioridad
        )
        self.repositorio.guardar(tarea)
        return tarea
    