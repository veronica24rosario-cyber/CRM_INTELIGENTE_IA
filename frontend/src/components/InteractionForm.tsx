import { useState } from 'react'
import type { Interaction } from '../types'

interface Props {
  clientId: number
  onSave: (data: Partial<Interaction>) => void
  onCancel: () => void
}

export function InteractionForm({ clientId, onSave, onCancel }: Props) {
  const [type, setType] = useState('call')
  const [subject, setSubject] = useState('')
  const [description, setDescription] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave({ client_id: clientId, type, subject, description })
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      <h4>Nueva Interacción</h4>
      <label>Tipo
        <select value={type} onChange={e => setType(e.target.value)}>
          <option value="call">Llamada</option>
          <option value="email">Email</option>
          <option value="meeting">Reunión</option>
          <option value="note">Nota</option>
        </select>
      </label>
      <label>Asunto <input value={subject} onChange={e => setSubject(e.target.value)} /></label>
      <label>Descripción <textarea value={description} onChange={e => setDescription(e.target.value)} /></label>
      <div className="form-actions">
        <button type="submit" className="btn primary">Guardar</button>
        <button type="button" className="btn" onClick={onCancel}>Cancelar</button>
      </div>
    </form>
  )
}
