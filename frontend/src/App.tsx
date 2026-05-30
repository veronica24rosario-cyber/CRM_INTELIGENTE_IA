import { useState } from 'react'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { Clients } from './pages/Clients'
import { Deals } from './pages/Deals'
import { TasksPage } from './pages/TasksPage'
import { Assistant } from './pages/Assistant'

type Page = 'dashboard' | 'clientes' | 'oportunidades' | 'tareas' | 'asistente'

const navItems: { id: Page; label: string; icon: string }[] = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  { id: 'clientes', label: 'Clientes', icon: '👥' },
  { id: 'oportunidades', label: 'Oportunidades', icon: '💼' },
  { id: 'tareas', label: 'Tareas', icon: '✅' },
  { id: 'asistente', label: 'Asistente IA', icon: '🤖' },
]

export function App() {
  const [page, setPage] = useState<Page>('dashboard')

  return (
    <div className="app-layout">
      <nav className="sidebar">
        <div className="sidebar-logo">
          <h1>CRM Inteligente</h1>
          <span>Gestión de clientes</span>
        </div>
        {navItems.map(item => (
          <button
            key={item.id}
            className={`nav-item ${page === item.id ? 'active' : ''}`}
            onClick={() => setPage(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
      <main className="main-content">
        {page === 'dashboard' && <Dashboard />}
        {page === 'clientes' && <Clients />}
        {page === 'oportunidades' && <Deals />}
        {page === 'tareas' && <TasksPage />}
        {page === 'asistente' && <Assistant />}
      </main>
    </div>
  )
}
