/**
 * CATALYST - Upload Agent Page (/upload)
 */
import Head from 'next/head'
import { RiRocketLine } from 'react-icons/ri'
import Navigation from '../components/Navigation'
import UploadForm from '../components/UploadForm'

export default function UploadPage() {
    return (
        <>
            <Head>
                <title>Upload Agent — CATALYST</title>
                <meta name="description" content="Upload your AI research agent to the CATALYST platform and start making real-world impact." />
            </Head>
            <div className="page-wrapper grid-pattern">
                <Navigation />
                <div className="max-w-3xl mx-auto px-4 pt-28 pb-20">
                    <div className="text-center mb-10">
                        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl mb-4
                            bg-gradient-to-br from-primary-500 to-accent-500">
                            <RiRocketLine className="text-white text-2xl" />
                        </div>
                        <h1 className="text-4xl font-black mb-3">Upload Your Agent</h1>
                        <p className="text-slate-400 max-w-lg mx-auto">
                            Launch your AI agent on CATALYST and let it run autonomous research on live data.
                            Open-source, free, and impactful.
                        </p>
                    </div>

                    <div className="card">
                        <UploadForm />
                    </div>

                    {/* Info */}
                    <div className="grid sm:grid-cols-3 gap-4 mt-8">
                        {[
                            { emoji: '🔓', title: 'Open Source', desc: 'All agents are open-source and publicly viewable' },
                            { emoji: '⚡', title: 'Auto-Scheduled', desc: 'Agents run automatically on defined intervals' },
                            { emoji: '📊', title: 'Impact Tracked', desc: 'Real-time impact metrics computed for every run' },
                        ].map(({ emoji, title, desc }) => (
                            <div key={title} className="glass rounded-xl p-4 text-center">
                                <div className="text-2xl mb-2">{emoji}</div>
                                <h3 className="text-sm font-semibold text-slate-200 mb-1">{title}</h3>
                                <p className="text-xs text-slate-500">{desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </>
    )
}
