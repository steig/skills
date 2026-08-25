# Claude Code session messaging: ListAgents / SendMessage facts

Research for [steig/skills#3](https://github.com/steig/skills/issues/3) (child of map #1, fleet-coordinator skill).
Date: 2026-08-24. Sources: official Claude Code docs (primary: [cross-session-messaging](https://code.claude.com/docs/en/cross-session-messaging.md), [tools-reference](https://code.claude.com/docs/en/tools-reference.md), [agent-teams](https://code.claude.com/docs/en/agent-teams.md)), the in-product `SendMessage` tool schema, and one controlled probe on this machine (a send to a deliberately nonexistent name — no live session was touched).

## Summary: what gates the fixed-slot report protocol

- Messages **enqueue and deliver between the receiver's tool calls** — a running tool is never interrupted; an idle receiver starts a new turn with the message. Delivered messages land in the receiver's transcript wrapped/attributed to the sender.
- **Replies are not automatic.** The receiver must itself call `SendMessage` back (copy the incoming `from` as `to`). Cross-machine sends without Remote Control have **no reply address** at all.
- **Names are the address** (user-set via `/rename`/`--name`, else auto-generated); conflicts are auto-resolved by renaming the newcomer to a variant; ambiguous names get short `[ref]` identifiers in listings.
- **Unknown/closed target is a soft failure** returned to the sender (verified by probe), not an exception.
- **Delivery ≠ read**: the receiver's `crossSessionInbound` setting (accept / hold / refuse) or the permission-mode default can hold a message for human approval (5-minute dialog expiry by default) or drop it silently.
- **Received messages cannot approve anything, change config, or run slash commands**; any resulting tool use runs under the *receiver's* permissions and can prompt the receiver's user.
- Format: **plain text only**, ~1M-char size cap (refused at sender), burst rate limiting, inbox holds max 100 held messages (oldest dropped), `summary` ≤ 200 chars, `to` ≤ 300 chars.
- Requires Claude Code v2.1.224+ (`notify_when_idle` v2.1.236+).

## 1. Delivery semantics

Docs ([cross-session-messaging](https://code.claude.com/docs/en/cross-session-messaging.md)):

> "The receiving Claude reads the message between tool calls during an active turn, so a running tool is never interrupted. When the receiving session is idle, Claude Code starts a new turn with the message."

- Queued, not interrupting. The delivered message "appears in the conversation under the sender's session name and stays there," and "counts toward usage like a prompt you type."
- SendMessage schema (verbatim): "messages enqueue and drain at the receiver's next tool round … Your message arrives wrapped as `<cross-session-message from=\"...\">`."
- Sender gets a synchronous tool result for the send (accept/refuse); it does not block awaiting a reply. Docs do not specify delivery-vs-send acknowledgment granularity, ordering guarantees, or latency (see gaps).

## 2. Busy vs idle targets

- Idle receiver: a new turn starts immediately with the message. Busy receiver: message lands between tool calls of the current turn.
- `ListAgents` rows state busy/idle per session (SendMessage schema).
- Waiting on a busy session: `notify_when_idle: true` — one-shot, opt-in, same-machine, **main-conversation only**. Exactly one `[Cross-session idle notice]` arrives when the target next goes idle (finishes its turn with nothing queued) or exits. "If no notice arrives within 12 hours, Claude Code drops the subscription and tells Claude" (docs, v2.1.236+). Omit `message` for a pure subscription; include one to deliver now AND subscribe.
- Explicit anti-pattern in the schema: "Never poll `ListAgents` in a loop or send 'are you done?' messages instead."

## 3. Replies

- Same mechanism both ways: "the receiving Claude can reply to the sender the same way" (docs). Schema: "To reply to an incoming message, copy its `from` attribute as your `to`." Incoming replies are delivered automatically — "you don't check an inbox."
- Plain assistant text output is never visible to other agents; only SendMessage communicates.
- **Cross-machine caveat**: "If this session isn't connected to Remote Control when Claude sends to a session beyond this machine, the message still goes through, but without a reply address, so the receiving Claude can't answer it" (docs).
- When a message is held for approval on the receiving side, an interactive same-machine sender sees a notice, then "a follow-up when the receiver later delivers, denies, or expires it" (docs).

## 4. Naming / addressing

- Names come from `/rename`, the `--name` CLI flag, or are auto-generated. `/list-agents` (alias `/peers`) shows this session's own name first, then all reachable agents — subagents, teammates, local sessions, cloud sessions, Remote Control sessions (docs).
- "The name IS the address; there is no separate address syntax" (schema). Bare name delivers when it uniquely matches one live agent/session on this machine, another machine, or the cloud.
- **Conflict handling**: starting/renaming a session to a taken name → "Claude Code leaves the name with the session that already has it and renames yours to a variant" (docs). Where sessions still share a name (or not everywhere could be checked), listings add a short identifier per row and the address uses it — the `[ref]` suffix. "A ref you did not just read from a listing or an error will not resolve" (schema). Local listings also show each session's working directory to tell same-named sessions apart.
- In-process precedence: a subagent with the same name always beats a cross-session peer for the bare name; for completed background agents "names keep working … (a send resumes it from its transcript)"; duplicated background names: latest wins (schema).
- `@`-mention in the prompt (v2.1.232+) routes through SendMessage.
- Cloud-session listing overflow: "If your account has more of those sessions than fit, Claude Code doesn't list the older ones, and Claude can't message them by name" (docs).

## 5. Closed / renamed / unknown targets

- **Probed on this machine** (nonexistent name): soft failure returned to the sender —

  ```json
  {"success": false, "message": "No agent named 'wayfinder-probe-target-that-does-not-exist-7f3a' is reachable.\nCheck the spelling, or use the agent ID from a background agent's spawn result."}
  ```

  No exception, nothing delivered. An exited session stops being listed and its name stops resolving the same way.
- Docs list the sender-side refusal cases: message over the size cap; rapid burst exceeding the target inbox; "the reply target on this machine fails a safety check, such as a symlinked target or an endpoint that isn't the expected process"; addressing this session's own name.
- Renames: delivery follows filesystem state, so a queued message follows the current name; a stale old name either fails as above or resolves to whichever live agent now holds it (latest wins). The 12-hour idle-notice expiry also covers targets that "ended abruptly."

## 6. Permissions on the receiving side

- **A message is never consent** (docs): the receiving Claude is told the message came from another session, and "It can't approve anything … It can't change configuration … Commands don't run: a command in the message's text, such as `/compact`, arrives as plain text."
- **Permission prompts still fire**: "if acting on the message requires a permission the receiving session doesn't have, you see the same prompt you'd see for any other work" (docs). Schema adds the policy edge: never ask a peer to do what your session was denied — "cross-session permission laundering."
- **Inbound control** — `crossSessionInbound` setting: `accept` (deliver all), `hold` (approval dialog), `refuse` (drop silently). Default when unset is decided per message from the two sessions' permission modes: sessions bypassing permission prompts form one trust class; a normal receiving session holds only messages from bypass-mode senders (docs).
- Held messages open an approval dialog (sender + preview); deny/dismiss drops it; unanswered past `dialogExpiry` (default **5 minutes**) it's dropped (docs).
- `isolatePeerMachines: true` requires explicit user approval before any SendMessage leaves the machine, even in `bypassPermissions` mode (docs).
- Opt out entirely: permission **deny rules** naming bare `SendMessage` and `ListAgents` (docs).
- Observed here: subagents get `SendMessage` but **not** `ListAgents`, and `notify_when_idle` is main-conversation-only — discovery and idle subscription are capabilities of the main conversation.

## 7. Size / format constraints

| Constraint | Value | Source |
|---|---|---|
| Content type | Plain text only — "never conversation history or files" | docs |
| Same-machine size cap | ~1,000,000 chars serialized; refused at sender, refusal names exact sizes | docs |
| Burst limit | Rapid bursts to one session refused at sender once the target inbox is full; refusal says to batch or wait | docs |
| Held-inbox depth | Max 100 messages held; past that oldest dropped | docs |
| `summary` | ≤ 200 chars, 5–10-word preview, defaults to message's first line, truncated not rejected (v2.1.224+) | tools-reference + schema |
| `to` | ≤ 300 chars, no newlines | schema |

No attachments, no structured payloads — a fixed-slot report must serialize into plain text (e.g. labeled `SLOT: value` lines), and the first line should carry meaning (it becomes the default summary preview).

## 8. Documented gaps (docs are silent)

FIFO ordering across bursts; delivery latency; delivered-vs-sent acknowledgment granularity; automatic retry after refusal (none implied — sender must decide); message timestamps in transcript; token cost beyond "counts like a typed prompt"; dedup scope ("drops identical repeats arriving within a short window" is mentioned for loops only); not available on Bedrock / Vertex / Foundry.

## Implications for the fixed-slot report protocol

1. **Push, don't poll.** Worker sends its report on completion; coordinator arms `notify_when_idle` per worker as a liveness backstop (one-shot — re-arm after each notice; 12-hour expiry is the outer bound).
2. **Check every send result.** Unreachable target, size cap, and burst refusals are all soft failures at the sender; the protocol needs handling (re-list for fresh refs, batch messages, split oversized reports).
3. **Reports are plain text.** Line-oriented fixed slots; meaningful first line (default preview); parseable from within the `<cross-session-message>` wrapper.
4. **Names are protocol state.** Auto-variant renaming on collision means a coordinator must read back actual names from listings rather than assume assigned names stuck; refresh `[ref]`s from a live listing before disambiguated sends.
5. **Delivery ≠ read.** `hold` mode and the bypass-sender default can park a report in a 5-minute approval dialog or drop it; `refuse` drops silently. A coordinator run under bypassPermissions will have its messages *held* at normal-mode receivers by default.
6. **Coordinator must live in the main conversation.** Subagents lack ListAgents and `notify_when_idle`; only the main session can discover peers and subscribe to idleness.
7. **No permission laundering.** Never route a denied action to a worker.
