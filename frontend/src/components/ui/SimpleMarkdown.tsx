'use client'
/**
 * Lightweight Markdown renderer — no external deps.
 * Handles: headings, bold, code blocks, inline code, lists, paragraphs.
 */
export default function SimpleMarkdown({ content }: { content: string }) {
  const lines = content.split('\n')
  const elements: React.ReactNode[] = []
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    // Code block
    if (line.startsWith('```')) {
      const codeLines: string[] = []
      i++
      while (i < lines.length && !lines[i].startsWith('```')) {
        codeLines.push(lines[i])
        i++
      }
      elements.push(
        <pre key={i}><code>{codeLines.join('\n')}</code></pre>
      )
      i++
      continue
    }

    // Headings
    if (line.startsWith('### ')) {
      elements.push(<h3 key={i}>{inline(line.slice(4))}</h3>)
    } else if (line.startsWith('## ')) {
      elements.push(<h2 key={i}>{inline(line.slice(3))}</h2>)
    } else if (line.startsWith('# ')) {
      elements.push(<h1 key={i}>{inline(line.slice(2))}</h1>)
    }
    // Unordered list
    else if (line.match(/^[-*] /)) {
      const items: string[] = []
      while (i < lines.length && lines[i].match(/^[-*] /)) {
        items.push(lines[i].replace(/^[-*] /, ''))
        i++
      }
      elements.push(
        <ul key={i}>
          {items.map((item, idx) => <li key={idx}>{inline(item)}</li>)}
        </ul>
      )
      continue
    }
    // Ordered list
    else if (line.match(/^\d+\. /)) {
      const items: string[] = []
      while (i < lines.length && lines[i].match(/^\d+\. /)) {
        items.push(lines[i].replace(/^\d+\. /, ''))
        i++
      }
      elements.push(
        <ol key={i}>
          {items.map((item, idx) => <li key={idx}>{inline(item)}</li>)}
        </ol>
      )
      continue
    }
    // Paragraph
    else if (line.trim()) {
      elements.push(<p key={i}>{inline(line)}</p>)
    }

    i++
  }

  return <div className="prose-chapter">{elements}</div>
}

function inline(text: string): React.ReactNode {
  // Split on **bold**, `code`
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={i}>{part.slice(1, -1)}</code>
    }
    return part
  })
}
