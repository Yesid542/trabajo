import { useState, useEffect } from 'react'

function TaskList() {
  const [tasks, setTasks] = useState([])
  const [newTask, setNewTask] = useState('')

  // Obtener tareas al cargar el componente
  useEffect(() => {
    fetch('http://localhost:5000/api/tasks')
      .then(res => res.json())
      .then(data => setTasks(data))
  }, [])

  // Agregar nueva tarea
  const handleSubmit = (e) => {
    e.preventDefault()
    fetch('http://localhost:5000/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTask })
    })
      .then(() => {
        setNewTask('')
        return fetch('http://localhost:5000/api/tasks')
      })
      .then(res => res.json())
      .then(data => setTasks(data))
  }

  return (
    <div>
      <h2>Lista de Tareas</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Nueva tarea"
        />
        <button type="submit">Agregar</button>
      </form>
      <ul>
        {tasks.map(task => (
          <li key={task[0]}>{task[1]} - {task[2] ? 'Completada' : 'Pendiente'}</li>
        ))}
      </ul>
    </div>
  )
}

export default TaskList