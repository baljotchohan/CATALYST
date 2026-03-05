/**
 * CATALYST API Client
 * Axios-based client with type-safe response wrappers
 */
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
    baseURL: API_URL,
    timeout: 30_000,
    headers: { 'Content-Type': 'application/json' },
})

// ── Types ────────────────────────────────────────────────────────────

export type AgentType = 'weather' | 'health' | 'education' | 'farm' | 'security'
export type AgentStatus = 'active' | 'idle' | 'running' | 'error'

export interface Agent {
    id: string
    name: string
    type: AgentType
    description: string
    specialization: string | null
    github_url: string | null
    created_by: string | null
    status: AgentStatus
    impact_score: number
    created_at: string
    updated_at: string
}

export interface ResearchLog {
    id: string
    agent_id: string
    result: string | null
    impact_metric: number
    impact_description: string | null
    status: string
    timestamp: string
}

export interface ImpactMetrics {
    total_agents: number
    active_agents: number
    total_research: number
    total_impact_score: number
    people_helped: number
    data_sources_connected: number
    countries_monitored: number
}

export interface AgentCreatePayload {
    name: string
    type: AgentType
    description: string
    specialization?: string
    github_url?: string
    created_by?: string
    data_sources?: string[]
}

// ── Agents ───────────────────────────────────────────────────────────

export async function fetchAgents(params?: { type?: AgentType; search?: string }): Promise<Agent[]> {
    const { data } = await api.get<Agent[]>('/api/agents', { params })
    return data
}

export async function fetchAgent(id: string): Promise<Agent> {
    const { data } = await api.get<Agent>(`/api/agents/${id}`)
    return data
}

export async function createAgent(payload: AgentCreatePayload): Promise<{ status: string; agent_id: string }> {
    const { data } = await api.post('/api/agents', payload)
    return data
}

export async function triggerAgent(id: string): Promise<{ status: string; agent_id: string }> {
    const { data } = await api.post(`/api/agents/${id}/run`)
    return data
}

// ── Research ─────────────────────────────────────────────────────────

export async function fetchResearchLogs(agentId: string, page = 1, limit = 20): Promise<ResearchLog[]> {
    const { data } = await api.get<ResearchLog[]>(`/api/research/${agentId}`, { params: { page, limit } })
    return data
}

// ── Impact ───────────────────────────────────────────────────────────

export async function fetchImpactMetrics(): Promise<ImpactMetrics> {
    const { data } = await api.get<ImpactMetrics>('/api/impact')
    return data
}

// ── Data Sources ─────────────────────────────────────────────────────

export async function fetchWeatherData(latitude: number, longitude: number, city?: string) {
    const { data } = await api.get('/api/data/weather', { params: { latitude, longitude, city } })
    return data
}

export async function fetchHealthData() {
    const { data } = await api.get('/api/data/health')
    return data
}

export async function fetchEducationData() {
    const { data } = await api.get('/api/data/education')
    return data
}

export default api
