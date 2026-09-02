/*
 * Export a claude.ai conversation to a markdown transcript.
 *
 * There is no public API for claude.ai chat history, so this runs against the
 * web app's own endpoints using the browser's logged-in session.
 *
 * Usage:
 *   1. Open https://claude.ai in a tab where you are signed in.
 *   2. Paste this whole file into the DevTools console (or have Claude Code run
 *      it via the Chrome extension's javascript_tool).
 *   3. Set MATCH below to a substring of the chat title, or to its uuid.
 *   4. The transcript downloads as <slug>.md; move it into docs/chat-exports/.
 *
 * Notes:
 *   - `thinking` blocks are dropped; text, tool calls and tool results are kept.
 *   - Non-code tool inputs are JSON-dumped and clipped at MAX_INPUT chars, so
 *     very large str_replace payloads come out truncated.
 *   - present_files results carry signed URLs; sandbox files must still be
 *     downloaded by hand from the chat UI.
 */

const MATCH = 'simple enough';   // substring of the chat title, or a uuid
const MAX_INPUT = 4000;          // clip for JSON-dumped tool inputs
const MAX_RESULT = 2000;         // clip for tool results

const json = (url) =>
  fetch(url, { headers: { accept: 'application/json' } }).then((r) => r.json());

const [org] = await json('/api/organizations');
const convos = await json(
  `/api/organizations/${org.uuid}/chat_conversations?limit=100`
);

const hit = convos.find((c) => c.uuid === MATCH || c.name.includes(MATCH));
if (!hit) throw new Error(`no conversation matching ${MATCH}`);

const conv = await json(
  `/api/organizations/${org.uuid}/chat_conversations/${hit.uuid}` +
    '?tree=True&rendering_mode=messages&render_all_tools=true'
);

const out = [
  `# ${conv.name}\n`,
  `- conversation: \`${conv.uuid}\``,
  `- project: \`${conv.project_uuid || ''}\``,
  `- created: ${conv.created_at}`,
  `- updated: ${conv.updated_at}`,
  `- model: ${conv.model || ''}`,
  `\n---\n`,
];

for (const m of conv.chat_messages || []) {
  out.push(`\n## ${m.sender === 'human' ? 'User' : 'Assistant'} — ${m.created_at}\n`);

  for (const b of m.content || []) {
    if (b.type === 'thinking') continue;

    if (b.type === 'text') {
      out.push(String(b.text ?? '').trim() + '\n');
    } else if (b.type === 'tool_use') {
      const input = b.input || {};
      const code = input.code ?? input.content ?? null;
      out.push(`\n<!-- tool_use: ${b.name} -->`);
      out.push(
        code !== null
          ? '```' + (b.name === 'repl' ? 'javascript' : '') + '\n' + code + '\n```\n'
          : '```json\n' + JSON.stringify(input, null, 1).slice(0, MAX_INPUT) + '\n```\n'
      );
    } else if (b.type === 'tool_result') {
      const text = (b.content || [])
        .filter((x) => x.type === 'text')
        .map((x) => String(x.text ?? ''))
        .join('\n');
      if (text.trim()) {
        out.push(
          `\n<!-- tool_result: ${b.name || ''} -->\n> ` +
            text.slice(0, MAX_RESULT).replace(/\n/g, '\n> ') +
            '\n'
        );
      }
    }
  }
}

const md = out.join('\n');
const a = document.createElement('a');
a.href = URL.createObjectURL(new Blob([md], { type: 'text/markdown' }));
a.download = conv.name.replace(/[^\w-]+/g, '-').replace(/^-+|-+$/g, '').toLowerCase() + '.md';
document.body.appendChild(a);
a.click();
a.remove();

({ name: conv.name, messages: (conv.chat_messages || []).length, chars: md.length });
