import { useEffect, useState } from 'react'
import type { Deal } from '../types'
import { api } from '../services/api'
import { DealForm } from '../components/DealForm'

const STAGES = [
  { key: 'lead', label: 'Nuevo', icon: '🟢' },
  { key: 'qualified', label: 'Calificado', icon: '🔵' },
  { key: 'proposal', label: 'Propuesta', icon: '🟡' },
  { key: 'negotiation', label: 'Negociación', icon: '🟠' },
  { key: 'closed_won', label: 'Ganado', icon: '🏆' },
  { key: 'closed_lost', label: 'Perdido', icon: '❌' },
]

const stageLabels: Record<string, string> = {}
STAGES.forEach(s => { stageLabels[s.key] = s.label })

export function Deals() {
  const [deals, setDeals] = useState<Deal[]>([])
  const [showForm, setShowForm] = useState(false)

  const load = () => api.deals.list().then(setDeals)
  useEffect(() => { load() }, [])

  const handleCreate = (data: Partial<Deal>) => {
    api.deals.create(data).then(() => { setShowForm(false); load() })
  }

  const handleStageChange = (deal: Deal, newStage: string) => {
    api.deals.update(deal.id, { ...deal, stage: newStage }).then(load)
  }

  return (
    <div>
      <div className="page-header">
        <h2>Oportunidades</h2>
        <button className="btn primary" onClick={() => setShowForm(true)}>+ Nueva Oportunidad</button>
      </div>
      {showForm && (
        <DealForm
          clientId={0}
          onSave={handleCreate}
          onCancel={() => setShowForm(false)}
        />
      )}
      <div className="pipeline">
        {STAGES.map(stage => (
          <div key={stage.key} className={`pipeline-col stage-${stage.key}`}>
            <div className="pipeline-header">
              <span className="stage-icon">{stage.icon}</span>
              <h4>{stage.label}</h4>
              <span className="stage-count">{deals.filter(d => d.stage === stage.key).length}</span>
            </div>
            {deals.filter(d => d.stage === stage.key).map(d => (
              <div key={d.id} className="deal-card">
                <div className="deal-card-title">{d.title}</div>
                <div className="deal-card-value">${d.value.toLocaleString()}</div>
                <select
                  className="stage-select"
                  value={d.stage}
                  onChange={e => handleStageChange(d, e.target.value)}
                >
                  {STAGES.map(s => (
                    <option key={s.key} value={s.key}>{s.label}</option>
                  ))}
                </select>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
