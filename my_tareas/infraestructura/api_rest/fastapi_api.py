import os

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from typing import Optional
from infraestructura.repositorios_sqlite.repositorio_sqlite import RepositorioSQLite
from aplicacion.crear_tarea import CrearTarea
from aplicacion.listar_tareas import ListarTareas
from aplicacion.eliminar_tarea import EliminarTarea
from aplicacion.modificar_tarea import ModificarTarea
from dominio.modelos.tarea import Tarea, EstadoTarea


app = FastAPI()

frontend_path = os.path.join(os.path.dirname(__file__), '../../../frontend')
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


repositorio = RepositorioSQLite()
crear_tarea = CrearTarea(repositorio)
listar_tareas = ListarTareas(repositorio)
eliminar_tarea = EliminarTarea(repositorio)
modificar_tarea = ModificarTarea(repositorio)

class TareaEntrada(BaseModel):
    titulo: str
    descripcion: str
    fecha_limite:str
    prioridad: str = "media"

class TareaSalida(BaseModel):
    id: str
    titulo: str
    descripcion: str
    fecha_limite: str
    estado: str
    prioridad: str

class TareaActualizacion(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_limite:Optional[str] = None
    estado: Optional[EstadoTarea] = None
    prioridad: Optional[str] = None

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_path, "index.html"))
    
@app.post("/tareas")
def crear(tarea_entrada: TareaEntrada):
    tarea = crear_tarea.ejecutar(
        titulo=tarea_entrada.titulo,
        descripcion=tarea_entrada.descripcion,
        fecha_limite=tarea_entrada.fecha_limite,
        prioridad=tarea_entrada.prioridad
    )
    return {"mensaje": "Tarea Creada", "id": tarea.id}

@app.get("/tareas", response_model=List[TareaSalida])
def listar():
    tareas = listar_tareas.ejecutar()
    return [
        TareaSalida(
            id= t.id,
            titulo= t.titulo,
            descripcion= t.descripcion,
            fecha_limite= t.fecha_limite,
            estado= t.estado,
            prioridad= t.prioridad
        )
        for t in tareas
    ]

@app.delete("/tareas/{tarea_id}")
def eliminar(tarea_id: str):
    tareas = listar_tareas.ejecutar()
    if not any(t.id == tarea_id for t in tareas):
        raise HTTPException(statu_code=404, detail="Tarea no encontrada")
    
    eliminar_tarea.ejecutar(tarea_id)
    return {"mensaje": "Tarea eliminada"}

@app.put("/tarea/{tarea_id}")
def actualizar(tarea_id: str, datos: TareaActualizacion):
    try:
        modificar_tarea.ejecutar(
            tarea_id=tarea_id,
            titulo=datos.titulo,
            descripcion=datos.descripcion,
            fecha_limite=datos.fecha_limite,
            estado=datos.estado,
            prioridad=datos.prioridad
        )
        return {"mensaje": "Tarea actualizada"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
