/**
 * CATALYST - Agent Card Component
 * Displays agent info with gradient borders, type badges, and status indicators
 */
import Link from 'next/link'
import {
    RiCloudyLine, RiHeartPulseLine, RiBookOpenLine,
    RiSeedlingLine, RiShieldLine, RiExternalLinkLine,
    RiFlashlightLine,
} from 'react-icons/ri'
import type { Agent } from '../lib/api'

const TYPE_CONFIG: Record<string, { icon: React.ReactNode; label: string; color: string }> = {
    weather: { icon: <RiCloudyLine />, label: 'Weather', color: 'badge-weather' },
    health: { icon: <RiHeartPulseLine />, label: 'Health', color: 'badge-health' },
    education: { icon: <RiBookOpenLine />, label: 'Education', color: 'badge-education' },
    farm: { icon: <RiSeedlingLine />, label: 'Farm', color: 'badge-farm' },
    security: { icon: <RiShieldLine />, label: 'Security', color: 'badge-security' },
}

interface AgentCardProps {
    agent: Agent
}

export default function AgentCard({ agent }: AgentCardProps) {
    const typeConf = TYPE_CONFIG[agent.type] ?? TYPE_CONFIG.weather
    const lastUpdated = new Date(agent.updated_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })

    return (
        <Link href={`/agents/${agent.id}`}>
            <article className="card cursor-pointer group h-full flex flex-col">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                    <span className={`badge ${typeConf.color}`}>
                        <span className="text-base">{typeConf.icon}</span>
                        {typeConf.label}
                    </span>
                    <div className="flex items-center gap-1.5">
                        <span className={`status-dot status-${agent.status}`} />
                        <span className="text-xs text-slate-500 capitalize">{agent.status}</span>
                    </div>
                </div>

                {/* Title */}
                <h3 className="text-lg font-semibold text-slate-100 mb-2 group-hover:text-primary-300 transition-colors">
                    {agent.name}
                </h3>

                {/* Description */}
                <p className="text-sm text-slate-400 leading-relaxed flex-1 line-clamp-3 mb-4">
                    {agent.description}
                </p>

                {/* Specialization */}
                {agent.specialization && (
                    <p className="text-xs text-slate-500 italic mb-4 line-clamp-1">
                        📍 {agent.specialization}
                    </p>
                )}

                {/* Footer stats */}
                <div className="flex items-center justify-between pt-4 border-t border-slate-700/50">
                    <div className="flex items-center gap-1.5 text-amber-400">
                        <RiFlashlightLine className="text-sm" />
                        <span className="text-sm font-bold">{agent.impact_score.toFixed(1)}</span>
                        <span className="text-xs text-slate-500 font-normal">impact</span>
                    </div>
                    <div className="flex items-center gap-3">
                        {agent.github_url && (
                            <a href={agent.github_url} target="_blank" rel="noopener noreferrer"
                                onClick={e => e.stopPropagation()}
                                className="text-slate-500 hover:text-slate-300 transition-colors">
                                <RiExternalLinkLine className="text-sm" />
                            </a>
                        )}
                        <span className="text-xs text-slate-600">{lastUpdated}</span>
                    </div>
                </div>
            </article>
        </Link>
    )
}
