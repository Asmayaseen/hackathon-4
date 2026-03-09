'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { BookOpen, BarChart2, Search, Zap } from 'lucide-react'
import clsx from 'clsx'

const links = [
  { href: '/',           label: 'Home',     icon: Zap },
  { href: '/chapters',   label: 'Chapters', icon: BookOpen },
  { href: '/progress',   label: 'Progress', icon: BarChart2 },
  { href: '/search',     label: 'Search',   icon: Search },
]

export default function Navbar() {
  const path = usePathname()
  return (
    <nav className="sticky top-0 z-30 bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 font-bold text-brand-700 text-lg">
          <Zap size={20} className="text-brand-600" />
          Course Companion FTE
        </Link>
        <div className="flex items-center gap-1">
          {links.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={clsx(
                'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                path === href || (href !== '/' && path.startsWith(href))
                  ? 'bg-brand-50 text-brand-700'
                  : 'text-gray-600 hover:bg-gray-100',
              )}
            >
              <Icon size={15} />
              {label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}
