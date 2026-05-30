import { ReactNode } from 'react'

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="app-layout">
      <main className="main-content">{children}</main>
    </div>
  )
}
