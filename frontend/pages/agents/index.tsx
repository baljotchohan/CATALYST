/**
 * CATALYST - Agents Marketplace (/agents)
 * Filterable grid with search, type filter, and agent cards
 */
import Head from 'next/head'
import { useEffect, useState } from 'react'
import { RiSearchLine, RiFilterLine } from 'react-icons/ri'
import Navigation from '../../components/Navigation'
import AgentCard from '../../components/AgentCard'
import { fetchAgents } from '../../lib/api'
import type { Agent, AgentType } from '../../lib/api'

const TYPE_FILTERS: { value: string; label: string }[] = [
    { value: '', label: 'All Types' },
    { value: 'weather', label: '🌤 Weather' },
    { value: 'health', label: '🏥 Health' },
    { value: 'education', label: '📚 Education' },
    { value: 'farm', label: '🌾 Farm' },
    { value: 'security', label: '🛡 Security' },
]

export default function AgentsPage() {
    const [agents, setAgents] = useState<Agent[]>([])
    const [filter, setFilter] = useState('')
    const [search, setSearch] = useState('')
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        setLoading(true)
        fetchAgents({ type: filter as AgentType || undefined, search: search || undefined })
            .then(setAgents)
            .catch(() => setAgents([]))
            .finally(() => setLoading(false))
    }, [filter, search])

    return (
        <>
            <Head>
                <title>Agents — CATALYST</title>
                <meta name="description" content="Browse all AI research agents on the CATALYST platform." />
            </Head>
            <div className="page-wrapper">
                <Navigation />
                <div className="max-w-7xl mx-auto px-4 pt-28 pb-20">
                    {/* Header */}
                    <div className="mb-10">
                        <p className="section-label mb-2">Marketplace</p>
                        <h1 className="text-4xl font-black mb-4">Research Agents</h1>
                        <p className="text-slate-400 max-w-xl">
                            Browse AI agents solving real-world problems with live data. Click any agent to see its latest research.
                        </p>
                    </div>

                    {/* Filters */}
                    <div className="flex flex-col sm:flex-row gap-3 mb-8">
                        {/* Search */}
                        <div className="relative flex-1 max-w-md">
                            <RiSearchLine className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                            <input
                                type="text"
                                value={search}
                                onChange={e => setSearch(e.target.value)}
                                placeholder="Search agents..."
                                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-800/70 border border-slate-700
                           text-white placeholder-slate-500 focus:outline-none focus:border-primary-500 transition-colors"
                            />
                        </div>

                        {/* Type filter */}
                        <div className="flex gap-2 flex-wrap">
                            {TYPE_FILTERS.map(t => (
                                <button key={t.value}
                                    onClick={() => setFilter(t.value)}
                                    className={`px-4 py-2.5 rounded-xl border text-sm font-medium transition-all duration-200
                    ${filter === t.value
                                            ? 'border-primary-500 bg-primary-500/20 text-primary-300'
                                            : 'border-slate-700 bg-slate-800/50 text-slate-400 hover:text-slate-200 hover:border-slate-600'}`}>
                                    {t.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Grid */}
                    {loading ? (
                        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
                            {[...Array(6)].map((_, i) => <div key={i} className="card h-56 shimmer" />)}
                        </div>
                    ) : agents.length > 0 ? (
                        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
                            {agents.map(a => <AgentCard key={a.id} agent={a} />)}
                        </div>
                    ) : (
                        <div className="text-center py-20 text-slate-500">
                            <RiFilterLine className="text-5xl mx-auto mb-3 opacity-30" />
                            <p className="text-lg font-medium">No agents found</p>
                            <p className="text-sm mt-1">Try adjusting your search or filter</p>
                        </div>
                    )}

                    {/* Count */}
                    {!loading && agents.length > 0 && (
                        <p className="text-center text-slate-600 text-sm mt-8">{agents.length} agent{agents.length !== 1 ? 's' : ''} found</p>
                    )}
                </div>
            </div>
        </>
    )
}
