export interface Client {
  id: number
  name: string
  email: string
  phone: string
  company: string
  notes: string
  owner_id: number | null
  created_at: string
  updated_at: string
}

export interface Interaction {
  id: number
  client_id: number
  type: string
  subject: string
  description: string
  created_at: string
}

export interface Deal {
  id: number
  client_id: number
  title: string
  value: number
  stage: string
  created_at: string
  updated_at: string
}

export interface Task {
  id: number
  client_id: number | null
  title: string
  description: string
  status: string
  priority: string
  created_at: string
}

export interface Note {
  id: number
  client_id: number
  content: string
  created_at: string
}

export interface Stats {
  total_clients: number
  total_deals: number
  total_tasks: number
  total_interactions: number
}
