import type { Client, Interaction, Deal, Task, Note, Stats } from '../types'

const BASE = '/api'

async function request<T>(path: string, opts?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...opts?.headers },
    ...opts,
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export const api = {
  clients: {
    list: (search = '') => request<Client[]>(`/clients?search=${encodeURIComponent(search)}`),
    get: (id: number) => request<Client>(`/clients/${id}`),
    create: (data: Partial<Client>) =>
      request<Client>('/clients', { method: 'POST', body: JSON.stringify(data) }),
    update: (id: number, data: Partial<Client>) =>
      request<Client>(`/clients/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id: number) => request<{ ok: boolean }>(`/clients/${id}`, { method: 'DELETE' }),
  },
  interactions: {
    byClient: (clientId: number) => request<Interaction[]>(`/clients/${clientId}/interactions`),
    create: (data: Partial<Interaction>) =>
      request<Interaction>('/interactions', { method: 'POST', body: JSON.stringify(data) }),
  },
  deals: {
    list: () => request<Deal[]>('/deals'),
    get: (id: number) => request<Deal>(`/deals/${id}`),
    byClient: (clientId: number) => request<Deal[]>(`/deals?client_id=${clientId}`),
    create: (data: Partial<Deal>) =>
      request<Deal>('/deals', { method: 'POST', body: JSON.stringify(data) }),
    update: (id: number, data: Partial<Deal>) =>
      request<Deal>(`/deals/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id: number) => request<{ ok: boolean }>(`/deals/${id}`, { method: 'DELETE' }),
  },
  tasks: {
    list: () => request<Task[]>('/tasks'),
    create: (data: Partial<Task>) =>
      request<Task>('/tasks', { method: 'POST', body: JSON.stringify(data) }),
    update: (id: number, data: Partial<Task>) =>
      request<Task>(`/tasks/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id: number) => request<{ ok: boolean }>(`/tasks/${id}`, { method: 'DELETE' }),
  },
  notes: {
    byClient: (clientId: number) => request<Note[]>(`/clients/${clientId}/notes`),
    create: (data: Partial<Note>) =>
      request<Note>('/notes', { method: 'POST', body: JSON.stringify(data) }),
    delete: (id: number) => request<{ ok: boolean }>(`/notes/${id}`, { method: 'DELETE' }),
  },
  assistant: {
    ask: (query: string) =>
      request<{ response: string }>('/assistant/ask', {
        method: 'POST',
        body: JSON.stringify({ query }),
      }),
  },
  stats: {
    get: () => request<Stats>('/stats'),
  },
}
