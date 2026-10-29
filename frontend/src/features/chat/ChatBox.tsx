import { useState, type FormEvent } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { streamSSE } from '@/lib/api'
import { cn } from '@/lib/utils'
import type { ChatMessage } from './types'

export function ChatBox() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [streaming, setStreaming] = useState(false)

  function appendToReply(text: string) {
    setMessages((prev) => {
      const last = prev[prev.length - 1]
      return [...prev.slice(0, -1), { ...last, content: last.content + text }]
    })
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    if (!input.trim() || streaming) return
    const history: ChatMessage[] = [...messages, { role: 'user', content: input.trim() }]
    setMessages([...history, { role: 'assistant', content: '' }])
    setInput('')
    setStreaming(true)
    try {
      await streamSSE('/api/chat/stream', { messages: history }, (event) => {
        if (event.delta) appendToReply(event.delta)
        if (event.error) appendToReply(`\n[error: ${event.error}]`)
      })
    } catch (err) {
      appendToReply(`\n[error: ${(err as Error).message}]`)
    } finally {
      setStreaming(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Chat</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          {messages.length === 0 && (
            <p className="text-sm text-muted-foreground">Say hi to the assistant.</p>
          )}
          {messages.map((m, i) => (
            <div
              key={i}
              className={cn(
                'max-w-[85%] rounded-lg px-3 py-2 text-sm whitespace-pre-wrap break-words',
                m.role === 'user' ? 'ml-auto bg-primary text-primary-foreground' : 'bg-muted',
              )}
            >
              {m.content || '…'}
            </div>
          ))}
        </div>
        <form onSubmit={onSubmit} className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message…"
          />
          <Button type="submit" disabled={streaming || !input.trim()}>
            Send
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
