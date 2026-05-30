import { useEffect, useState } from 'react'
import type { Stats, Deal, Task } from '../types'
import { api } from '../services/api'

const stageLabels: Record<string, string> = {
  lead: 'Nuevo', qualified: 'Calificado', proposal: 'Propuesta',
  negotiation: 'Negociación', closed_won: 'Ganado', closed_lost: 'Perdido',
}

export function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [deals, setDeals] = useState<Deal[]>([])
  const [tasks, setTasks] = useState<Task[]>([])

  useEffect(() => {
    api.stats.get().then(setStats)
    api.deals.list().then(setDeals)
    api.tasks.list().then(setTasks)
  }, [])

  return (
    <div>
      <div className="page-header">
        <h2>Dashboard</h2>
      </div>
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Clientes</div>
            <div className="stat-value">{stats.total_clients}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Oportunidades</div>
            <div className="stat-value">{stats.total_deals}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Tareas</div>
            <div className="stat-value">{stats.total_tasks}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Interacciones</div>
            <div className="stat-value">{stats.total_interactions}</div>
          </div>
        </div>
      )}
      <div className="grid-2">
        <div className="table-container">
          <h3 style={{ padding: '1rem 1.25rem 0', fontSize: '0.95rem' }}>Oportunidades Recientes</h3>
          <table className="table">
            <thead><tr><th>Título</th><th>Valor</th><th>Etapa</th></tr></thead>
            <tbody>
              {deals.slice(0, 5).map(d => (
                <tr key={d.id}>
                  <td><a href="#oportunidades">{d.title}</a></td>
                  <td><strong>${d.value.toLocaleString()}</strong></td>
                  <td><span className={`status-badge`} style={{background: 'rgba(108,99,255,0.1)', color: '#6C63FF'}}>{stageLabels[d.stage] || d.stage}</span></td>
                </tr>
              ))}
              {deals.length === 0 && <tr><td colSpan={3} style={{color: '#B2BEC3', textAlign: 'center', padding: '2rem'}}>Sin oportunidades aún</td></tr>}
            </tbody>
          </table>
        </div>
        <div className="table-container">
          <h3 style={{ padding: '1rem 1.25rem 0', fontSize: '0.95rem' }}>Tareas Pendientes</h3>
          <table className="table">
            <thead><tr><th>Título</th><th>Prioridad</th></tr></thead>
            <tbody>
              {tasks.filter(t => t.status === 'pending').slice(0, 5).map(t => (
                <tr key={t.id}>
                  <td>{t.title}</td>
                  <td><span className={`status-badge priority-${t.priority}`}>{t.priority}</span></td>
                </tr>
              ))}
              {tasks.filter(t => t.status === 'pending').length === 0 && <tr><td colSpan={2} style={{color: '#B2BEC3', textAlign: 'center', padding: '2rem'}}>Sin tareas pendientes</td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
