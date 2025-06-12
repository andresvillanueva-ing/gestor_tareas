class ModificarTarea:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def ejecutar(self, tarea_id, titulo= None, descripcion=None, fecha_limite=None, estado=None, prioridad=None):
        tarea=self.repositorio.obtener_por_id(tarea_id)
        if not tarea:
            raise ValueError("Tarea no encontrada")

        if titulo is not None:
            tarea.titulo=titulo
        if descripcion is not None:
            tarea.descripcion=descripcion
        if fecha_limite is not None:
            tarea.fecha_limite=fecha_limite
        if estado is not None:
            tarea.estado=estado
        if prioridad is not None:
            tarea.prioridad=prioridad

        self.repositorio.actualizar(tarea)