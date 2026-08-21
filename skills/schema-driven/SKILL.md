---
name: schema-driven
description: Walk the user through Schema-Driven Development (SDD) design decisions for a new system or feature before any code is written. Forces explicit decisions across the 11 interlocking schema layers — ontology, state machines, events, tools, workflows, data ownership, C4, roles, compliance, integrations, verification — plus the package and observability dimensions. Use when the user wants to "spec this out", "model the system before coding", "schema-drive this", "walk me through SDD on X", "design the contracts first", or is starting a non-trivial new system, service, or domain (50+ entities, regulated, multi-team, long-lived, or agent-consumed). Don't wait for explicit invocation — if the user is about to start building something non-trivial and the domain model isn't yet pinned down, suggest schema-driving it first.
---

# Schema-Driven Design Interview

The user is about to build a system, service, or feature whose domain semantics matter. Before code is written, walk them through the 11 SDD schema layers in dependency order, forcing an explicit decision on each branch. The goal is a cross-referenced specification that is both human-readable and machine-consumable — so when implementation starts (by them or an agent), the architecture is already decided and the only remaining work is precision.

The style is a relentless design interview: one question per turn, every recommendation anchored in the SDD operating principles, no branch left unresolved. The decision tree is pre-defined by the methodology.

## When NOT to do this

SDD has clear boundaries. **Refuse or scope down** if the work is:

- A discovery-phase product where the domain model is still being learned
- A single-service CRUD app whose entities fit in one developer's head
- A UI-heavy workflow where complexity is in interaction design, not domain
- A prototype, MVP, or spike where learning speed matters more than correctness
- A bug fix, refactor, or feature addition to an existing system whose schemas already exist (in that case, read them first, then ask only about deltas)

If the request looks like one of these, say so up front and offer a lighter alternative: "This looks like X — schema-driving it would be overkill. I'd recommend Y instead. Still want the full SDD walkthrough?" Don't sandbag the user into a long interview they didn't need.

## How to operate

**One layer at a time, one question per turn.** Don't dump the whole decision tree on the user. Resolve the current layer before moving to the next, and within a layer resolve one branch before opening another.

**Walk layers in dependency order.** Later layers reference earlier ones. The order is fixed because the cross-references only resolve one way:

1. **Ontology** — entities, attributes, states (declared), events (declared), package
2. **State machines** — transitions, guards, triggering events (references ontology states + events)
3. **Event catalog** — producer, consumers, payload, envelope (references ontology events)
4. **Tool registry** — operations, API, safety, permissions, emitted events (references events + roles)
5. **Workflows & sagas** — multi-step processes (references tools + events)
6. **Data ownership** — which service owns which entity (references ontology + C4)
7. **C4 model** — system structure, containers, actors (references services from ownership)
8. **Roles & policies** — RBAC/ABAC for tool access (references tools)
9. **Compliance rules** — regulatory constraints scoped to packages
10. **Integration contracts** — external connectors, message mappings (references events + entities)
11. **Verification & observability** — eval rubric, tool-call contracts, span taxonomy (references tools + state machines + events + roles + compliance)

Plus the **package dimension** — every schema element carries a `package` tag, decided up front and applied to every later answer.

And the **observability dimension** — every runtime span (tool call, transition, event) is tagged with the schema-element id and package that produced it, so traces and eval failures are queryable along the same axes the system was designed with. Like the package tag, it's decided once and falls out of the other layers; you don't interview for it separately.

**Pose each question with tradeoffs visible, and recommend.** Anchor recommendations in the SDD operating principles when relevant. Example: "I'd model this as a `Tool` with `safety: unsafe` and `requires_human_approval: true` because it mutates financial state — that follows the operating principle 'Tools, not APIs.' The alternative is a bare endpoint, which loses the safety classification and approval gate. Which way?"

**Apply tiered formalization.** Not every layer needs full rigor for every system. Adjust depth to risk:

- **Always formal** (no shortcuts): Ontology, State Machines, Event Catalog, Data Ownership. These are expensive to get wrong — orphaned entities, missing transitions, dangling events, shared ownership all create bugs that compound. Spend time here.
- **Formal when regulated _or holding consumer PII_**: Compliance Rules, Roles & Policies. Don't limit this to finance/healthcare/insurance — CCPA/CPRA (and GDPR) reach any business holding consumers' personal information; an ordinary e-commerce retailer qualifies. If the system stores names, emails, IPs, phone numbers, or purchase history of consumers, treat the compliance layer as audit-grade: PII flags, retention, erasure-reachability, and opt-out/suppression are formal, not "later."
- **Lightweight acceptable**: Workflows, C4 Model, Integration Contracts, Tool Registry. Useful as documentation early; can graduate from markdown to formal JSON as the system stabilizes. Don't over-formalize on day one — that's the architecture astronaut trap.
- **Formal when an agent executes the tools**: Verification & Observability. If the only consumer of the schemas is deterministic codegen, the cross-reference validator already covers the deterministic core and the eval scaffold is documentation. The moment an LLM agent drives the tools, its trajectory and its NL outputs are non-deterministic and must be checked — make the eval layer formal (golden trajectories in CI, approval gates enforced, LM-judge rubrics with explicit scoring).

Tell the user which tier each layer falls into as you enter it, so they know when to push back on depth.

**If the answer is in the codebase, go find it.** Don't ask what entities exist when there's a `models/` directory. Don't ask what events fire when there's a `events.ts`. Read first, ask only about deltas. This is doubly true for SDD on an existing system — the schemas may exist in some form (Prisma, OpenAPI, Pact contracts); reverse-engineer those before interviewing.

**Cross-reference as you go.** After each layer, name what it just locked in for later layers. Example: "OK — we've declared `OrderConfirmed` as an event on the `Order` entity. That means: the state machine transition `Draft → Confirmed` must emit it, the event catalog needs a payload schema for it, and at least one tool must produce it. We'll resolve those when we get to those layers — I'll flag if any go missing."

**Validate at the end.** Before declaring done, run the cross-reference checks the methodology proposes:

- Orphaned entities (no owning service)
- Missing state machines (entity has states, no machine)
- Dangling events (emitted but not cataloged)
- Toolless transitions (transition with no implementing tool)
- Permission gaps (tool references non-existent role)
- Duplicate ownership (entity owned by 2+ services)
- C4/ownership mismatch (service in ownership not in C4)
- Uncovered events (cataloged event with no producer tool)
- **PII not erasure-reachable** (an entity carries a PII attribute but isn't covered by the deletion/erasure path)
- **PII copies outside erasure/suppression scope** (a PII-bearing entity is replicated or exported — read model, warehouse, parquet, ad-platform audience, external processor — with no deletion/suppression reaching the copy)
- **Untested transition** (a declared state transition with no golden trajectory exercising it — invisible until an agent drives it wrong in production)
- **Ungated write executed without approval** (a tool the approval policy marks gated that a recorded trajectory ran without a human sign-off)
- **Unjudged NL output** (a tool whose output is LLM-generated but has no LM-judge rubric, so "did it answer well?" is unmeasured)

> **Check membership both ways.** A validator that only iterates `erasure.applies_to` (or any compliance allow-list) will silently pass an entity that was *omitted* from it — the gap is invisible. Assert the inverse: every entity with a PII attribute **must** appear in the erasure scope. (Real bug: two PII carriers escaped erasure for exactly this reason — the coverage rule never checked for omissions.)

For each gap, ask: fix it now or accept it as deferred (with a written reason)?

**Make implicit assumptions explicit.** When the user says "Order has a customer," surface the assumption: "OK, so `Order.customer_id` references the `Customer` entity owned by `customer_service` — that means orders consume `CustomerUpdated` events to stay in sync. Confirm or change?"

**Push back on hand-waves for load-bearing layers.** "We'll figure out ownership later" is a non-answer because every later layer depends on it. Either pin it down or name what blocks the answer.

**Defer derived artifacts.** Don't interview about the DB schema, OpenAPI spec, or actions matrix — those are *generated* from the primary schemas. If the user asks "what about the database?", remind them: "DB schema is derived from the ontology. We pin the ontology, then generate. Skip ahead?"

## The package dimension — decide early

Before the ontology, ask: **what packages does this system support?**

- A single-product startup: one package (`core`) is fine; mark every entity `package: "core"` and move on.
- A multi-tenant platform serving distinct verticals: name the packages now (`core`, `lending`, `payments`, `wealth`) and require every later answer to declare which one it belongs to.

Recommended default: one `core` package unless the user explicitly names a multi-tenant or multi-vertical use case. Don't pre-engineer packages for a system that may never need them.

## Layer-by-layer prompts

These are the seeds for each layer. Use them as a starting point; adapt to context.

### 1. Ontology

- "What entities does this system manage? I'll start the list — add anything I miss."
- For each entity: "Required attributes? Optional ones? States it can be in? Events it emits?"
- "Which attributes are PII?" — tag them now; the compliance layer depends on it.
- "Which package does this entity belong to?" (skip if single-package system)
- Recommendation pattern: propose the obvious entities from the user's description, mark which states/events feel canonical, ask what's missing.

### 2. State machines

- For each entity with states: "Which transitions are valid? What event triggers each? What guards must hold?"
- Recommendation: draw the obvious lifecycle (Draft → Confirmed → Done), name the guards you'd expect (`credit_check_passed`, `all_lines_valid`), ask which are wrong.

### 3. Event catalog

- For each event declared in ontology/state machines: "Who produces it? Who consumes it? Payload?"
- Recommendation: name the producer from the entity's owning service (decided in layer 6 — flag if not yet decided), guess obvious consumers (audit, analytics always consume; domain consumers per use case).

### 4. Tool registry

- "What operations can a user or agent perform on this entity?"
- For each tool: `kind` (read/write/admin), `safety` (safe/unsafe/destructive), `requires_human_approval`, `emits_events`, `permissions.allow_roles`.
- Recommendation: write tools mutate state and emit events; safety follows blast radius; approval gates on anything financial, destructive, or PII-touching.
- **Implementation note: type tool inputs explicitly.** Query-string params arrive as strings — a GET tool with an `int`/`bool`/`date` param that isn't coerced at the boundary will silently 400 (or worse, compare wrong). Declare param types in the registry so the generator coerces them.

### 5. Workflows & sagas

- "Which cross-service processes does this system run?"
- For each: trigger event, steps, compensations.
- Recommendation: only model workflows that span 2+ services. Single-service operations are tools, not workflows.

### 6. Data ownership

- "Which service owns each entity?" — one and only one per entity.
- "Which entities does each service reference (read-only) from elsewhere?"
- For PII-bearing entities, also record **where else the data lives** — read models, warehouse/exports, parquet snapshots, external processors (analytics, ad platforms, email, payment). A deletion/erasure obligation must reach **every** copy, not just the owning store. This list is what makes a DSAR tractable later.
- Recommendation: ownership follows the team that operates the lifecycle; references happen via events or read models, never shared DBs.

### 7. C4 model

- "Containers: which services exist? Tiers (platform / core / vertical)?"
- "Actors: who uses the system?"
- Recommendation: reuse the service IDs from data ownership; group into platform-engine, core, and package-specific tiers.

### 8. Roles & policies

- "What roles exist? Which org types do they belong to? Which packages?"
- Recommendation: start with `Admin`, `Operator`, `Viewer` per package; add domain roles as tools require them. Don't pre-declare roles no tool uses.

### 9. Compliance rules

- "What regulations apply? **If the system holds consumer personal information, assume CCPA/CPRA (and GDPR for EU data) apply — even if you're not in a 'classic' regulated industry.**"
- "Which entities carry PII?" (you tagged these in the ontology) — "is every PII-bearing entity reachable by the deletion/erasure path?" Omitted carriers are the #1 compliance bug; see the validation checks.
- "Retention: how long is each PII category kept, and what's the legal basis for keeping it past a deletion request?" (e.g., completed-order/tax records are retained and anonymized, not deleted.)
- "Opt-out / suppression: do consumers have a 'do not sell/share' right? If so, model a **durable suppression mechanism keyed on a stable (hashed) identifier** — deletion is point-in-time, opt-out is forward-looking and must survive account re-creation and reach every external processor."
- "External processors: which PII leaves the system (analytics, ad platforms, email, payment)? Each is a 'share' surface and must be reachable by both deletion and suppression."
- Recommendation: if consumer PII is involved, model this formally now (PII flags + erasure reachability + retention + suppression). If genuinely no consumer PII and no regulated domain, mark "lightweight, formalize when audit arrives."

### 10. Integration contracts

- "What external systems does this connect to? Inbound, outbound, or both? What protocols?"
- For each inbound message: which entity does it map to, which event does it emit?
- For each outbound flow carrying PII: confirm it's listed under the owning entity's data-ownership "where else it lives" so erasure/suppression reaches it.
- Recommendation: model only the boundary; internal services use the event catalog directly.

### 11. Verification & observability

**Most of this layer is derived, not interviewed.** Like the DB schema and OpenAPI spec, the deterministic eval scaffold falls out of the layers already pinned — don't ask the user to hand-write it. From the schemas you can generate, for free:

- **The trajectory rubric** from the state machines — a valid trajectory is a legal path through the machine, and the tool that emits a transition's event is that edge's implementing tool. This is the rubric source most eval setups lack.
- **Tool-call contracts** from the tool registry — for any recorded agent call: input parses against the tool's typed schema, caller role ∈ `allow_roles`, emitted events ⊆ `emits_events`, and gated tools carry an approval. All checkable with no human input.
- **The observability span taxonomy** — every span tagged with the tool/transition/event id + package, so traces and failures cluster along the same axes as the design.

So when you reach this layer, **interview only the parts that genuinely can't be derived**:

- "Which tools produce LLM-mediated (natural-language) output that needs an **LM-judge rubric**? For each, what's the scoring rubric — what does 'good' mean?" (An eval without a rubric measures nothing.)
- "What's the **approval-gate policy**? Default I'd apply: every `unsafe` write requires human sign-off. Override per tool?"
- "Which transitions and tools need **golden trajectories** in CI before they ship? Start with the highest-blast-radius ones."

Scope this to the complement of correctness-by-construction: **don't generate evals that re-test what the schema already guarantees.** The cross-reference validator covers static consistency; this layer covers only the non-deterministic surface — agent trajectories, NL outputs, and runtime cross-system behavior (e.g., post-deletion PII probes).

- Recommendation: generate the deterministic scaffold from the specs (rubric + contract checker + span taxonomy) on every `generate` run; keep the hand-authored golden trajectories and LM-judge rubrics in a separate, non-generated location so a regeneration never clobbers them.

## How to know you're done

- Every entity has: an owning service, a state machine (if stateful), a catalog entry for each declared event
- Every event has: a producer, at least one consumer, a payload schema
- Every tool has: API binding, typed inputs, safety class, permission roles, emitted events declared
- Every workflow step references a tool that exists in the registry
- Every service in data ownership exists in the C4 model
- Every role referenced by a tool exists in roles & policies
- Every PII-bearing entity is erasure-reachable and its external copies are on the deletion/suppression map
- If an agent executes the tools: every non-deterministic surface has a verification — a golden trajectory for each high-blast-radius transition, an enforced approval gate for each gated write, an LM-judge rubric for each NL output — or is explicitly deferred with a reason
- Cross-reference checks pass (or remaining gaps are explicitly deferred with reasons)
- The user signals satisfaction — "ok, let's go," "that's the spec"

When done, **synthesize a brief summary**: list the entities, the package(s), the services, the high-risk transitions, the PII entities + their erasure/suppression coverage, and any deferred items. This is the artifact the user (or an agent) will hand to implementation. Offer to write it out as JSON files (`ontology.json`, `compliance.json`, `state_machines.json`, etc.) in the project — but only if asked. Don't auto-generate.

## Lessons baked in (from production)

These refinements come from real failures on our own systems — apply them by default:

- **Compliance allow-lists hide omissions.** A `GDPR_ERASURE.applies_to` list that the validator merely *iterates* will pass a PII carrier that was left *off* it. Two carriers escaped erasure this way. Always assert the inverse: every PII attribute implies erasure-reachability.
- **Consumer PII ≠ "regulated industry."** CCPA/CPRA apply to an ordinary retailer. Treat the compliance layer as formal whenever consumer PII is stored, not only for finance/healthcare.
- **Opt-out is forward-looking.** A "do not sell/share" suppression must survive account re-creation and reach every external processor — model it as a durable, identifier-keyed mechanism, not a one-time scrub.
- **Coerce GET query params.** Untyped string params silently 400; declare input types so the generator coerces them.

## Anti-patterns

- **Walking all 11 layers for a system that doesn't need them.** A single-service CRUD app needs ontology and maybe state machines. Don't drag the user through compliance rules they don't have.
- **Asking the user things you could read.** If models exist, read them. If a Prisma schema is sitting there, that's most of the ontology — confirm gaps, don't reinvent.
- **Skipping the package dimension.** Decide it once, up front. Otherwise every later answer is missing a field and you'll have to retro-fill.
- **Letting "we'll figure out ownership" pass.** Ownership is load-bearing. Pin it before moving past layer 6, or every subsequent answer is provisional.
- **Treating compliance as "only when regulated."** If the system holds consumer PII, it's regulated (CCPA/CPRA). Tag PII in the ontology and assert erasure-reachability — don't defer it.
- **Validating compliance with an allow-list only.** Membership must be checked both ways, or omitted PII carriers pass green.
- **Auto-writing JSON files.** The user may want the interview output to feed into their own template, agent prompt, or doc system. Offer; don't impose.
- **Over-formalizing tools and workflows on day one.** These can be markdown notes early. Force them through the registry only when the system has stabilized or when an agent will consume them.
- **Generating evals that re-test what the schema guarantees.** The cross-reference validator already proves the deterministic core. The verification layer's job is the *complement*: agent trajectories, NL outputs, runtime behavior. Re-asserting "the input matches the type" the codegen already enforced is wasted CapEx and OpEx.
- **Hand-authoring the derivable eval scaffold, or letting regeneration clobber the hand-authored part.** The rubric, contract checker, and span taxonomy are generated; golden trajectories and LM-judge rubrics are authored once and live outside the generated tree. Mixing them means either reinventing free artifacts or losing expensive ones on the next `generate`.

## Example exchange

User: "I'm building an inventory management system for our warehouses."

Bad: "Great, let's start with the ontology. What entities does this system have? What attributes does each have? What states? What events? What's the package structure?"

Better: "Before we open the ontology, two scoping questions:

**Is this a single-tenant warehouse app, or a multi-tenant platform serving different warehouse types (3PL, retail DC, manufacturing) with different rules?** I'd default to single-tenant with one `core` package — pre-engineering packages for a system that may never need them is the architecture astronaut trap. We can split later if you ship multi-tenant.

Which is it?"

(After answer:) "OK, single-tenant, one `core` package. Layer 1: ontology. I'll seed the obvious entities — `Item`, `StockLevel`, `Location`, `Movement`, `Receipt`, `Shipment` — and you tell me what I'm missing or what's wrong. Start with `Item`: required attributes, optional attributes, states? And flag any PII attributes now — if this holds supplier or customer contact data, the compliance layer becomes formal."
