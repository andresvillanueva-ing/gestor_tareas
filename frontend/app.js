const API_URL = "http://127.0.0.1:8000/tareas";

document.addEventListener("DOMContentLoaded", () => {
  cargarTareas();

  document.getElementById("tarea-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const nuevaTarea = {
      titulo: document.getElementById("titulo").value,
      descripcion: document.getElementById("descripcion").value,
      fecha_limite: document.getElementById("fecha_limite").value,
      prioridad: document.getElementById("prioridad").value
    };

    await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(nuevaTarea)
    });

    e.target.reset();
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
      <button onclick="eliminarTarea('${t.id}')">Eliminar</button>
    `;
    lista.appendChild(li);
  });
}

async function eliminarTarea(id) {
  await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  cargarTareas();
}