import { useState } from 'react'
import type { Client } from '../types'

interface Props {
  initial?: Partial<Client>
  onSave: (data: Partial<Client>) => void
  onCancel: () => void
}

export function ClientForm({ initial, onSave, onCancel }: Props) {
  const [name, setName] = useState(initial?.name || '')
  const [email, setEmail] = useState(initial?.email || '')
  const [phone, setPhone] = useState(initial?.phone || '')
  const [company, setCompany] = useState(initial?.company || '')
  const [notes, setNotes] = useState(initial?.notes || '')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave({ name, email, phone, company, notes })
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      <h3>{initial?.id ? 'Editar Cliente' : 'Nuevo Cliente'}</h3>
      <label>Nombre <input value={name} onChange={e => setName(e.target.value)} required /></label>
      <label>Email <input value={email} onChange={e => setEmail(e.target.value)} /></label>
      <label>Teléfono <input value={phone} onChange={e => setPhone(e.target.value)} /></label>
      <label>Empresa <input value={company} onChange={e => setCompany(e.target.value)} /></label>
      <label>Notas <textarea value={notes} onChange={e => setNotes(e.target.value)} /></label>
      <div className="form-actions">
        <button type="submit" className="btn primary">Guardar</button>
        <button type="button" className="btn" onClick={onCancel}>Cancelar</button>
      </div>
    </form>
  )
}
