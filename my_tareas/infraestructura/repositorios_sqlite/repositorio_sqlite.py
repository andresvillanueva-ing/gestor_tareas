import sqlite3
from dominio.repositorios.tarea_repositorio import TareaRepositorio
from dominio.modelos.tarea import Tarea, EstadoTarea

class RepositorioSQLite(TareaRepositorio):
    def __init__(self, db_path="tareas.db"):
        self.conn=sqlite3.connect(db_path, check_same_thread=False)
        self._crear_tabla()

    def _crear_tabla(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
            id TEXT PRIMARY KEY,
            titulo TEXT,
            descripcion TEXT,
            fecha_limite TEXT,
            estado TEXT,
            prioridad TEXT
            )
            """
        )
        self.conn.commit()

    def guardar(self, tarea):
        self.conn.execute("""
            INSERT INTO tareas (id, titulo, descripcion, fecha_limite, estado, prioridad)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tarea.id, tarea.titulo, tarea.descripcion, tarea.fecha_limite, tarea.estado, tarea.prioridad))
        self.conn.commit()

    def listar(self):
        cursor = self.conn.execute("SELECT id, titulo, descripcion, fecha_limite, estado, prioridad FROM tareas")
        tareas= []
        for fila in cursor:
            tarea = Tarea(
                id=fila[0],
                titulo=fila[1],
                descripcion=fila[2],
                fecha_limite=fila[3],
                estado=EstadoTarea(fila[4]),
                prioridad=fila[5]
            )
            tareas.append(tarea)
        return tareas

    def eliminar(self, tarea_id: str):
        with self.conn:
            self.conn.execute("DELETE FROM tareas WHERE id=?", (tarea_id,))
    
    def obtener_por_id(self, tarea_id: str):
        cursor = self.conn.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,))
        row = cursor.fetchone()
        if row:
            return Tarea(
                id=row[0],
                titulo=row[1],
                descripcion=row[2],
                fecha_limite=row[3],
                estado=EstadoTarea(row[4]),  # Aquí parseas correctamente
                prioridad=row[5]
            )
        return None

    def actualizar(self, tarea):
        with self.conn:
            self.conn.execute("""
                UPDATE tareas
                SET titulo = ?, descripcion=?, fecha_limite=?, estado=?, prioridad=?
                WHERE id = ?
            """, (tarea.titulo, tarea.descripcion, tarea.fecha_limite, tarea.estado, tarea.prioridad, tarea.id))
            