import { useEffect, useState, type FormEvent } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { getJson, postJson } from '@/lib/api'
import type { HelloMessage } from './types'

export function HelloPage() {
  const [messages, setMessages] = useState<HelloMessage[]>([])
  const [text, setText] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    getJson<HelloMessage[]>('/api/hello/messages')
      .then(setMessages)
      .catch((e: Error) => setError(e.message))
  }, [])

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    if (!text.trim()) return
    setSaving(true)
    try {
      const created = await postJson<HelloMessage>('/api/hello/messages', { text: text.trim() })
      setMessages((prev) => [created, ...prev])
      setText('')
      setError(null)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Hello messages</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <form onSubmit={onSubmit} className="flex gap-2">
          <Input
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Write a message…"
            maxLength={500}
          />
          <Button type="submit" disabled={saving || !text.trim()}>
            Add
          </Button>
        </form>
        {error && <p className="text-sm text-destructive">{error}</p>}
        <ul className="space-y-2">
          {messages.map((m) => (
            <li key={m.id} className="rounded-md border p-2 text-sm break-words">
              {m.text}
              <span className="ml-2 text-xs text-muted-foreground">
                {new Date(m.created_at).toLocaleString()}
              </span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}
