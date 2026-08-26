# skills

Agent skills I use for my own work, shared in case they're useful. Currently three, and
they're a family:

## schema-driven

An interview that walks you through Schema-Driven Development (SDD) before any code is
written: 11 schema layers in dependency order — ontology, state machines, events, tools,
workflows, data ownership, C4, roles, compliance, integrations, verification — each an
explicit decision, cross-referenced and validated at the end. The output is a spec both
humans and coding agents can build against.

It knows when *not* to run (prototypes, simple CRUD, discovery-phase products) and reads
your codebase instead of asking questions the code already answers.

## view-driven

The frontend companion. Projects the SDD schemas onto a closed set of six UI archetypes
(collection, record, form, dashboard, wizard, picker), derives most of the surface map for
free, and interviews you only on what schemas can't encode: the kit (framework +
component library, recommended from the UX you describe), navigation, state waivers,
archetype overrides. Accessibility is baked into the archetype contracts — keyboard,
labels, focus — and verified mechanically, not audited later. Ships a mandatory state floor (loading/empty/error/forbidden/stale/
not-found on every surface) and validation that checks coverage from the schema side.
Deliberately stops at visual taste — that stays a human call.

Requires domain schemas to exist first; it's derive-first and useless standalone.

## map-driven

The execution companion, for design work one interview sitting can't hold. Runs
schema-driven's completeness through a Wayfinder map: every unresolved branch becomes a
ticket on a DAG, agents resolve the researchable ones in parallel, and the human is
grilled on one genuine judgment per session — one question at a time. A continuous
validator (which is also the seeder) spawns tickets for the gaps nobody thought to
raise, so "done" means *validator green*, not "we ran out of ideas." Decisions land
twice: on the ticket and in an append-only in-repo log that becomes the spec's
provenance. Frontier clear is declared by the human, never auto-closed.

Refuses systems small enough to spec in one sitting — those get plain schema-driven.
Designed by dogfooding itself: [steig/skills#20](https://github.com/steig/skills/issues/20)
is the map that produced it.

## Install

As a Claude Code plugin — this repo is a plugin marketplace, and `steig-skills` carries
all three skills:

```
/plugin marketplace add steig/skills
/plugin install steig-skills
```

The marketplace also lists `worktender` (worktree fleet skills, sourced from
[steig/worktender](https://github.com/steig/worktender)).

Alternatively, with the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add steig/skills --skill schema-driven -g
npx skills add steig/skills --skill view-driven -g
npx skills add steig/skills --skill map-driven -g
```

Or manually — each skill is a single markdown file:

```bash
mkdir -p ~/.claude/skills/schema-driven ~/.claude/skills/view-driven ~/.claude/skills/map-driven
curl -o ~/.claude/skills/schema-driven/SKILL.md \
  https://raw.githubusercontent.com/steig/skills/main/skills/schema-driven/SKILL.md
curl -o ~/.claude/skills/view-driven/SKILL.md \
  https://raw.githubusercontent.com/steig/skills/main/skills/view-driven/SKILL.md
curl -o ~/.claude/skills/map-driven/SKILL.md \
  https://raw.githubusercontent.com/steig/skills/main/skills/map-driven/SKILL.md
```

Then in Claude Code: `/schema-driven` to start the interview, or just describe a
non-trivial system you're about to build and it should offer.

## Status

All three evolve as I use them — the "lessons baked in" sections come from real failures on my
own systems. Issues and corrections welcome; feature-sized opinions probably belong in
your own fork, since the whole point is that the methodology stays small enough to argue
with.

## License

MIT
