# Per-layer HITL/AFK triage table and ticket templates

Resolves steig/skills#25, feeding the `schema-mapped` skill (map: steig/skills#20).
Derived from `skills/schema-driven/SKILL.md` (tiered formalization, "if the answer is
in the codebase, go find it", layer prompts, dependency order) and
`skills/view-driven/SKILL.md` (derive-first table, experience-layer-only interview).
Escalation wiring modeled on steig/herdrmux #10 ← #17 (see §Escalation for what that
pair does and does not attest).

## Triage vocabulary

- **HITL** — needs a live human; the answer is a judgment, trade-off, or business fact
  not recoverable from any artifact. One HITL ticket per session (map constraint 3).
- **AFK** — an agent can resolve it by reading the codebase, configs, git history, or
  external docs, and recording facts. No human in the loop.
- **derived** — falls out of already-pinned layers by rule; **never becomes a ticket**.
  Generating a ticket for a derivable answer is the hybrid's cardinal sin (SDD:
  "defer derived artifacts"; VDD's derive-first table: "Derived for free — never
  interview").

The table assumes the hybrid's own scope guard: multi-session work on an **existing
codebase** (or agent-parallel greenfield past charter). Pure greenfield flips most AFK
rows to HITL — that is the single biggest flip condition and is listed only where the
flip is not the generic "no code to read."

## The triage table

| # | Layer / decision | Default | What flips it |
|---|---|---|---|
| P | **Package dimension** | **HITL** (DAG root; blocks everything) | → derived when the charter or codebase already fixes it (single-product, no verticals, or explicit tenancy structure in code) — record `core`, no ticket |
| 1 | **Ontology** (always-formal) | **AFK** — reverse-engineer from Prisma/`models/`/OpenAPI; ticket asks only for deltas | → HITL greenfield (no models to read); → HITL for PII tagging *only* when attribute semantics are ambiguous (a field named `notes` that might hold PII) |
| 2 | **State machines** (always-formal) | **AFK** — status enums + transition code are readable | → HITL for a *new* lifecycle, or when guards encode business policy the code doesn't state (credit thresholds, approval rules) |
| 3 | **Event catalog** (always-formal) | **AFK** — producers/consumers/payloads readable from `events.ts`, handlers, topics | → HITL when the envelope/versioning strategy is unsettled (real trade-off); → HITL for events a *new* feature must introduce |
| 4 | **Tool registry** (lightweight) | **AFK** enumerate from routes/controllers; `safety`/`requires_human_approval` defaults are **derived by rule** (write + financial/destructive/PII-touching → gated) | → gating *overrides* (relaxing or tightening a rule-derived gate) are HITL but **owned by the Verification ticket** (layer 11 is where SDD interviews approval-gate policy) — layer 4 itself stays AFK |
| 5 | **Workflows & sagas** (lightweight) | **AFK** — existing cross-service processes readable from orchestration code | → HITL for compensation semantics not already implemented ("what happens when step 3 fails" is a trade-off, not a fact) |
| 6 | **Data ownership** (always-formal) | **HITL** — who *should* own an entity is load-bearing judgment; an AFK sub-ticket maps the as-is (which store holds which table, where PII copies live) and seeds it | → derived for a single-service system (one owner, no ticket); → escalate immediately if the AFK as-is map finds duplicate ownership |
| 7 | **C4 model** (lightweight) | **AFK** — containers from ownership's service list + deploy configs (compose/k8s); actors from auth code | → derived once ownership lands and topology is unambiguous (skip the ticket); → HITL when target-state re-architecture is on the table |
| 8 | **Roles & policies** (formal when PII/regulated) | **HITL** — share/permission *semantics* are policy; the role *inventory* is AFK-read and seeds the ticket | → AFK when `allow_roles` already exists in code and no new semantics are needed (pure transcription); tier escalates to audit-grade formal on consumer PII |
| 9 | **Compliance rules** (formal when PII/regulated) | **HITL-formal** — retention, legal basis, opt-out posture are the human's; the *PII scan* that triggers it is AFK, and erasure-reachability is validator-derived | → derived stub ("lightweight, formalize when audit arrives") when the AFK PII scan is clean **and** the domain is unregulated. Consumer PII appearing anywhere flips it back to HITL-formal — CCPA/CPRA reach ordinary retailers |
| 10 | **Integration contracts** (lightweight) | **AFK** — connectors, protocols, message mappings readable from clients/webhooks | → HITL when choosing a *new* integration protocol or partner (trade-off); PII-outbound flows found here escalate to the compliance ticket, not a new decision |
| 11 | **Verification & observability** (formal when agent-executed) | **derived** — trajectory rubric, tool-call contracts, span taxonomy all generate from layers 2/3/4/8; no ticket (the ticket, when it exists, also reads compliance — see template row) | → HITL for exactly the three non-derivable questions, and only when an LLM agent drives the tools: LM-judge rubrics ("what does good mean"), approval-gate overrides (single owner per row 4), golden-trajectory picks |
| O | **Observability dimension** | **derived** — span tags fall out of schema-element ids + package; SDD says don't interview for it | never flips; it has no ticket by construction |
| V1 | **Kit** (framework + component library) | **HITL, one early ticket, seeded with the repo-read default** — VDD calls it "a front-loaded interview decision — asked once"; an existing `package.json`/design system wins by default, so on an existing stack it's a quick confirm | → the flip is *depth*, not triage: greenfield opens the full recommend-from-UX interview; existing stack is confirm-or-replatform |
| V2 | **Nav classification** (`primary/secondary/none` per entity) | **HITL** — one batched ticket, seeded with the derived proposal (junctions/children → `none` by heuristic); human confirms exceptions | → derived for structurally forced entities (junction tables, pure child rows) — exclude them from the ticket |
| V3 | **State waivers** | **no ticket exists until the validator flags a missing per-archetype state; then HITL** — a waiver is a written human reason by definition; universal-6 is a hard floor and never waivable | never flips to AFK — an agent writing its own waiver defeats the mechanism |
| V4 | **Archetype overrides** (columns, density, placement) | **derived** — auto-binding covers it; rare placement exception is the only human call | → HITL per exception, on request only; `visual: needs-human` remains a build-phase human gate, not a map ticket |

**Tally: 11 SDD layers → 7 AFK, 3 HITL (ownership, roles, compliance), 1 derived
(verification). Package: HITL. VDD experience layer: 3 HITL (kit, nav, waivers), 1
derived (overrides). Observability: derived.** Most of the map is
agent-resolvable or never a ticket at all — the human's queue is short and every item
on it is a genuine judgment.

### Validator-spawned tickets

Cross-reference failures (map constraint 4) spawn tickets with a split verdict: the
**fix** is triaged by this table (a dangling event is AFK; a duplicate-ownership hit is
HITL), while a **defer-with-reason** is always HITL — a deferral reason, like a waiver,
is human-authored by definition.

## Escalation rules

### AFK → HITL: the research ticket births a grilling ticket (prescriptive)

An AFK agent that discovers its question is actually **contested** — a real trade-off,
hard to reverse, or the facts came back surprising — must not decide. It:

1. **Finishes only the measurable part** of its own ticket: figures, not impressions,
   recorded in `docs/research/` (herdrmux #17 measured churn per file, cadence,
   upstream posture — it never answered "fork or track").
2. **Births a `wayfinder:grilling` ticket** carrying the decision, with the options and
   the measured costs of each stated in the body.
3. **Wires the edge:** the grilling ticket is `blocked-by` the research ticket, so the
   human never grills without the facts in hand.

**What the exemplar attests, honestly:** herdrmux #10 ← #17 shows the *wiring and
discipline* (a grilling decision hard-blocked on a research ticket; the research agent
measuring without deciding — #17's body opens "Blocks #10, which cannot be decided
without knowing what tracking upstream would actually cost"), **not the genesis**. #10
predates #17 by 50 minutes and came from charting; the research ticket was created to
unblock an existing decision, the reverse direction. The mid-research birth rule above
is prescriptive — no exemplar instance exists yet. Its trigger: when an AFK agent finds
itself **reframing the question rather than measuring it**, that is the signal to birth,
not decide. (The phrase "the question the ticket asked is not quite the one that
matters" is from #10's *resolution*, written after the fact — a retrospective
description of the phenomenon, not a tell that fired mid-research.)

### HITL → AFK: the grilling ticket gets downgraded

The mirror rule, from SDD's "asking the user things you could read" anti-pattern: a
grilling ticket whose question turns out to be answerable from the codebase (the
"decision" was already made — it's in the models, the auth code, the deploy config) is
**relabeled research and resolved AFK**, with the found answer recorded as fact, not
decision. Only the *delta* from what the code says — if any remains — stays HITL. This
keeps the one-HITL-per-session budget spent on real judgments.

## Ticket-template mapping

Question shapes are seeded verbatim from schema-driven's layer prompts; `blocked-by`
edges come from SDD's stated dependency order and cross-references. Where SDD's serial
order hid a two-way reference (tools↔roles, ownership↔C4), the DAG resolves it
explicitly below; the validator catches whatever the provisional direction misses.

| Layer ticket | Question shape (seed) | Blocked-by edges |
|---|---|---|
| Package | "Single package (`core`) or named verticals? Default: `core` unless multi-tenant is explicit." | — (root; blocks everything) |
| 1 Ontology | AFK: "Reverse-engineer entities/attributes/states/events from {models source}; tag PII attributes; report deltas and ambiguities." HITL variant: "What entities does this system manage? I'll start the list." | Package |
| 2 State machines | Per stateful entity: "Valid transitions? Triggering event per transition? Guards?" — seeded with the lifecycle read from code | that entity's Ontology ticket |
| 3 Event catalog | Per declared event: "Producer? Consumers? Payload? Envelope?" — producer defaults to the owning service | Ontology; **soft edge to Ownership** (SDD layer-3 rule: flag, don't block, if ownership undecided — producer field stays provisional) |
| 4 Tool registry | Per entity: "What operations can a user/agent perform? For each: kind, safety, approval, emitted events, typed inputs (coerce GET params)." | Event catalog; `allow_roles` filled provisionally, validated by the Roles ticket |
| 5 Workflows | "Which processes span 2+ services? Trigger event, steps, compensations?" (single-service ops are tools, not workflows) | Tool registry, Event catalog |
| 6 Ownership | "Which service owns each entity (exactly one)? What does each reference read-only? For PII entities: where *else* does the data live?" — seeded by the AFK as-is map | Ontology |
| 7 C4 | "Containers = services from ownership; tiers? Actors?" | Ownership |
| 8 Roles | "What roles exist, per org type and package? Which do the declared tools require?" — don't pre-declare roles no tool uses | Tool registry (roles derive from tool demand; closes the tools↔roles loop) |
| 9 Compliance | "What regulations apply (assume CCPA/CPRA+GDPR on consumer PII)? Is every PII entity erasure-reachable, including copies? Retention + legal basis? Durable suppression?" | Ontology (PII tags), Ownership (where-else-it-lives); receives escalations from Integrations |
| 10 Integrations | Per external system: "Inbound/outbound/both? Protocol? Each inbound message → which entity, which event? Each outbound PII flow → on the ownership copy-list?" | Event catalog, Ontology |
| 11 Verification | Only the three HITL seeds: "Which tools emit NL output, and what's each LM-judge rubric? Approval-gate policy overrides? Which transitions get golden trajectories first (highest blast radius)?" | Tool registry, State machines, Event catalog, Roles, Compliance |
| V1 Kit | "Repo stack found: {X} — stay on it? (Greenfield: recommend from the UX; accessibility is a selection criterion.)" — always a ticket, per triage row V1 | — (repo read only) |
| V2 Nav | Batched: "Proposed `primary/secondary/none` per entity — confirm exceptions; not every entity gets a menu item." | Ontology |
| V3 Waivers | Per validator flag — universal-6 state missing: "Surface {S} omits {state}. Fix." (fix-only; the floor is never waivable). Per-archetype add missing: "Fix, or waive with a written reason?" | the surface's source tickets (Tools, Roles, State machines) — exists only post-validator |
| V4 Overrides | Per exception: "Default binding is {X}; override placement/columns?" | Kit |

**Hard `blocked-by` edges never point forward.** Forward references exist only as soft
mechanisms: a ticket may leave a field provisional (event producer before ownership;
`allow_roles` before roles; the layer-3 soft edge to Ownership; Integrations escalating
into Compliance), and the continuously-running validator spawns the reconciliation
ticket if a provisional value goes stale — that is constraint 4 doing the work the
serial 1→11 order used to do.

**Embedding notes** (this table claims verbatim embeddability — these must travel with
it): "map constraint 3" = one HITL ticket per session; "map constraint 4" = validator
failures spawn tickets; the scope guard = multi-session work on an existing codebase
(steig/skills#20, Settled 3–5). Per #22, every seeded ticket below the frontier also
carries a `provisional` marker and is **re-posed against the current trunk at pickup**
— a seeder built from this table must emit that marker.
