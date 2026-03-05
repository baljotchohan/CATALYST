/**
 * CATALYST - Impact Stats Component
 * Animated counter for big-number impact metrics
 */
import { useEffect, useRef, useState } from 'react'
import { RiBrainLine, RiSearchLine, RiGroupLine, RiGlobalLine } from 'react-icons/ri'
import type { ImpactMetrics } from '../lib/api'

function useCountUp(target: number, duration = 2000) {
    const [count, setCount] = useState(0)
    const ref = useRef<NodeJS.Timeout | null>(null)

    useEffect(() => {
        if (!target) return
        const startTime = Date.now()
        const animate = () => {
            const elapsed = Date.now() - startTime
            const progress = Math.min(elapsed / duration, 1)
            // Ease-out cubic
            const eased = 1 - Math.pow(1 - progress, 3)
            setCount(Math.floor(target * eased))
            if (progress < 1) ref.current = setTimeout(animate, 16)
        }
        animate()
        return () => { if (ref.current) clearTimeout(ref.current) }
    }, [target, duration])

    return count
}

function formatNumber(n: number): string {
    if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`
    if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
    return n.toLocaleString()
}

interface StatCardProps {
    icon: React.ReactNode
    label: string
    value: number
    suffix?: string
    color: string
}

function StatCard({ icon, label, value, suffix = '', color }: StatCardProps) {
    const count = useCountUp(value)
    return (
        <div className="glass rounded-2xl p-6 flex flex-col gap-2 hover:border-primary-500/30 transition-all duration-300">
            <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-xl ${color}`}>
                {icon}
            </div>
            <div className="flex items-end gap-1 mt-1">
                <span className="text-3xl font-black text-white">{formatNumber(count)}</span>
                {suffix && <span className="text-lg font-semibold text-slate-400 pb-0.5">{suffix}</span>}
            </div>
            <span className="text-sm text-slate-400">{label}</span>
        </div>
    )
}

interface ImpactStatsProps {
    metrics: ImpactMetrics
}

export default function ImpactStats({ metrics }: ImpactStatsProps) {
    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard
                icon={<RiBrainLine />}
                label="Active Agents"
                value={metrics.total_agents}
                color="bg-primary-500/20 text-primary-400"
            />
            <StatCard
                icon={<RiSearchLine />}
                label="Research Runs"
                value={metrics.total_research}
                color="bg-accent-500/20 text-accent-400"
            />
            <StatCard
                icon={<RiGroupLine />}
                label="People Helped"
                value={metrics.people_helped}
                color="bg-emerald-500/20 text-emerald-400"
            />
            <StatCard
                icon={<RiGlobalLine />}
                label="Countries Monitored"
                value={metrics.countries_monitored}
                color="bg-amber-500/20 text-amber-400"
            />
        </div>
    )
}
