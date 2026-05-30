import { useState } from 'react'
import { api } from '../services/api'

export function Assistant() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)

  const handleAsk = async () => {
    if (!query.trim()) return
    setLoading(true)
    setResponse('')
    try {
      const res = await api.assistant.ask(query)
      setResponse(res.response)
    } catch {
      setResponse('Error al consultar el asistente. Verifica que la API key de OpenAI esté configurada.')
    }
    setLoading(false)
  }

  return (
    <div>
      <h2>Asistente IA</h2>
      <p className="subtle">Pregunta sobre tus clientes, oportunidades o tareas. El asistente buscará en tu CRM y te responderá con inteligencia artificial.</p>
      <div className="assistant-form">
        <textarea
          className="assistant-input"
          placeholder="Ej: ¿Cómo va la negociación con la empresa TechSolutions?"
          value={query}
          onChange={e => setQuery(e.target.value)}
          rows={3}
        />
        <button className="btn primary" onClick={handleAsk} disabled={loading}>
          {loading ? 'Consultando...' : 'Preguntar'}
        </button>
      </div>
      {response && (
        <div className="assistant-response">
          <h4>Respuesta:</h4>
          <p>{response}</p>
        </div>
      )}
    </div>
  )
}
