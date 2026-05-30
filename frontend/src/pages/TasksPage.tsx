import { useEffect, useState } from 'react'
import type { Task } from '../types'
import { api } from '../services/api'

const statusLabels: Record<string, string> = {
  pending: 'Pendiente', in_progress: 'En Progreso', completed: 'Completada',
}

const priorityLabels: Record<string, string> = {
  low: 'Baja', medium: 'Media', high: 'Alta',
}

export function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState<Task | null>(null)

  const load = () => api.tasks.list().then(setTasks)
  useEffect(() => { load() }, [])

  const handleSave = (data: Partial<Task>) => {
    const promise = editing
      ? api.tasks.update(editing.id!, data)
      : api.tasks.create(data)
    promise.then(() => { setShowForm(false); setEditing(null); load() })
  }

  const handleDelete = (id: number) => {
    if (confirm('¿Eliminar tarea?')) api.tasks.delete(id).then(load)
  }

  return (
    <div>
      <div className="page-header">
        <h2>Tareas</h2>
        <button className="btn primary" onClick={() => { setShowForm(true); setEditing(null) }}>+ Nueva Tarea</button>
      </div>
      {showForm && (
        <TaskForm
          initial={editing || undefined}
          onSave={handleSave}
          onCancel={() => { setShowForm(false); setEditing(null) }}
        />
      )}
      <div className="table-container">
        <table className="table">
          <thead><tr><th>Título</th><th>Estado</th><th>Prioridad</th><th></th></tr></thead>
          <tbody>
            {tasks.map(t => (
              <tr key={t.id}>
                <td style={{ fontWeight: 500 }}>{t.title}</td>
                <td><span className={`status-badge status-${t.status}`}>{statusLabels[t.status] || t.status}</span></td>
                <td><span className={`status-badge priority-${t.priority}`}>{priorityLabels[t.priority] || t.priority}</span></td>
                <td>
                  <button className="btn small" onClick={() => { setEditing(t); setShowForm(true) }}>Editar</button>
                  <button className="btn small danger" onClick={() => handleDelete(t.id)} style={{ marginLeft: '0.35rem' }}>Eliminar</button>
                </td>
              </tr>
            ))}
            {tasks.length === 0 && <tr><td colSpan={4} style={{ color: '#B2BEC3', textAlign: 'center', padding: '2rem' }}>Sin tareas registradas</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function TaskForm({ initial, onSave, onCancel }: { initial?: Partial<Task>; onSave: (d: Partial<Task>) => void; onCancel: () => void }) {
  const [title, setTitle] = useState(initial?.title || '')
  const [description, setDescription] = useState(initial?.description || '')
  const [status, setStatus] = useState(initial?.status || 'pending')
  const [priority, setPriority] = useState(initial?.priority || 'medium')

  return (
    <form className="form" onSubmit={e => { e.preventDefault(); onSave({ title, description, status, priority }) }}>
      <h3>{initial?.id ? 'Editar Tarea' : 'Nueva Tarea'}</h3>
      <label>Título <input value={title} onChange={e => setTitle(e.target.value)} required /></label>
      <label>Descripción <textarea value={description} onChange={e => setDescription(e.target.value)} /></label>
      <label>Estado
        <select value={status} onChange={e => setStatus(e.target.value)}>
          <option value="pending">Pendiente</option><option value="in_progress">En Progreso</option><option value="completed">Completada</option>
        </select>
      </label>
      <label>Prioridad
        <select value={priority} onChange={e => setPriority(e.target.value)}>
          <option value="low">Baja</option><option value="medium">Media</option><option value="high">Alta</option>
        </select>
      </label>
      <div className="form-actions">
        <button type="submit" className="btn primary">Guardar</button>
        <button type="button" className="btn" onClick={onCancel}>Cancelar</button>
      </div>
    </form>
  )
}
