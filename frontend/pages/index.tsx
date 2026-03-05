/**
 * CATALYST - Home Page (/)
 * Hero section, impact stats, featured agents, CTA
 */
import Head from 'next/head'
import Link from 'next/link'
import { useEffect, useState } from 'react'
import { RiRocketLine, RiBrainLine, RiArrowRightLine, RiGithubLine } from 'react-icons/ri'
import Navigation from '../components/Navigation'
import AgentCard from '../components/AgentCard'
import ImpactStats from '../components/ImpactStats'
import { fetchAgents, fetchImpactMetrics } from '../lib/api'
import type { Agent, ImpactMetrics } from '../lib/api'

const DEFAULT_METRICS: ImpactMetrics = {
    total_agents: 5, active_agents: 5, total_research: 142,
    total_impact_score: 2193.4, people_helped: 2193400,
    data_sources_connected: 6, countries_monitored: 12,
}

export default function Home() {
    const [agents, setAgents] = useState<Agent[]>([])
    const [metrics, setMetrics] = useState<ImpactMetrics>(DEFAULT_METRICS)

    useEffect(() => {
        fetchAgents().then(a => setAgents(a.slice(0, 6))).catch(() => { })
        fetchImpactMetrics().then(setMetrics).catch(() => { })
    }, [])

    return (
        <>
            <Head>
                <title>CATALYST — Universal AI Agent Research Platform</title>
                <meta name="description" content="Upload AI agents that solve real-world problems using live data. Track impact, collaborate, and make a difference." />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <div className="page-wrapper grid-pattern">
                <Navigation />

                {/* ── Hero ── */}
                <section className="relative pt-32 pb-24 px-4 overflow-hidden">
                    {/* Glowing orbs */}
                    <div className="absolute top-20 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl pointer-events-none" />
                    <div className="absolute top-40 right-1/4 w-80 h-80 bg-accent-500/10 rounded-full blur-3xl pointer-events-none" />

                    <div className="relative max-w-5xl mx-auto text-center">
                        {/* Label */}
                        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-primary-500/30
                            bg-primary-500/10 text-primary-300 text-sm font-medium mb-8 animate-fade-up">
                            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
                            Open-Source · 5 Live Agents · Real-World Impact
                        </div>

                        <h1 className="text-5xl sm:text-7xl font-black mb-6 leading-none animate-fade-up"
                            style={{ animationDelay: '0.1s' }}>
                            Where Problems
                            <br />
                            <span className="gradient-text">Get Solved.</span>
                        </h1>

                        <p className="text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed animate-fade-up"
                            style={{ animationDelay: '0.2s' }}>
                            CATALYST is an open-source platform where anyone can upload AI agents that analyze
                            live data, generate insights, and demonstrate measurable real-world impact.
                        </p>

                        <div className="flex flex-wrap gap-4 justify-center animate-fade-up" style={{ animationDelay: '0.3s' }}>
                            <Link href="/agents" className="btn-primary flex items-center gap-2 text-base">
                                Explore Agents <RiArrowRightLine />
                            </Link>
                            <Link href="/upload" className="btn-ghost flex items-center gap-2 text-base">
                                <RiRocketLine /> Upload Your Agent
                            </Link>
                        </div>
                    </div>
                </section>

                {/* ── Impact Stats ── */}
                <section className="max-w-6xl mx-auto px-4 pb-20">
                    <div className="text-center mb-10">
                        <p className="section-label mb-2">Live Impact</p>
                        <h2 className="text-3xl font-bold">Numbers that matter</h2>
                    </div>
                    <ImpactStats metrics={metrics} />
                </section>

                {/* ── Featured Agents ── */}
                <section className="max-w-6xl mx-auto px-4 pb-24">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <p className="section-label mb-1">Featured</p>
                            <h2 className="text-2xl font-bold">Active Research Agents</h2>
                        </div>
                        <Link href="/agents" className="btn-ghost text-sm flex items-center gap-1.5">
                            View All <RiArrowRightLine />
                        </Link>
                    </div>

                    {agents.length > 0 ? (
                        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
                            {agents.map(agent => <AgentCard key={agent.id} agent={agent} />)}
                        </div>
                    ) : (
                        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
                            {[...Array(3)].map((_, i) => (
                                <div key={i} className="card h-52 shimmer" />
                            ))}
                        </div>
                    )}
                </section>

                {/* ── CTA Banner ── */}
                <section className="max-w-6xl mx-auto px-4 pb-24">
                    <div className="relative rounded-3xl overflow-hidden p-10 text-center"
                        style={{
                            background: 'linear-gradient(135deg, rgba(59,130,246,0.15) 0%, rgba(168,85,247,0.15) 100%)',
                            border: '1px solid rgba(59,130,246,0.2)'
                        }}>
                        <div className="absolute inset-0 bg-gradient-radial from-primary-500/5 to-transparent" />
                        <div className="relative">
                            <RiBrainLine className="text-5xl mx-auto mb-4 gradient-text" />
                            <h2 className="text-3xl font-bold mb-3">Have an Agent Idea?</h2>
                            <p className="text-slate-400 mb-6 max-w-lg mx-auto">
                                Upload your AI agent to CATALYST and let it run research that helps real people.
                                All code is open-source and free to use.
                            </p>
                            <div className="flex flex-wrap gap-3 justify-center">
                                <Link href="/upload" className="btn-primary flex items-center gap-2">
                                    <RiRocketLine /> Upload an Agent
                                </Link>
                                <a href="https://github.com" target="_blank" rel="noopener noreferrer"
                                    className="btn-ghost flex items-center gap-2">
                                    <RiGithubLine /> View on GitHub
                                </a>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Footer */}
                <footer className="border-t border-slate-800/50 py-8 text-center text-slate-600 text-sm">
                    <p>CATALYST © 2024 · Open-Source · MIT License · Built for real-world impact</p>
                </footer>
            </div>
        </>
    )
}
