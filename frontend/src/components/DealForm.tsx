import { useState } from 'react'
import type { Deal } from '../types'

interface Props {
  clientId: number
  onSave: (data: Partial<Deal>) => void
  onCancel: () => void
}

export function DealForm({ clientId, onSave, onCancel }: Props) {
  const [title, setTitle] = useState('')
  const [value, setValue] = useState('')
  const [stage, setStage] = useState('lead')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave({ client_id: clientId, title, value: parseFloat(value) || 0, stage })
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      <h4>Nueva Oportunidad</h4>
      <label>Título <input value={title} onChange={e => setTitle(e.target.value)} required /></label>
      <label>Valor $ <input type="number" value={value} onChange={e => setValue(e.target.value)} /></label>
      <label>Etapa
        <select value={stage} onChange={e => setStage(e.target.value)}>
          <option value="lead">Nuevo</option>
          <option value="qualified">Calificado</option>
          <option value="proposal">Propuesta</option>
          <option value="negotiation">Negociación</option>
          <option value="closed_won">Ganado</option>
          <option value="closed_lost">Perdido</option>
        </select>
      </label>
      <div className="form-actions">
        <button type="submit" className="btn primary">Guardar</button>
        <button type="button" className="btn" onClick={onCancel}>Cancelar</button>
      </div>
    </form>
  )
}
