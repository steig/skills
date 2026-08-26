---
name: map-driven
description: Run Schema-Driven Development's completeness through a Wayfinder map — a ticket DAG where agents research the layers in parallel (AFK) and the human is grilled on one judgment per session (HITL), with a continuous validator that spawns tickets for what nobody thought to raise. The third skill of the family — schema-driven supplies WHAT must be decided, this skill supplies HOW and WHEN. Use when the user wants to "chart a map", "map-drive this", "wayfind the design", or is starting SDD-scale design work that is multi-session, sits on an existing codebase, or has agents available to parallelize. Refuses single-sitting-sized systems — those get plain schema-driven.
---

# Map-Driven Design

> The Wayfinder methodology this skill builds on — maps, question-tickets, plan-don't-build — is
> [Matt Pocock's `wayfinder` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/wayfinder)
> (MIT), as practiced and extended across two real maps; the grilling discipline is his
> `grilling`/`grill-me`. This skill is that execution model fused with schema-driven's
> completeness machinery.

The user is starting design work big enough that one interview sitting can't hold it: a system that needs schema-driven's 11-layer rigor, but across days, an existing codebase, or a fleet of agents. Instead of walking the layers in lockstep with a human present for all of it, chart a **map**: every unresolved design branch becomes a **ticket**, tickets are triaged by who can resolve them (agent research vs. live human judgment), dependency order becomes edges on a DAG, and a continuously-running validator spawns tickets for the gaps nobody thought to raise. The map plans; it doesn't build.

The division of labor with the siblings is exact: **`schema-driven` supplies the *what*** (the 11 layers, their prompts, tiered formalization, the cross-reference checks) and **`view-driven` supplies the frontend *what*** (archetypes, state floor, experience-layer decisions). **This skill supplies the *how* and *when*.** Read the sibling SKILL.mds for interview content when posing a ticket — never duplicate their layer definitions; the projections this skill owns (triage table, ticket templates, check list) are below.

## When NOT to do this

**Refuse or scope down** if the work is:

- **Small enough to spec in one sitting.** A single-service system whose design interview fits an afternoon gets plain `schema-driven` — the map's overhead (charting, triage, edges, log) buys nothing. This is the load-bearing boundary: when in doubt, ask "would the interview outlast this session?" and only chart if yes.
- Anything `schema-driven` itself refuses (discovery-phase products, simple CRUD, prototypes, UI-complexity-only work) — the map inherits SDD's refusals wholesale.
- **Mid-flight work on an existing map** — pick up the frontier; don't re-chart.

## The map: two halves (split-by-role backing)

- **Execution state lives in GitHub issues:** one map issue (label `wayfinder:map`) whose sub-issues are the tickets; native `blocked-by`/`blocking` edges; ticket types as labels (`wayfinder:research`, `wayfinder:grilling`, `wayfinder:task`, `wayfinder:prototype`); a `provisional` label on below-frontier tickets.
- **Decision state lives in one in-repo file per map:** `docs/wayfinder/<map>.md` — the **append-only decisions log** (dated one-liner per resolution event; corrections are new lines, never rewrites) plus the **measured-facts cache** ("do not re-derive"). This file is canonical: every resolution is recorded **twice** — full closing comment on the ticket *and* one log line. A closed ticket with no log line is a skipped resolution, and the validator flags it.
- **Fallback (no GitHub):** everything collapses into the one markdown file, with an explicit `blocked-by:` line per ticket (prose "→ informs" covers only soft edges). All protocol rules hold identically.

Ticket types: **research** (agent-resolvable from code/docs/measurement; prescribe the output doc: "Record in `docs/research/X.md`, following Y for shape", plus do-not-decide guardrails), **grilling** (needs the live human), **task** (mechanical map upkeep), **prototype** (research whose evidence requires *running code* — a throwaway spike; same rules as research, plus: the spike is evidence, never a deliverable, and is discarded after the facts are logged).

## Lifecycle

### 1. Charting — one sitting, always

Write the map issue: **Destination** (done-when, in one paragraph), **out of scope**, **Settled at charting** (constraints carried in — from a prior grill, the codebase, or the user's brief), and file **one research ticket: "seed the map."** Charting never walks the layers itself — that's the seeder's job. Then ask the two SDD scoping questions (package dimension; "does this have a frontend?" — no frontend means no V-rows) and stop.

### 2. Seeding — the validator's first run

The seeder **is** the validator (one machine): its *coverage check* — "every layer the tiered-formalization rules require has a ticket or a resolution" — fails everywhere on an empty map and auto-spawns the full ticket set from the triage table and templates below. Big-bang: the whole frontier is visible on day one, AFK research fans out immediately. Every ticket below the frontier carries the `provisional` marker.

### 3. Frontier work

- **Re-pose at pickup:** whoever picks up a ticket — agent or grill session — first re-derives its Question against the current trunk and resolved tickets. If a redraw invalidated it, edit the body (bodies are mutable pre-resolution; only the log is append-only), then answer. This makes redraw propagation lazy and safe.
- **One HITL ticket per session; AFK exempt.** Research tickets run in parallel, as many as there are agents. The human's session resolves exactly one grilling ticket. Grill it the way the siblings do: **one question per turn, always** — tradeoffs visible, a recommendation to react to, never a bundle of questions.
- **Resolutions:** headline first, options rejected with reasons, "→ informs / unblocks" named. Closing comment + log line, both.

### 4. Redraw

When a settled constraint must change: **in-place dated edit preserving the original text** (*"Redrawn YYYY-MM-DD; originally …"*), with the rationale, a reversibility argument, and fan-out — a comment on every open ticket that cited the redrawn decision, plus a log line. Seeded tickets need no immediate touch-up; re-pose-at-pickup catches them.

### 5. Validator — continuous, maturity-gated, auto-spawning

Runs on **every log append**. Each check **arms** only once every layer it reads from has no open tickets (kills early-map noise). A failure **auto-spawns a ticket**, triaged by the table below; the human veto is closing it **with a written deferral reason**, which lands in the log. Nothing is silently declinable.

**Checks:** all of `schema-driven`'s cross-reference checks, verbatim (read them from the sibling — orphans, dangling events, toolless transitions, permission gaps, duplicate ownership, PII erasure-reachability *with membership asserted both ways*, and the rest), **plus the map-level checks:** coverage (= the seeder), closed-ticket-without-log-line, prescribed-research-doc-never-landed, provisional-field staleness, every blocked-by chain terminates.

### 6. Frontier clear and handoff

**Eligibility is mechanical:** every ticket resolved or closed-with-written-reason, validator green (all armed checks passing), deferred list written. **Declaration is human** — a HITL act in a session; the map never closes itself on a technicality. The declaration session appends the terminal log entry — SDD's closing synthesis (entities, packages, services, high-risk transitions, PII coverage, deferred items) — and **offers** to generate the SDD JSON artifacts. Never auto-generate. The **deferred list** (validator deferrals + defer-resolutions + charting's out-of-scope) is signed off here.

**The map ends there.** "Does this need an ARD?" is a late-gated research ticket on the map (three-criteria test: hard to reverse · surprising without context · real trade-off — checkable against the map's own contents); *writing* the ARD, spec changes, generation, build, and gates all belong to the project's own tooling, downstream.

## Triage table (the projection this skill owns)

Defaults assume the scope guard: multi-session work on an existing codebase. Greenfield flips most AFK rows to HITL.

| # | Layer / decision | Default | What flips it |
|---|---|---|---|
| P | Package dimension | **HITL** (DAG root) | → derived when charter/codebase fixes it — record `core`, no ticket |
| 1 | Ontology | **AFK** — reverse-engineer models; deltas only | → HITL greenfield; HITL for ambiguous PII tagging |
| 2 | State machines | **AFK** — enums + transition code | → HITL for new lifecycles or unstated business guards |
| 3 | Event catalog | **AFK** — producers/consumers readable | → HITL for envelope/versioning strategy, new-feature events |
| 4 | Tool registry | **AFK**; safety/approval gates derived by rule | → gate *overrides* are HITL but owned by the layer-11 ticket |
| 5 | Workflows | **AFK** — orchestration code | → HITL for unimplemented compensation semantics |
| 6 | Data ownership | **HITL** — seeded by an AFK as-is map | → derived single-service; duplicate ownership found → escalate now |
| 7 | C4 | **AFK** — ownership + deploy configs | → derived when unambiguous; HITL for re-architecture |
| 8 | Roles & policies | **HITL** — semantics are policy; inventory AFK-seeded | → AFK for pure transcription; audit-grade on consumer PII |
| 9 | Compliance | **HITL-formal** — AFK PII scan triggers it | → derived stub only if scan clean AND unregulated |
| 10 | Integrations | **AFK** — connectors readable | → HITL for new protocol/partner; PII-outbound escalates to compliance |
| 11 | Verification | **derived** — scaffold generates; no ticket | → HITL for LM-judge rubrics, gate overrides, golden-trajectory picks (agent-executed only) |
| V1 | Kit | **HITL, one early ticket, repo-read default seeded** | flip is depth: greenfield = full interview; existing stack = confirm |
| V2 | Nav classification | **HITL** — one batched confirm of the derived proposal | structurally forced entities excluded |
| V3 | State waivers | **post-validator HITL only** — universal-6 is fix-only, never waivable | never AFK: an agent writing its own waiver defeats the mechanism |
| V4 | Archetype overrides | **derived** | → HITL per exception, on request |

Ticket Question shapes seed verbatim from the siblings' layer prompts (read them at posing time); hard `blocked-by` edges follow SDD's dependency order (Package at the root); two-way references (tools↔roles, ownership↔C4) resolve by leaving a **provisional field** the validator later reconciles — hard edges never point forward.

**Escalation, both directions.** AFK→HITL (*prescriptive — the exemplars attest the wiring, not the genesis*): an agent whose question turns contested — a real trade-off, hard to reverse, surprising facts — finishes only the measurable part, births a grilling ticket carrying the options with measured costs, wires it `blocked-by` its research. The tell: the agent is *reframing* the question instead of *measuring* it. HITL→AFK: a grilling ticket answerable from the codebase is relabeled research and resolved as fact; only the remaining delta stays HITL. Validator-spawned fixes triage by the table; a defer-with-reason is always HITL.

## Anti-patterns

- **Charting a map for an afternoon's system.** The scope guard is the point — send it to `schema-driven`.
- **Walking the layers during charting.** Charting writes the destination and one seed ticket; the seeder walks.
- **Duplicating the siblings' layer content.** Interview prompts, formalization tiers, archetype contracts live in `schema-driven`/`view-driven` — read them; only the projections above are owned here.
- **Answering a stale question.** Picking up a ticket without re-posing it against the current trunk resolves a question from a world that no longer exists.
- **Resolving in one place.** Closing comment without a log line (or vice versa) is a half-resolution; the herdrmux exemplar drifted exactly here and lost three answers.
- **Batch-grilling.** More than one HITL ticket per session, or more than one question per turn, trades answer quality for speed — the map exists so you never have to.
- **A proposal queue.** Validator findings that "propose" instead of spawning are silently declinable — the hole the validator exists to close.
- **Deciding in a research ticket.** Evidence and judgment are separate tickets; guardrail every research body with an explicit do-not-decide line.
- **Auto-generating the JSONs at frontier clear.** Offer; don't impose — the user may feed the log into their own tooling.

## Example exchange

User: "Let's design the multi-warehouse inventory platform properly — this'll take a few weeks."

Bad: "Great, layer 1: what entities does the system manage?"

Better: "Multi-week and there's an existing codebase — that's map territory, not a single interview. Charting takes one sitting: I'll write the destination and out-of-scope from what you've told me, carry in the constraints we've already settled, and file the seed ticket — agents will walk the 11 layers against the code and file the full ticket set with edges, most of it research they resolve themselves. You'll get grilled on the short list that's genuinely yours: ownership, permission semantics, compliance posture, one question at a time, one ticket per session.

One scoping question first: **single package, or are 3PL and retail-DC genuinely different products?** I'd default to one `core` package — pre-engineering verticals is the architecture-astronaut trap. Which is it?"
