'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { BookOpen, BarChart2, Search, Zap, Sparkles, LayoutDashboard, Shield, CreditCard } from 'lucide-react'
import clsx from 'clsx'

const links = [
  { href: '/',           label: 'Home',      icon: Zap,             pro: false, admin: false },
  { href: '/dashboard',  label: 'Dashboard', icon: LayoutDashboard, pro: false, admin: false },
  { href: '/chapters',   label: 'Chapters',  icon: BookOpen,        pro: false, admin: false },
  { href: '/progress',   label: 'Progress',  icon: BarChart2,       pro: false, admin: false },
  { href: '/search',     label: 'Search',    icon: Search,          pro: false, admin: false },
  { href: '/synthesis',  label: 'Synthesis', icon: Sparkles,        pro: true,  admin: false },
  { href: '/upgrade',    label: 'Pricing',   icon: CreditCard,      pro: false, admin: false },
  { href: '/admin',      label: 'Admin',     icon: Shield,          pro: false, admin: true  },
]

export default function Navbar() {
  const path = usePathname()
  return (
    <nav className="sticky top-0 z-30 bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 font-bold text-brand-700 text-lg shrink-0">
          <Zap size={20} className="text-brand-600" />
          <span className="hidden sm:inline">Course Companion FTE</span>
          <span className="sm:hidden">CC FTE</span>
        </Link>
        <div className="flex items-center gap-0.5 overflow-x-auto">
          {links.map(({ href, label, icon: Icon, pro, admin }) => (
            <Link
              key={href}
              href={href}
              className={clsx(
                'flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
                path === href || (href !== '/' && path.startsWith(href))
                  ? 'bg-brand-50 text-brand-700'
                  : admin
                    ? 'text-gray-400 hover:bg-gray-100'
                    : 'text-gray-600 hover:bg-gray-100',
              )}
            >
              <Icon size={14} />
              <span className="hidden md:inline">{label}</span>
              {pro && <span className="text-xs px-1 py-0.5 rounded bg-amber-100 text-amber-700 font-semibold hidden md:inline">Pro</span>}
              {admin && <span className="text-xs px-1 py-0.5 rounded bg-gray-100 text-gray-500 font-semibold hidden md:inline">P3</span>}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}
