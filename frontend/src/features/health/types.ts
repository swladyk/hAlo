export type Health = {
  status: 'ok'
  db: 'ok' | 'error'
  llm: 'live' | 'mock'
}
