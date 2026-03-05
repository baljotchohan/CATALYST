/**
 * CATALYST - Dashboard Page (/dashboard)
 * Real-time global metrics, agent status grid, research feed
 */
import Head from 'next/head'
import Link from 'next/link'
import { useEffect, useState } from 'react'
import { RiRefreshLine, RiPlayCircleLine, RiLoader4Line } from 'react-icons/ri'
import Navigation from '../components/Navigation'
import ImpactStats from '../components/ImpactStats'
import { fetchAgents, fetchImpactMetrics, triggerAgent } from '../lib/api'
import type { Agent, ImpactMetrics } from '../lib/api'

const DEFAULT_METRICS: ImpactMetrics = {
    total_agents: 5, active_agents: 5, total_research: 0,
    total_impact_score: 0, people_helped: 0,
    data_sources_connected: 6, countries_monitored: 12,
}

const SCHEDULE_LABELS: Record<string, string> = {
    weather: 'Every 6 hours', health: 'Every 24 hours',
    education: 'Weekly', farm: 'Every 6 hours', security: 'Every 4 hours',
}

export default function Dashboard() {
    const [agents, setAgents] = useState<Agent[]>([])
    const [metrics, setMetrics] = useState<ImpactMetrics>(DEFAULT_METRICS)
    const [refreshed, setRefreshed] = useState(new Date())
    const [runningId, setRunningId] = useState<string | null>(null)

    const refresh = () => {
        Promise.all([fetchAgents(), fetchImpactMetrics()])
            .then(([a, m]) => { setAgents(a); setMetrics(m); setRefreshed(new Date()) })
            .catch(() => { })
    }

    useEffect(() => { refresh() }, [])

    const handleRun = async (agentId: string) => {
        setRunningId(agentId)
        try { await triggerAgent(agentId) } catch { }
        setTimeout(() => { setRunningId(null); refresh() }, 4000)
    }

    return (
        <>
            <Head>
                <title>Dashboard — CATALYST</title>
                <meta name="description" content="Real-time CATALYST platform metrics and agent status." />
            </Head>
            <div className="page-wrapper grid-pattern">
                <Navigation />
                <div className="max-w-7xl mx-auto px-4 pt-28 pb-20">
                    {/* Header */}
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <p className="section-label mb-1">Live Platform</p>
                            <h1 className="text-3xl font-black">Impact Dashboard</h1>
                        </div>
                        <button onClick={refresh}
                            className="btn-ghost text-sm flex items-center gap-2">
                            <RiRefreshLine /> Refresh
                        </button>
                    </div>

                    {/* Global Stats */}
                    <div className="mb-10">
                        <ImpactStats metrics={metrics} />
                    </div>

                    {/* Agents Status Grid */}
                    <div className="mb-10">
                        <h2 className="text-xl font-bold mb-4">Agent Status</h2>
                        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                            {agents.length === 0
                                ? [...Array(5)].map((_, i) => <div key={i} className="card h-32 shimmer" />)
                                : agents.map(agent => (
                                    <div key={agent.id} className="card">
                                        <div className="flex items-center justify-between mb-3">
                                            <div className="flex items-center gap-2">
                                                <span className={`status-dot status-${agent.status}`} />
                                                <span className="text-xs text-slate-400 capitalize">{agent.status}</span>
                                            </div>
                                            <span className="text-xs text-slate-500">{SCHEDULE_LABELS[agent.type]}</span>
                                        </div>
                                        <Link href={`/agents/${agent.id}`}
                                            className="font-semibold text-slate-100 hover:text-primary-300 transition-colors block mb-1">
                                            {agent.name}
                                        </Link>
                                        <p className="text-xs text-slate-500 capitalize mb-3">{agent.type}</p>

                                        <div className="flex items-center justify-between">
                                            <div className="text-amber-400 text-sm font-bold">
                                                ⚡ {agent.impact_score.toFixed(1)}
                                            </div>
                                            <button
                                                onClick={() => handleRun(agent.id)}
                                                disabled={runningId === agent.id || agent.status === 'running'}
                                                className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg
                                     bg-primary-500/20 text-primary-300 border border-primary-500/30
                                     hover:bg-primary-500/30 transition-colors disabled:opacity-50">
                                                {runningId === agent.id
                                                    ? <RiLoader4Line className="animate-spin" />
                                                    : <RiPlayCircleLine />}
                                                Run
                                            </button>
                                        </div>
                                    </div>
                                ))
                            }
                        </div>
                    </div>

                    {/* Live data connections */}
                    <div>
                        <h2 className="text-xl font-bold mb-4">Connected Data Sources</h2>
                        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                            {[
                                { name: 'Open-Meteo', type: 'Weather', status: 'live', icon: '🌤' },
                                { name: 'WHO Health Observatory', type: 'Health', status: 'live', icon: '🏥' },
                                { name: 'World Bank / UNESCO', type: 'Education', status: 'live', icon: '📚' },
                                { name: 'GDELT News API', type: 'Security', status: 'live', icon: '📰' },
                                { name: 'World Bank Commodities', type: 'Farm', status: 'live', icon: '📈' },
                                { name: 'Claude AI (Anthropic)', type: 'Analysis', status: 'live', icon: '🧠' },
                            ].map(ds => (
                                <div key={ds.name} className="glass rounded-xl p-4 flex items-center gap-3">
                                    <span className="text-xl">{ds.icon}</span>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-medium text-slate-200 truncate">{ds.name}</p>
                                        <p className="text-xs text-slate-500">{ds.type}</p>
                                    </div>
                                    <div className="flex items-center gap-1 shrink-0">
                                        <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full" />
                                        <span className="text-xs text-emerald-400">{ds.status}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <p className="text-center text-slate-700 text-xs mt-8">Last refreshed: {refreshed.toLocaleTimeString()}</p>
                </div>
            </div>
        </>
    )
}
