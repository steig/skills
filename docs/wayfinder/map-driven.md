# wayfinder:log — map-driven

> The **decision half** of the split-by-role backing decided in
> [#21](https://github.com/steig/skills/issues/21). Execution state (tickets, edges,
> labels, frontier) lives on the map issue,
> [steig/skills#20](https://github.com/steig/skills/issues/20). This file is the
> canonical, append-only record of what was decided; a closed ticket with no line here
> is a skipped resolution.

**Map:** [#20 — map-driven: SDD completeness on Wayfinder execution](https://github.com/steig/skills/issues/20)
**Created:** 2026-08-25 · **Status:** ✅ **FRONTIER CLEAR (7/7)** — declared 2026-08-26; hands off to the build route (draft `skills/map-driven/SKILL.md`)

---

## 🗺️ Decisions log (append-only)

- **2026-08-25** — Map charted; trunk Settled-1…6 recorded on #20 (SDD = what, Wayfinder = how/when; separate companion skill; layer order → ticket DAG; one-HITL-per-session pacing; validator failures spawn tickets; refuses single-sitting systems; maps plan, don't build).
- **2026-08-25** — [#22](https://github.com/steig/skills/issues/22) resolved (grilling): seeding = **provisional big-bang, agent-run** — charting files one AFK "seed the map" ticket; below-frontier tickets are `provisional` and re-posed at pickup; redraw propagation is lazy by construction. Rejected: naive big-bang, lazy.
- **2026-08-25** — [#25](https://github.com/steig/skills/issues/25) resolved (research): **triage table** — 7 layers default AFK, 3 HITL (ownership, permission semantics, compliance posture), verification derived-never-a-ticket; escalation AFK→HITL when the agent reframes instead of measures; downgrade HITL→AFK when the answer is greppable. → `docs/research/triage-table.md`.
- **2026-08-25** — [#24](https://github.com/steig/skills/issues/24) resolved (research): **convention codified** from herdrmux + eoscrusher — redraw = in-place dated edit with fan-out; `wayfinder:prototype` defined but never exercised (skill must define or reserve it); herdrmux drifted on resolution recording (3 tickets closed unanswered) → motivates a resolution-required check. → `docs/research/wayfinder-convention.md`.
- **2026-08-25** — [#21](https://github.com/steig/skills/issues/21) resolved (grilling): backing = **split-by-role** — execution state in GitHub issues, decision state in one in-repo markdown log per map (this file's pattern); resolutions recorded twice (closing comment + log line); markdown-only is the no-GitHub fallback. Rejected: issues-only, markdown-only default, two full adapters.
- **2026-08-25** — **Correction to the #25 entry** (adversarial verification of both research docs): the escalation exemplar was misattributed — herdrmux #10 predates #17 and came from charting; #10 ← #17 attests the *wiring*, not the AFK-births-grilling genesis, which is now marked **prescriptive**. Kit reclassified HITL-with-default (VDD: 3 HITL / 1 derived). The convention doc survived ~70 claims with zero wrong; its per-session-cadence evidence softened to labeled inference and two §5 recommendations marked superseded by #21/Settled-6. Both docs updated; correction comment on #25.
- **2026-08-26** — [#26](https://github.com/steig/skills/issues/26) resolved (grilling): validator = **continuous, maturity-gated, auto-spawning, one machine** — runs on every log append; checks arm when their source layers have no open tickets; failures auto-spawn tickets (triaged per #25; veto = close-with-written-reason); the seeder is the validator's coverage check (charting's big-bang seed = first run; redraw re-seed free). Checks: SDD's list verbatim + coverage, closed-without-log-line, prescribed-doc-missing, provisional staleness, chain termination. Unblocks #27.

- **2026-08-26** — [#23](https://github.com/steig/skills/issues/23) resolved (grilling): coupling = **own the projections, reference the interviews** (embed triage table/templates/check list; read sibling SKILL.mds for layer prompts — same plugin, single source); VDD = **same map** (V-rows seed when charting answers "has a frontend"; headless seeds none); name = **`map-driven`** (keeps the `*-driven` family idiom). Map + log renamed from working name `schema-mapped`.

- **2026-08-26** — [#27](https://github.com/steig/skills/issues/27) resolved (grilling): frontier-clear = **eligibility mechanical, declaration human** — criteria: all tickets resolved/closed-with-reason + validator green + deferred list written; a HITL session declares. Handoff = terminal synthesis entry in this log + **offered** (never auto-generated) SDD JSONs. ARD-needed seeds as a late-gated AFK ticket; ARD writing is build-route, outside the map. Last ticket — map eligible for frontier clear.

- **2026-08-26** — ✅ **Frontier clear (7/7), declared by Tom.** Synthesis — the `map-driven` skill, fully decided:
  - **Identity:** third companion skill in steig-skills; SDD's 11-layer completeness on Wayfinder's map execution. Refuses single-sitting-sized systems; maps plan, don't build.
  - **Charting:** one sitting → destination + trunk + map; **seeding is the validator's first run** — its coverage check auto-spawns the full ticket set per the triage table/templates (#22, #26), `provisional` below the frontier, re-posed at pickup.
  - **Backing:** split-by-role (#21) — issues carry execution (tickets, edges, labels); the in-repo `docs/wayfinder/<map>.md` log is the canonical decisions record; markdown-only is the no-GitHub fallback.
  - **Triage (#25):** SDD 7 AFK / 3 HITL / 1 derived, package HITL at the root; VDD rows on the same map (#23), 3 HITL / 1 derived; escalation both directions (AFK→HITL birth is prescriptive — no exemplar yet; HITL→AFK downgrade).
  - **Pacing:** one HITL ticket per session (prescriptive, adopted as design); AFK exempt and parallel.
  - **Validator (#26):** continuous on log append, maturity-gated, auto-spawning with close-with-reason veto; SDD's checks verbatim + coverage, closed-without-log-line, prescribed-doc-missing, provisional staleness, chain termination.
  - **Coupling (#23):** owns the projections (triage table, templates, check list); references the sibling SKILL.mds for interview content. Named **`map-driven`**.
  - **Close (#27):** eligibility mechanical, declaration human; handoff = terminal synthesis + offered (never auto-generated) SDD JSONs; ARD-needed = late-gated AFK ticket; build route outside the map.
  - **Deferred:** the AFK→HITL birth rule awaits a first real instance; `wayfinder:prototype` needs a definition or explicit reservation in the skill draft.

## 📌 Measured facts, do not re-derive

- The five `wayfinder:*` labels attested in the wild: `map`, `research`, `grilling`, `task`, `prototype` — `prototype` has **zero** uses across both exemplars (#24).
- herdrmux resolution drift: #29/#37/#39 closed with no resolution comment, #38 with a bare "-" and its prescribed research doc never landed (#24).
- The redraw precedent: herdrmux Settled-3, 2026-08-19 — in-place dated edit preserving original text, rationale + reversibility argument + explicit fan-out to citing tickets (#24).

## ⏭️ Open frontier

*(empty — eligible for frontier clear, awaiting declaration)*
