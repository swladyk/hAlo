import { useEffect, useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { getJson } from '@/lib/api'
import type { Health } from './types'

function StatusBadge({ label, ok, text }: { label: string; ok: boolean; text: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-muted-foreground">{label}</span>
      <Badge
        variant={ok ? 'default' : 'destructive'}
        className={ok ? 'bg-green-600 text-white' : undefined}
      >
        {text}
      </Badge>
    </div>
  )
}

export function HealthCard() {
  const [health, setHealth] = useState<Health | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    getJson<Health>('/api/health')
      .then(setHealth)
      .catch(() => setError(true))
  }, [])

  const loading = !health && !error
  return (
    <Card>
      <CardHeader>
        <CardTitle>System status</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-wrap gap-4">
        {loading ? (
          <span className="text-sm text-muted-foreground">Checking… (the backend may be waking up)</span>
        ) : (
          <>
            <StatusBadge label="Backend" ok={!error} text={error ? 'down' : 'ok'} />
            <StatusBadge label="DB" ok={health?.db === 'ok'} text={health?.db ?? 'unknown'} />
            <StatusBadge label="LLM" ok={!!health} text={health?.llm ?? 'unknown'} />
          </>
        )}
      </CardContent>
    </Card>
  )
}
