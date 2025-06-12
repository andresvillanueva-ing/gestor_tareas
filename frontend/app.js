const API_URL = "http://127.0.0.1:8000/tareas";

document.addEventListener("DOMContentLoaded", () => {
  cargarTareas();

  document.getElementById("tarea-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const tareaId = document.getElementById("tarea-id").value;
    const tareaData = {
      titulo: document.getElementById("titulo").value,
      descripcion: document.getElementById("descripcion").value,
      fecha_limite: document.getElementById("fecha_limite").value,
      prioridad: document.getElementById("prioridad").value
    };

    if (tareaId) {
      // Editar tarea
      await fetch(`${API_URL}/${tareaId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tareaData)
      });
    } else {
      // Crear tarea
      await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tareaData)
      });
    }

    e.target.reset();
    document.getElementById("tarea-id").value = "";
    cargarTareas();
  });
});

async function cargarTareas() {
  const response = await fetch(API_URL);
  const tareas = await response.json();

  const lista = document.getElementById("tareas-lista");
  lista.innerHTML = "";

  tareas.forEach(t => {
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>${t.titulo}</strong> - ${t.descripcion} (venc: ${t.fecha_limite}) - <em>${t.prioridad}</em>
      <button onclick="editarTarea('${t.id}', '${t.titulo}', '${t.descripcion}', '${t.fecha_limite}', '${t.prioridad}')">Editar</button>
      <button onclick="eliminarTarea('${t.id}')">Eliminar</button>
    `;
    lista.appendChild(li);
  });
}

async function eliminarTarea(id) {
  await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  cargarTareas();
}

function editarTarea(id, titulo, descripcion, fecha, prioridad) {
  document.getElementById("tarea-id").value = id;
  document.getElementById("titulo").value = titulo;
  document.getElementById("descripcion").value = descripcion;
  document.getElementById("fecha_limite").value = fecha;
  document.getElementById("prioridad").value = prioridad;
}
