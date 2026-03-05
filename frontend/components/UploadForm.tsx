/**
 * CATALYST - Upload Form Component
 * Controlled form for uploading a new agent
 */
import { useState } from 'react'
import { useRouter } from 'next/router'
import { createAgent } from '../lib/api'
import type { AgentType } from '../lib/api'
import { RiRocketLine, RiLoader4Line } from 'react-icons/ri'

const AGENT_TYPES: { value: AgentType; label: string; description: string }[] = [
    { value: 'weather', label: '🌤 Weather', description: 'Meteorology & climate analysis' },
    { value: 'health', label: '🏥 Health', description: 'Disease surveillance & alerts' },
    { value: 'education', label: '📚 Education', description: 'Learning outcomes & literacy' },
    { value: 'farm', label: '🌾 Farm', description: 'Crop advice & market timing' },
    { value: 'security', label: '🛡 Security', description: 'Threat detection & alerts' },
]

const DATA_SOURCE_OPTIONS = [
    'Open-Meteo (Weather)',
    'WHO Global Health Observatory',
    'World Bank / UNESCO Education',
    'GDELT News API',
    'World Bank Commodities',
    'OpenAQ Air Quality',
    'NewsAPI',
    'Custom API',
]

interface FormData {
    name: string
    type: AgentType
    description: string
    specialization: string
    github_url: string
    created_by: string
    data_sources: string[]
}

export default function UploadForm() {
    const router = useRouter()
    const [form, setForm] = useState<FormData>({
        name: '', type: 'weather', description: '', specialization: '',
        github_url: '', created_by: '', data_sources: [],
    })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')

    const toggleSource = (source: string) => {
        setForm(f => ({
            ...f,
            data_sources: f.data_sources.includes(source)
                ? f.data_sources.filter(s => s !== source)
                : [...f.data_sources, source],
        }))
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        setSuccess('')

        if (!form.name.trim() || !form.description.trim()) {
            setError('Name and description are required.')
            return
        }

        setLoading(true)
        try {
            const result = await createAgent(form)
            setSuccess(`Agent created! ID: ${result.agent_id}`)
            setTimeout(() => router.push(`/agents/${result.agent_id}`), 1500)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to create agent. Is the backend running?')
        } finally {
            setLoading(false)
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-6">

            {/* Name */}
            <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">Agent Name *</label>
                <input
                    type="text" required
                    value={form.name}
                    onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
                    className="w-full px-4 py-3 rounded-xl bg-slate-800/70 border border-slate-700 text-white
                     placeholder-slate-500 focus:outline-none focus:border-primary-500 focus:ring-1
                     focus:ring-primary-500/50 transition-colors"
                    placeholder="e.g. Flood Risk Analyzer"
                />
            </div>

            {/* Type */}
            <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Agent Type *</label>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2">
                    {AGENT_TYPES.map(t => (
                        <button key={t.value} type="button"
                            onClick={() => setForm(f => ({ ...f, type: t.value }))}
                            className={`px-3 py-2.5 rounded-xl border text-left transition-all duration-200 text-sm
                ${form.type === t.value
                                    ? 'border-primary-500 bg-primary-500/20 text-primary-300'
                                    : 'border-slate-700 bg-slate-800/50 text-slate-400 hover:border-slate-600 hover:text-slate-200'}`}>
                            <div className="font-medium">{t.label}</div>
                            <div className="text-xs text-slate-500 mt-0.5 hidden sm:block">{t.description}</div>
                        </button>
                    ))}
                </div>
            </div>

            {/* Description */}
            <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">Description *</label>
                <textarea
                    required rows={4}
                    value={form.description}
                    onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
                    className="w-full px-4 py-3 rounded-xl bg-slate-800/70 border border-slate-700 text-white
                     placeholder-slate-500 focus:outline-none focus:border-primary-500 focus:ring-1
                     focus:ring-primary-500/50 transition-colors resize-none"
                    placeholder="What problem does this agent solve? What data does it analyze and what insights does it generate?"
                />
            </div>

            {/* Specialization */}
            <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">Specialization</label>
                <input
                    type="text"
                    value={form.specialization}
                    onChange={e => setForm(f => ({ ...f, specialization: e.target.value }))}
                    className="w-full px-4 py-3 rounded-xl bg-slate-800/70 border border-slate-700 text-white
                     placeholder-slate-500 focus:outline-none focus:border-primary-500 focus:ring-1
                     focus:ring-primary-500/50 transition-colors"
                    placeholder="e.g. Flood risk in river delta regions, Bangladesh"
                />
            </div>

            {/* GitHub URL */}
            <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">GitHub Repository URL</label>
                <input
                    type="url"
                    value={form.github_url}
                    onChange={e => setForm(f => ({ ...f, github_url: e.target.value }))}
                    className="w-full px-4 py-3 rounded-xl bg-slate-800/70 border border-slate-700 text-white
                     placeholder-slate-500 focus:outline-none focus:border-primary-500 focus:ring-1
                     focus:ring-primary-500/50 transition-colors"
                    placeholder="https://github.com/username/my-agent"
                />
            </div>

            {/* Creator */}
            <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">Your GitHub Username</label>
                <input
                    type="text"
                    value={form.created_by}
                    onChange={e => setForm(f => ({ ...f, created_by: e.target.value }))}
                    className="w-full px-4 py-3 rounded-xl bg-slate-800/70 border border-slate-700 text-white
                     placeholder-slate-500 focus:outline-none focus:border-primary-500 focus:ring-1
                     focus:ring-primary-500/50 transition-colors"
                    placeholder="@yourusername"
                />
            </div>

            {/* Data Sources */}
            <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Data Sources Used</label>
                <div className="flex flex-wrap gap-2">
                    {DATA_SOURCE_OPTIONS.map(src => (
                        <button key={src} type="button"
                            onClick={() => toggleSource(src)}
                            className={`px-3 py-1.5 rounded-lg border text-xs font-medium transition-all duration-200
                ${form.data_sources.includes(src)
                                    ? 'border-accent-500 bg-accent-500/20 text-accent-300'
                                    : 'border-slate-700 bg-slate-800/50 text-slate-400 hover:border-slate-500 hover:text-slate-300'}`}>
                            {src}
                        </button>
                    ))}
                </div>
            </div>

            {/* Messages */}
            {error && <p className="text-sm text-red-400 bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3">{error}</p>}
            {success && <p className="text-sm text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-xl px-4 py-3">{success}</p>}

            {/* Submit */}
            <button type="submit" disabled={loading} className="btn-primary w-full text-center flex items-center justify-center gap-2 disabled:opacity-60">
                {loading
                    ? <><RiLoader4Line className="animate-spin" />Uploading Agent...</>
                    : <><RiRocketLine />Launch Agent on CATALYST</>}
            </button>
        </form>
    )
}
