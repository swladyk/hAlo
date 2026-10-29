import { ChatBox } from '@/features/chat/ChatBox'
import { HealthCard } from '@/features/health/HealthCard'
import { HelloPage } from '@/features/hello/HelloPage'

// Layout only. One line per feature.
export default function App() {
  return (
    <main className="mx-auto max-w-2xl space-y-4 p-4">
      <h1 className="text-2xl font-semibold">hAlo</h1>
      <HealthCard />
      <HelloPage />
      <ChatBox />
    </main>
  )
}
