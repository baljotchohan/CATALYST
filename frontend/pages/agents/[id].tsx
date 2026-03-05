/**
 * CATALYST - Agent Detail Page (/agents/[id])
 * Full agent info, research history, impact timeline, data sources
 */
import Head from 'next/head'
import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'
import {
    RiExternalLinkLine, RiFlashlightLine, RiLoader4Line,
    RiPlayCircleLine, RiArrowLeftLine, RiTimeLine,
} from 'react-icons/ri'
import Navigation from '../../components/Navigation'
import { fetchAgent, fetchResearchLogs, triggerAgent } from '../../lib/api'
import type { Agent, ResearchLog } from '../../lib/api'

const TYPE_COLORS: Record<string, string> = {
    weather: 'badge-weather', health: 'badge-health', education: 'badge-education',
    farm: 'badge-farm', security: 'badge-security',
}

export default function AgentDetailPage() {
    const router = useRouter()
    const { id } = router.query as { id: string }

    const [agent, setAgent] = useState<Agent | null>(null)
    const [logs, setLogs] = useState<ResearchLog[]>([])
    const [loading, setLoading] = useState(true)
    const [running, setRunning] = useState(false)
    const [error, setError] = useState('')

    useEffect(() => {
        if (!id) return
        Promise.all([fetchAgent(id), fetchResearchLogs(id)])
            .then(([a, l]) => { setAgent(a); setLogs(l) })
            .catch(() => setError('Could not load agent. Is the backend running?'))
            .finally(() => setLoading(false))
    }, [id])

    const handleRun = async () => {
        if (!id || running) return
        setRunning(true)
        try {
            await triggerAgent(id)
            setTimeout(() => {
                fetchResearchLogs(id).then(setLogs)
                fetchAgent(id).then(setAgent)
                setRunning(false)
            }, 3000)
        } catch {
            setRunning(false)
        }
    }

    if (loading) return (
        <div className="page-wrapper"><Navigation />
            <div className="flex items-center justify-center min-h-screen">
                <RiLoader4Line className="text-4xl text-primary-400 animate-spin" />
            </div>
        </div>
    )

    if (error || !agent) return (
        <div className="page-wrapper"><Navigation />
            <div className="flex flex-col items-center justify-center min-h-screen gap-4 text-slate-400">
                <p>{error || 'Agent not found'}</p>
                <button onClick={() => router.push('/agents')} className="btn-ghost text-sm">← Back to Agents</button>
            </div>
        </div>
    )

    return (
        <>
            <Head>
                <title>{agent.name} — CATALYST</title>
                <meta name="description" content={agent.description} />
            </Head>
            <div className="page-wrapper">
                <Navigation />
                <div className="max-w-5xl mx-auto px-4 pt-28 pb-20">

                    {/* Back nav */}
                    <button onClick={() => router.push('/agents')}
                        className="flex items-center gap-1.5 text-slate-500 hover:text-slate-300 text-sm mb-6 transition-colors">
                        <RiArrowLeftLine /> Back to Agents
                    </button>

                    {/* Agent header */}
                    <div className="card mb-6">
                        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                            <div className="flex-1">
                                <div className="flex flex-wrap items-center gap-3 mb-3">
                                    <span className={`badge ${TYPE_COLORS[agent.type]}`}>{agent.type}</span>
                                    <div className="flex items-center gap-1.5">
                                        <span className={`status-dot status-${agent.status}`} />
                                        <span className="text-xs text-slate-500 capitalize">{agent.status}</span>
                                    </div>
                                </div>
                                <h1 className="text-3xl font-black mb-2">{agent.name}</h1>
                                <p className="text-slate-400 leading-relaxed">{agent.description}</p>
                                {agent.specialization && (
                                    <p className="text-sm text-slate-500 mt-2 italic">📍 {agent.specialization}</p>
                                )}
                            </div>

                            {/* Stats */}
                            <div className="flex sm:flex-col gap-4 sm:gap-2 sm:text-right">
                                <div>
                                    <div className="flex items-center gap-1 text-amber-400 sm:justify-end">
                                        <RiFlashlightLine />
                                        <span className="text-2xl font-black">{agent.impact_score.toFixed(1)}</span>
                                    </div>
                                    <p className="text-xs text-slate-500">Impact Score</p>
                                </div>
                                <div>
                                    <p className="text-2xl font-black text-primary-400">{logs.length}</p>
                                    <p className="text-xs text-slate-500">Research Runs</p>
                                </div>
                            </div>
                        </div>

                        {/* Actions */}
                        <div className="flex flex-wrap gap-3 mt-5 pt-5 border-t border-slate-700/50">
                            <button onClick={handleRun} disabled={running || agent.status === 'running'}
                                className="btn-primary flex items-center gap-2 text-sm disabled:opacity-60">
                                {running
                                    ? <><RiLoader4Line className="animate-spin" />Running...</>
                                    : <><RiPlayCircleLine />Run Agent Now</>}
                            </button>
                            {agent.github_url && (
                                <a href={agent.github_url} target="_blank" rel="noopener noreferrer"
                                    className="btn-ghost flex items-center gap-2 text-sm">
                                    <RiExternalLinkLine /> View Source on GitHub
                                </a>
                            )}
                            {agent.created_by && (
                                <p className="self-center text-sm text-slate-500">by @{agent.created_by}</p>
                            )}
                        </div>
                    </div>

                    {/* Research Timeline */}
                    <div>
                        <div className="flex items-center gap-2 mb-5">
                            <RiTimeLine className="text-primary-400" />
                            <h2 className="text-xl font-bold">Research Timeline</h2>
                        </div>

                        {logs.length === 0 ? (
                            <div className="card text-center py-12 text-slate-500">
                                <RiPlayCircleLine className="text-4xl mx-auto mb-2 opacity-30" />
                                <p>No research runs yet. Click "Run Agent Now" to start the first research cycle.</p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {logs.map((log, i) => (
                                    <div key={log.id} className="card">
                                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                                            <div className="flex items-center gap-2">
                                                <span className={`w-2 h-2 rounded-full ${log.status === 'completed' ? 'bg-emerald-400' : 'bg-red-400'}`} />
                                                <span className="text-sm font-medium capitalize">{log.status}</span>
                                                {i === 0 && (
                                                    <span className="text-xs px-2 py-0.5 rounded-full bg-primary-500/20 text-primary-300 border border-primary-500/30">
                                                        Latest
                                                    </span>
                                                )}
                                            </div>
                                            <div className="flex items-center gap-3 text-sm text-slate-500">
                                                {log.impact_description && (
                                                    <span className="text-amber-400 font-medium">⚡ {log.impact_description}</span>
                                                )}
                                                <span>{new Date(log.timestamp).toLocaleString()}</span>
                                            </div>
                                        </div>
                                        {log.result && (
                                            <div className="bg-slate-900/60 rounded-xl p-4 text-sm text-slate-300 whitespace-pre-wrap max-h-64 overflow-y-auto font-mono">
                                                {log.result.length > 800 ? log.result.slice(0, 800) + '…' : log.result}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </>
    )
}
