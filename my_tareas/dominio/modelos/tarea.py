from enum import Enum

class EstadoTarea(str, Enum):
    PENDIENTE= "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"

class Tarea:
    def __init__(self, id, titulo, descripcion, fecha_limite, estado=EstadoTarea.PENDIENTE, prioridad="media"):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.estado = estado
        self.prioridad = prioridad
