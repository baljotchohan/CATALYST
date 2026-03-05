/**
 * CATALYST - Navigation Component
 */
import Link from 'next/link'
import { useRouter } from 'next/router'
import { useState } from 'react'
import { RiRocketLine, RiBrainLine, RiMenuLine, RiCloseLine } from 'react-icons/ri'

const NAV_LINKS = [
    { href: '/agents', label: 'Agents' },
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/upload', label: 'Upload' },
]

export default function Navigation() {
    const router = useRouter()
    const [open, setOpen] = useState(false)

    return (
        <nav className="fixed top-0 inset-x-0 z-50 glass border-b border-slate-800/50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">

                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-2.5 group">
                        <div className="w-8 h-8 rounded-lg flex items-center justify-center
                            bg-gradient-to-br from-primary-500 to-accent-500
                            group-hover:shadow-glow-blue transition-shadow duration-300">
                            <RiBrainLine className="text-white text-lg" />
                        </div>
                        <span className="font-bold text-lg tracking-tight">
                            <span className="gradient-text">CATALYST</span>
                        </span>
                    </Link>

                    {/* Desktop links */}
                    <div className="hidden md:flex items-center gap-1">
                        {NAV_LINKS.map(({ href, label }) => {
                            const active = router.pathname.startsWith(href)
                            return (
                                <Link key={href} href={href}
                                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200
                    ${active
                                            ? 'bg-primary-500/20 text-primary-300'
                                            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'}`}>
                                    {label}
                                </Link>
                            )
                        })}
                    </div>

                    {/* CTA */}
                    <div className="hidden md:flex items-center gap-3">
                        <Link href="/upload" className="btn-primary text-sm py-2">
                            <RiRocketLine className="inline-block mr-1.5 -mt-0.5" />
                            Upload Agent
                        </Link>
                    </div>

                    {/* Mobile menu toggle */}
                    <button onClick={() => setOpen(!open)}
                        className="md:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors">
                        {open ? <RiCloseLine size={22} /> : <RiMenuLine size={22} />}
                    </button>
                </div>
            </div>

            {/* Mobile menu */}
            {open && (
                <div className="md:hidden border-t border-slate-800/50 py-2 px-4 space-y-1">
                    {NAV_LINKS.map(({ href, label }) => (
                        <Link key={href} href={href}
                            onClick={() => setOpen(false)}
                            className="block px-4 py-2.5 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800">
                            {label}
                        </Link>
                    ))}
                    <div className="pt-2 pb-1">
                        <Link href="/upload" onClick={() => setOpen(false)} className="btn-primary text-sm block text-center">
                            Upload Agent
                        </Link>
                    </div>
                </div>
            )}
        </nav>
    )
}
