import { useEffect, useState } from 'react'
import type { Client } from '../types'
import { api } from '../services/api'
import { ClientForm } from '../components/ClientForm'

export function Clients() {
  const [clients, setClients] = useState<Client[]>([])
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState<Client | null>(null)
  const [selected, setSelected] = useState<Client | null>(null)

  const load = () => api.clients.list(search).then(setClients)
  useEffect(() => { load() }, [search])

  const handleSave = (data: Partial<Client>) => {
    const promise = editing
      ? api.clients.update(editing.id!, data)
      : api.clients.create(data)
    promise.then(() => { setShowForm(false); setEditing(null); load() })
  }

  const handleDelete = (id: number) => {
    if (confirm('¿Eliminar este cliente?')) {
      api.clients.delete(id).then(() => load())
    }
  }

  return (
    <div>
      <div className="page-header">
        <h2>Clientes</h2>
        <button className="btn primary" onClick={() => { setShowForm(true); setEditing(null) }}>+ Nuevo Cliente</button>
      </div>
      <input
        className="search-input"
        placeholder="Buscar clientes por nombre, email o empresa..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      {showForm && (
        <ClientForm
          initial={editing || undefined}
          onSave={handleSave}
          onCancel={() => { setShowForm(false); setEditing(null) }}
        />
      )}
      <div className="table-container">
        <table className="table">
          <thead><tr><th>Nombre</th><th>Email</th><th>Empresa</th><th>Teléfono</th><th></th></tr></thead>
          <tbody>
            {clients.map(c => (
              <tr key={c.id}>
                <td>
                  <a href="#" onClick={e => { e.preventDefault(); setSelected(selected?.id === c.id ? null : c) }}>
                    {c.name}
                  </a>
                </td>
                <td>{c.email}</td>
                <td>{c.company}</td>
                <td>{c.phone}</td>
                <td>
                  <button className="btn small" onClick={() => { setEditing(c); setShowForm(true) }}>Editar</button>
                  <button className="btn small danger" onClick={() => handleDelete(c.id)} style={{ marginLeft: '0.35rem' }}>Eliminar</button>
                </td>
              </tr>
            ))}
            {clients.length === 0 && (
              <tr><td colSpan={5} style={{ color: '#B2BEC3', textAlign: 'center', padding: '2rem' }}>No se encontraron clientes</td></tr>
            )}
          </tbody>
        </table>
      </div>
      {selected && <ClientDetail client={selected} onClose={() => setSelected(null)} />}
    </div>
  )
}

function ClientDetail({ client, onClose }: { client: Client; onClose: () => void }) {
  const [tab, setTab] = useState<'interactions' | 'notes'>('interactions')
  const [data, setData] = useState<any[]>([])
  const [showForm, setShowForm] = useState(false)

  const loadData = () => {
    if (tab === 'interactions') {
      api.interactions.byClient(client.id).then(setData)
    } else {
      api.notes.byClient(client.id).then(setData)
    }
  }

  useEffect(() => { loadData() }, [tab])

  const handleInteractionCreate = (d: any) => {
    api.interactions.create(d).then(() => { setShowForm(false); loadData() })
  }

  const handleNoteCreate = (d: any) => {
    api.notes.create(d).then(() => { setShowForm(false); loadData() })
  }

  return (
    <div className="modal">
      <div className="modal-content">
        <div className="flex-between">
          <h3>{client.name}</h3>
          <button className="btn" onClick={onClose}>✕ Cerrar</button>
        </div>
        <div style={{ background: '#F8F9FA', padding: '1rem', borderRadius: '8px', marginBottom: '1.25rem', fontSize: '0.9rem', lineHeight: 1.8 }}>
          <strong>Email:</strong> {client.email || '—'}&nbsp;&nbsp;|&nbsp;&nbsp;
          <strong>Teléfono:</strong> {client.phone || '—'}&nbsp;&nbsp;|&nbsp;&nbsp;
          <strong>Empresa:</strong> {client.company || '—'}
          {client.notes && <><br /><strong>Notas:</strong> {client.notes}</>}
        </div>
        <div className="tabs">
          <button className={`tab-btn ${tab === 'interactions' ? 'active' : ''}`} onClick={() => setTab('interactions')}>Interacciones</button>
          <button className={`tab-btn ${tab === 'notes' ? 'active' : ''}`} onClick={() => setTab('notes')}>Notas</button>
        </div>
        <button className="btn primary small" onClick={() => setShowForm(true)} style={{ marginBottom: '0.75rem' }}>
          + {tab === 'interactions' ? 'Registrar Interacción' : 'Agregar Nota'}
        </button>
        {showForm && tab === 'interactions' && (
          <InteractionFormInline clientId={client.id} onSave={handleInteractionCreate} onCancel={() => setShowForm(false)} />
        )}
        {showForm && tab === 'notes' && (
          <NoteFormInline clientId={client.id} onSave={handleNoteCreate} onCancel={() => setShowForm(false)} />
        )}
        <ul className="data-list">
          {data.map((item: any) => (
            <li key={item.id}>
              {tab === 'interactions' && (
                <><span className={`type-badge type-${item.type}`}>{item.type}</span> <strong>{item.subject}</strong> — {item.description} <em>{new Date(item.created_at).toLocaleDateString()}</em></>
              )}
              {tab === 'notes' && <>{item.content} <em>{new Date(item.created_at).toLocaleDateString()}</em></>}
            </li>
          ))}
          {data.length === 0 && <li style={{ color: '#B2BEC3', textAlign: 'center' }}>Sin registros</li>}
        </ul>
      </div>
    </div>
  )
}

function InteractionFormInline({ clientId, onSave, onCancel }: { clientId: number; onSave: (d: any) => void; onCancel: () => void }) {
  const [type, setType] = useState('call')
  const [subject, setSubject] = useState('')
  const [description, setDescription] = useState('')
  return (
    <form className="form" onSubmit={e => { e.preventDefault(); onSave({ client_id: clientId, type, subject, description }) }} style={{ marginBottom: '0.75rem' }}>
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem', flexWrap: 'wrap' }}>
        <select value={type} onChange={e => setType(e.target.value)} style={{ flex: 1, minWidth: '120px' }}>
          <option value="call">📞 Llamada</option>
          <option value="email">✉️ Email</option>
          <option value="meeting">🤝 Reunión</option>
        </select>
        <input placeholder="Asunto" value={subject} onChange={e => setSubject(e.target.value)} style={{ flex: 2, minWidth: '150px' }} />
      </div>
      <textarea placeholder="Descripción" value={description} onChange={e => setDescription(e.target.value)} style={{ marginBottom: '0.5rem' }} />
      <div className="form-actions"><button type="submit" className="btn primary small">Guardar</button><button type="button" className="btn small" onClick={onCancel}>Cancelar</button></div>
    </form>
  )
}

function NoteFormInline({ clientId, onSave, onCancel }: { clientId: number; onSave: (d: any) => void; onCancel: () => void }) {
  const [content, setContent] = useState('')
  return (
    <form className="form" onSubmit={e => { e.preventDefault(); onSave({ client_id: clientId, content }) }} style={{ marginBottom: '0.75rem' }}>
      <textarea placeholder="Contenido de la nota" value={content} onChange={e => setContent(e.target.value)} />
      <div className="form-actions"><button type="submit" className="btn primary small">Guardar</button><button type="button" className="btn small" onClick={onCancel}>Cancelar</button></div>
    </form>
  )
}
