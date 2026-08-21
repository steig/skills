---
name: view-driven
description: Walk the user through View-Driven Development (VDD) — the frontend companion to schema-driven. Projects the SDD schemas (ontology, tools, state machines, roles) onto a closed set of UI archetypes so an agent scaffolds clean, consistent screens instead of improvising a layout each time. Forces explicit decisions only on the thin experience layer schemas can't encode — the kit (frontend framework + component library, recommended from the UX being described), navigation, per-surface state waivers, archetype overrides — and ships a static validator plus a runtime conformance layer (state-coverage, permissions, interaction legality, accessibility) that stops at the door of visual taste and routes it to a human. Use when the user wants to "scaffold the frontend", "design the UI before building", "spec the screens", "make the agents build consistent UI", or is about to build a frontend over a system that already has (or will have) SDD-style schemas. Requires the domain schemas to exist first; it is derive-first and useless standalone.
---

# View-Driven Design Interview

The user is about to build (or scaffold) a frontend over a system whose domain is already modeled in schemas — entities, tools, state machines, roles. Before screens are written, walk them through projecting those schemas onto a closed set of UI **archetypes**, forcing a decision only on the handful of things schemas genuinely can't encode. The goal is a cross-referenced UI specification that is both human-readable and machine-consumable — so when implementation starts (by them or an agent), the layout, the states, and the affordances are already decided, and the only remaining work is binding them to components.

This is the **companion to `schema-driven`**: SDD pins the domain; VDD projects it onto the screen. Same relentless-interview discipline — one question per turn, recommendations with tradeoffs — but the decision tree is pre-defined and most of it is *derived*, not asked.

## The one rule that defines this skill: derive-first

Most of a frontend is already latent in the SDD schemas. Treat it as a **projection**, not a fresh spec:

| Derived for free — never interview | Source schema |
|---|---|
| list/detail screens | entities (ontology) |
| create/edit forms (typed, with enums + required) | tool inputs (tool registry) |
| buttons + confirm dialogs + gating + visibility | tool `kind`/`safety`/`requires_human_approval`/`allow_roles` |
| status badges, transition buttons, step flows | state machines |
| menu skeleton + per-item visibility | packages / domains / roles |
| relation selectors | `ref` attributes |

The interview covers only the **experience layer** schemas don't hold: the kit (framework + component library — see below), which entities deserve a menu home, per-surface state waivers, and archetype overrides (which columns, what density). If you find yourself asking the user what fields a form has, stop — read the tool input. Scope every question to *the complement of what the schemas already encode.*

## When NOT to do this

**Refuse or scope down** if the work is:

- A frontend with **no domain schemas** (no ontology/tool registry, and none planned). VDD is derive-first — without SDD-style schemas there's nothing to project. Run `schema-driven` first, or fall back to ordinary component work.
- A **marketing site, landing page, or content surface** — the complexity is in copy and visual design, not data-bound screens. Archetypes don't help.
- A **bespoke, highly-interactive canvas** (editor, whiteboard, game, dashboard-builder) where the value *is* the custom interaction. Archetypes constrain exactly what you want free here.
- A **one-off screen** added to an existing frontend whose patterns are already established — follow the existing patterns, don't impose a methodology.

If the request looks like one of these, say so up front: "This looks like X — view-driving it would be overkill / impossible without schemas. I'd recommend Y instead. Still want the full walkthrough?" Don't drag the user through an interview that doesn't fit.

## How to operate

**Derive first, then interview the gaps — one archetype or one decision per turn.** Don't dump the whole surface map on the user. Generate the derived projection, show it, and ask only about the exceptions.

**Pose each question with tradeoffs visible, and recommend.** "I'd make `Order` a `primary` nav item and `OrderLine` `none` — line items are reached through their order, not the global menu. Putting junction entities in the sidebar is the #1 way these get cluttered. Agree, or does `OrderLine` need its own home?"

**If the answer is in the schemas, go find it.** Read `tool_registry.json` for form fields, `state_machines.json` for statuses, `roles.json` for who sees what. Asking the user what a form contains when the tool input declares it is the cardinal sin of this skill.

## The archetype vocabulary — the UI ontology

Every data-bound surface is exactly **one of six archetypes**. This closed set is the whole reason agents produce consistent UI: they *name an archetype*, they don't design a layout. A surface that fits none needs a deliberate, reviewed new archetype — not a freelanced page.

| Archetype | What it is | Auto-bound from |
|---|---|---|
| `collection` | table/list of an entity | every entity (one each) |
| `record` | detail view of one entity | every entity (one each) |
| `form` | create/edit | every non-trivial write tool |
| `dashboard` | aggregates / rollups | opt-in per domain |
| `wizard` | multi-step flow | every workflow / saga |
| `picker` | select a related entity | every `ref` attribute |

**Modal vs. page is a presentation flag, not a separate archetype.** A `form` or `record` renders inline, in a modal, or full-page — that's one boolean on the surface, decided per context, never a new layer.

### Archetype anatomy: contract + adapter

Each archetype is a **generic contract** the skill owns, bound to real UI by one per-project **kit adapter** — the seam that keeps this skill stack-agnostic (the exact analogue of SDD's per-stack code generator).

- **Contract** (generic): `slots` (named regions — `title`, `primaryActions`, `filters`, `body`, `rowActions`, `footer`…), `requiredStates` (below), `affordances` (which actions render where), and **accessibility obligations** — every interactive slot is keyboard-reachable, labeled, and focus-managed *by contract*, not as a later audit. This is where best practices live.
- **Kit adapter** (one stack-specific file): maps each slot → the project's actual components (`title → <PageHeader>`, `body → <DataTable>`). Swap the adapter and the same archetypes render in React, Vue, or anything. **The contracts never name a component library** — but choosing one is a real decision, so the interview owns it (next section).

So `layout` = the slot arrangement a contract prescribes; `components` = whatever the adapter binds slots to. Neither is a freeform canvas.

## Picking the kit — one early, explicit decision

The adapter has to bind slots to *something*, so the framework and component library are a
front-loaded interview decision — asked once, early, and recorded in the adapter. Rules:

- **Read the repo first.** An existing `package.json`, an established design system, or a
  team's current stack wins by default — recommend staying unless the user is explicitly
  replatforming. Don't relitigate a decision the codebase already made.
- **Greenfield: recommend from the UX they're describing**, with tradeoffs visible:
  - *Data-dense internal/admin* (heavy `collection`s, bulk actions) → a headless table
    (TanStack Table) + an accessible primitive/component kit (shadcn/Radix, Mantine)
  - *Forms-heavy back office* (many `form`s and `wizard`s) → a batteries-included library
    with mature form + validation patterns (Mantine, Ant Design)
  - *Customer-facing product surface* (brand matters, fewer archetypes) → primitives you
    style yourself (Radix/Headless UI + Tailwind) over a themed kit you'll fight
  - *Team already fluent elsewhere* → project onto their stack (Vue → PrimeVue/Vuetify,
    Svelte → Bits UI/Skeleton); the archetypes don't care
- **Accessibility is a selection criterion, not a nice-to-have.** The contracts oblige
  every interactive slot to be keyboard-reachable, labeled, and focus-managed — so prefer
  libraries that deliver that out of the box (it's the hardest thing to retrofit). A
  beautiful kit with broken keyboard support fails the contract before taste even comes up.
- Record the outcome as the kit adapter's header: framework, library, table/form/date
  dependencies. One decision, one place, easy to swap later precisely because everything
  else is contract-shaped.

## The state floor — the best-practices payload

UI is hardest to get right because of the states agents skip. Make them mandatory.

**Universal-6 — hard on every archetype, no exceptions:**

1. `loading` — skeleton, not a spinner on a blank page
2. `empty` — split `empty-initial` (none exist → call-to-action) vs `empty-filtered` (search/filter killed them → clear-filters). Conflating these is the most common miss.
3. `error` — with retry, distinct from empty
4. `forbidden` ← roles + tool `allow_roles` — "you can't see this," not a generic error
5. `stale / refetching` — background revalidation is visible, not silent
6. `not-found` — the id didn't resolve (distinct from error)

**Per-archetype additions — default-on, waivable with a written reason** (the validator flags a *silent* omission, passes a *declared* waiver — SDD's "defer with a reason" pattern):

- `collection` `+` `loading-more`/pagination · `row-pending` · `partial-permission` (some rows actionable) ← roles · `selection`/bulk
- `record` `+` `read-only` (view-not-edit) ← roles · `terminal/archived` ← state-machine end states · `optimistic-pending`+rollback
- `form` `+` `field-error` · `form-error` (server reject) · `submitting` · `optimistic`+rollback · `dirty-guard` (unsaved-changes on nav-away) · `approval-pending` ← tool `requires_human_approval` · `success`+what-next
- `dashboard` `+` **per-widget** `loading`/`error`/`forbidden` (one widget failing ≠ page failing) · `last-updated` stamp
- `wizard` `+` `step-pending` ← saga step · `compensation`/rollback ← saga compensations · `resume` (saved progress) · `abandon-guard`
- `picker` `+` `no-match` · `empty → create-inline` ← ref + the target's create tool · `forbidden` (can't see the target type)

Tell the user the floor is non-negotiable and the adds are waivable, so they know where pushing back on depth is legitimate.

## Navigation — one decision per entity

Keep this dead simple. Derive the skeleton (`package` → section, `domain` → group, role → visibility); the entire interview is a per-entity **`nav: primary | secondary | none`**:

- `primary` — has a top-level menu home (the things you navigate *to*: `Order`, `Customer`)
- `secondary` / `none` — reached *through* a parent `record` or a `picker`, never the global menu (line items, junctions)

The best-practice rule: **not every entity gets a menu item.** Agents default to "everything in the sidebar"; the classification is what prevents the 40-item mess. The **nav chrome** (sidebar vs. topbar vs. command-palette) is the *adapter's* choice — not part of this interview.

## Actions — fully derived, placement auto-defaulted

Don't design actions. They fall out of the tool registry:

- every tool → a button
- `destructive` → confirm dialog first
- `requires_human_approval` → submits for sign-off instead of executing
- caller's role ∉ `allow_roles` → button absent (not disabled — absent)
- **placement auto:** single-id tool → row/record button; multi-target tool → bulk action

The only thing a human might override is placement of a rare exception. Everything else is generated.

## The validator — enforcement, not guidance

Best practices in a doc get skimmed and ignored. Ship the check that *fails* a sloppy surface (the `sdd:validate` analogue). It runs against the surface spec + the SDD schemas:

- **Missing screens** — an entity with no `collection`/`record` and not marked "headless"
- **Formless write tool** — a write tool with non-trivial input and no `form` (or declared headless)
- **State-floor gap** — a surface missing a universal-6 state with no waiver
- **Undeclared waiver** — an archetype add omitted with no written reason (silent skip)
- **Dangling action** — a button referencing a tool that doesn't exist in the registry
- **Phantom field** — a form/table field not present in the source tool input / entity attribute
- **Orphan nav** — a menu item your role can never open (visibility never resolves true)
- **Unknown archetype** — a surface whose type isn't one of the six (caught the freelanced page)

> **Check coverage both ways.** Don't only iterate the surface spec and confirm each surface is valid — iterate the *schemas* and assert every primary entity and every exposed write tool has a surface (or an explicit "headless" marker). A surface spec that's merely internally consistent can still be silently missing half the system. (Same lesson as SDD's erasure-reachability: membership must be asserted from the schema side, not just the spec side.)

For each gap: fix now, or mark headless/waived with a reason?

## Runtime verification — does the rendered surface honor the contract?

The validator above is **static** — it checks the surface *spec* (the `sdd:validate` analogue). It can't tell you whether the component the adapter actually rendered honors its archetype contract. That's the runtime half — the frontend twin of the backend's eval/verification layer — and like everything here it's **derive-first**: the checks fall out of contracts you already specced.

**Derived deterministic checks** (generated from contract + roles/tools/state machine — no interview):

- **state-coverage** — mount each surface in each `requiredState` and assert the contract holds: `empty-filtered` shows clear-filters, `forbidden` *hides* the action (not just disables), `dirty-guard` intercepts navigation, `error` shows retry. The contract lists the states, so the test list is *derived* — exactly how the backend trajectory rubric came from the state machine.
- **affordance / permission** ← roles + tool safety — destructive actions gated behind confirm, `requires_human_approval` routes to sign-off, a role outside `allow_roles` sees no button.
- **interaction legality** ← state machine + nav — the UI exposes only transitions and surfaces actually reachable for the current state/role (no button for an illegal transition, no link to a `forbidden` surface).
- **accessibility** ← the contract's baked-in obligations — keyboard reachability, labels, focus management, contrast on every interactive slot, verified with an axe-style automated pass. Derived from the contract like everything else; largely tooled, not authored.

**Contract + adapter, again:** the *contract* names which checks a surface owes (generic, derived); the *adapter* supplies the stack-specific harness — how to mount a component forced into a given state, and how to assert a slot is present. One harness per project, like the kit adapter and the SDD generators.

**The boundary — visual correctness is out of scope, by design.** These checks prove a surface *behaves* to contract; they deliberately do **not** judge whether it *looks* right — layout, hierarchy, density, taste. That is the human's job, and the skill treats it as a first-class checkpoint, not a gap: every surface carries a **`visual: needs-human`** gate that a person clears by looking at it. Don't mechanize this — no pixel snapshots to re-bless, no vision-model grading. *Generation is solved; judgment and direction are the craft* — the visual pass is exactly where the human guides and corrects, and the methodology's job is to **route their attention there**, not to substitute for it.

Scope, same rule as the backend: **don't re-verify what the generator already guarantees.** The typed form has the right fields by construction; runtime verification checks the *states, permissions, flows, and accessibility* the generator/adapter can't guarantee — then stops at the door of taste.

## How to know you're done

- Every primary entity has a `collection` + `record` (or is explicitly headless)
- Every exposed write tool has a `form` (or is explicitly headless)
- Every surface declares its archetype (one of six) and meets the universal-6 (or has waivers)
- Every action maps to a real tool; every field maps to a real input/attribute
- Navigation classification (`primary/secondary/none`) is decided for every entity
- The kit is chosen (framework + component library, recorded in the adapter) and the adapter exists or its slots are specced enough to write
- Validator passes (or remaining gaps are explicitly waived with reasons)
- Runtime conformance passes per surface (state-coverage, affordance, interaction legality, accessibility); every surface has cleared its `visual: needs-human` gate or is flagged pending human review
- The user signals satisfaction — "that's the surface map," "let's go"

When done, **synthesize a brief summary**: the surface map (entity → archetypes), the nav classification, the waivers and why, and any headless markers. This is the artifact the user (or an agent) hands to implementation. Offer to write it as a `surfaces.json` (or per-entity view files) — but only if asked. Don't auto-generate.

## Anti-patterns

- **Asking what a form/table contains.** It's in the tool input / entity attributes. Read it.
- **Authoring a parallel UI spec that re-declares entities/tools/roles.** That's not derive-first — it duplicates SDD and drifts the moment either side changes. Project; don't restate.
- **Freelancing a "custom page" instead of naming an archetype.** A surface that fits none of the six is a signal to add a reviewed archetype, not to abandon the vocabulary for one screen.
- **Putting every entity in the menu.** Junction and child entities are `none`. The sidebar is for things you navigate *to*.
- **Hard-coding a component library into the contracts.** Contracts own slots and obligations; the adapter owns components. Helping the user *choose* a library is in scope (the kit interview); baking one into the methodology makes it "the X skill," not a methodology.
- **Treating the state floor as optional.** The universal-6 are the whole point — they're the states agents skip. Hard-mandate them; only the per-archetype adds are waivable, and only with a reason.
- **Validating one direction.** A spec that's internally consistent can still miss half the entities. Assert surface-coverage from the schema side.
- **Running this without schemas.** No ontology/tool registry → nothing to derive. Send the user to `schema-driven` first.
- **Mechanizing visual judgment.** Snapshot diffs rot and vision-graders hallucinate; the visual pass is the human's checkpoint, not a test to automate. Verify behavior/states/permissions/accessibility deterministically, and route taste to a person.

## Example exchange

User: "Scaffold the admin UI for our orders system."

Bad: "What screens do you want? What columns on the orders table? What should the order detail page show? What actions are available?"

Better: "These all derive from your schemas — let me project first, then we only talk about exceptions.

From the ontology + tool registry I get: `Order` and `Customer` as `collection`+`record`, `OrderLine` as a child (no menu), 4 write tools → 4 `form`s, `Order.customer_id` → a `picker`, the `Order` state machine → status badges + transition buttons (`confirm`, `cancel`), and `cancel_order` is `destructive` so its button gets a confirm dialog.

Three real questions, not twenty:

**Kit:** this repo already has React + a component library in `package.json`, so I'd stay on it — replatforming isn't in scope. (Greenfield, I'd have recommended from the UX: this is a data-dense admin, so a headless table plus an accessible component kit.) Agree?

**Navigation:** I'd make `Order` and `Customer` `primary` (menu homes) and `OrderLine` `none` (reached through its order). Putting line items in the sidebar is how these get cluttered. Agree?

(After answer:) **State waivers:** the `Order` `collection` will be big — I'm mandating the universal-6 plus `loading-more` and `partial-permission` (some orders may be read-only for support roles). Want me to keep both, or waive `partial-permission` with a reason if every role can act on every order?"
