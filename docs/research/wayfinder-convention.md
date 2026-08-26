# The Wayfinder convention, extracted from its two exemplars

> Wayfinder originates as [Matt Pocock's `wayfinder` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/wayfinder)
> (MIT). This doc codifies the convention *as practiced* in two local maps, which may
> extend or diverge from his upstream skill.

Resolves steig/skills#24. Sources read in full: the **GitHub-issues exemplar**
(steig/herdrmux — map issue [#1](https://github.com/steig/herdrmux/issues/1), twelve
tickets sampled across `wayfinder:research` / `wayfinder:grilling` / `wayfinder:task`
(#2, #8, #10, #12, #13, #15, #16, #19, #29, #35, #38, #39), the full merged-PR list
#18–#43, the label set, and the local clone's `CONTEXT.md` and `docs/research/`), and
the **local-markdown exemplar** (eoscrusher `docs/wayfinder/personal-workspace.md`,
whole file). Every claim below cites where it was observed. Where the exemplars
disagree, the divergence is pulled out into §5 rather than silently averaged.

**One negative finding up front:** the `wayfinder:prototype` label exists in herdrmux
(five `wayfinder:*` labels are defined: `map`, `research`, `grilling`, `task`,
`prototype`) but **zero issues carry it**, and the eoscrusher map has no prototype
ticket either. The prototype type is declared, never exercised — §2.4 records what can
and cannot be inferred about it.

---

## 1. The map lifecycle

Five phases are observable: **charting → frontier work → redraw → frontier clear →
build-route handoff**. herdrmux is a live map mid-frontier (25 of 26 sub-issues
complete, map still OPEN); eoscrusher is a finished map that ran the whole arc to
SHIPPED. Between them the full lifecycle is visible.

### 1.1 Charting

A map is born with a **Destination**, a set of **settled constraints**, a body of
**carried-in decisions**, and a **fog list** — before any ticket is worked.

- **Destination** states the end state and, critically, the map's own done-condition:
  herdrmux #1: *"The map is done when every architectural decision below is settled and
  the first build slice is specified. Building is downstream of the map."* eoscrusher
  puts scope-cuts right in the Destination section (*"Out of scope (this map): …"*).
- **Settled at charting** (herdrmux #1) is a numbered list of standing constraints —
  *"standing constraints for every session, not steps on the route"* — e.g. constraint
  8, "Subscription accounts only. No Anthropic API key." The numbering matters: later
  material refers to "constraint 3", "constraint 9" by number.
- Charting inherits from a prior grill: eoscrusher's trunk is explicit — *"Decisions so
  far (locked trunk — carried in from the grill)"*, D1–D5 predating every ticket.
- **Fog**: herdrmux #1 keeps a "Not yet specified" section. Items *graduate* from fog to
  ticket when they become live — #35's body opens *"Graduated from the fog"*, #10's
  *"Graduated from the fog once #3 sized the change"* — and resolutions can push items
  *back* into fog (#12: *"Recorded as fog on the map rather than a ticket, since the
  sharper question only exists once the lag has been felt"*).
- The map issue also carries **Notes** (domain, reference table with licenses/roles,
  which skills each session should consult), **Measured facts, do not re-derive**
  (§3.4), **Flagged, not technical** (a commercial/legal risk called out at map level
  *"rather than buried in a ticket"*), and **Out of scope**.

### 1.2 Frontier work

Sessions burn down the ticket frontier. The observable mechanics in herdrmux:

- Every ticket is a **native GitHub sub-issue of the map** (`parent: steig/herdrmux#1`
  on every sampled issue; the map's sub-issue summary reads 25/26 complete).
- **blocked-by / blocking edges are native GitHub issue relationships**, and they encode
  research-feeds-decision: research #39 shows `blocking: #15`; grilling #15 shows
  `blocked-by: #39, #20`; grilling #9 shows five blockers (#14, #13, #8, #4, #2).
  Ticket bodies restate the edge in prose ("Blocks #7", "Depends on #16 only if…").
- Each resolution **writes back to the map**: a per-ticket entry in "Decisions so far"
  (`<!-- one line per closed ticket -->`), plus updates to Measured facts. Closing
  comments on late tickets say it outright: #16, #35, #15 all end *"Decision line on
  #1."* CONTEXT.md confirms the division of labor: *"mechanism lives in
  `docs/research/`, and decisions live on the map (#1)."*
- Resolutions may **invalidate standing map facts**, and the map is corrected rather
  than left stale: #19's resolution has a section titled "This invalidates a standing
  map fact"; the map's measured-facts list then carries the withdrawal inline (*"The
  original claim that it needs none is withdrawn"*; on `pane.report_agent`: *"withdrawn
  as a fact about anything here"*). Corrections are appended as dated sub-bullets naming
  their source (#10's decision entry: *"**Correction (2026-08-16, from #36):** the fork
  point is `v1.5.0`, a stable tag, not `v1.5.0-beta.945` … The earlier check missed it
  because `git tag --sort=creatordate` ordered the beta after the stable"*).
- Frontier work spawns follow-up tickets: #12's resolution *"graduates the map's 'Which
  layer reports agent state' fog into its own ticket"* (→ #14).

### 1.3 Redraw

The redraw protocol is best seen on herdrmux Settled-at-charting item 3, redrawn
2026-08-19 (originally "multi-provider routing is a headline feature" with dynamic
rate-limit failover; now "Multi-account, statically bound — no automatic account
switching"). How it was recorded and propagated:

1. **Edited in place, original preserved.** The constraint keeps its number and slot;
   the new text opens with *"(Redrawn 2026-08-19; originally 'multi-provider routing is
   a headline feature' with dynamic rate-limit failover in scope.)"* — date, plus enough
   of the old text to reconstruct what changed.
2. **Rationale recorded in the constraint itself**: *"Redrawn because dynamic switching
   carried the map's one existential risk — pooled accounts read as limit arbitrage,
   static work/personal separation is ordinary use — and most of #9's unresolved
   design."*
3. **Reversibility argued, not assumed**: *"Reversible by construction: the
   `CLAUDE_CONFIG_DIR` binding mechanism is identical in both worlds, so failover added
   later is a scheduler, not an architecture change."*
4. **Propagated to affected map sections**: the "Flagged, not technical" risk gets an
   *"Update 2026-08-19: constraint 3's redraw defuses most of this … The question is not
   closed, but it is no longer load-bearing"* note appended below the original.
5. **Propagated to affected open tickets by comment, not silent closure**: task #13 got
   the 2026-08-20 comment *"Downgraded by the redraw of constraint 3 (2026-08-19): with
   no automatic switching there is no scheduler reading the refusal envelope … Leaving
   open as a someday-task."* — the ticket stays OPEN, demoted off the route.
6. **Later resolutions cite the redraw as an input**: #9's decision entry opens *"most
   of this ticket's original design space was removed by constraint 3's redraw."*

So a redraw is an **in-place dated edit with the original text kept, a recorded reason,
a reversibility argument, and explicit fan-out** to every section and ticket the old
constraint was load-bearing for. Nothing is deleted; things are annotated.

### 1.4 Frontier clear

Only eoscrusher shows this phase. When the last ticket resolves, the decisions log gets
a terminal entry: *"2026-07-14 — ✅ **Frontier clear (8/8).** Destination reachable; map
hands off to the build route below."* herdrmux, at 25/26 with #13 demoted to
someday-task, has **not** declared frontier clear and keeps "First build slice.
Deliberately last." in its fog — sequencing the build is itself the last map question.

### 1.5 Build-route handoff

eoscrusher's "🚦 Build route (map → implementation)" section: *"The map is a plan; these
are the deliverable steps, in order. Each is gated by `just ci`."* Seven ordered,
✅-marked, dated steps (ARD → spec-change → gen/migration → service → web → gate
→ review+fixes); steps cite their constraining source where one exists (step 3's
migration check is "T5 check clean", step 4 "per T3", step 1 cites grill decisions
D1–D6) but most steps carry no ticket citation. The map header is then stamped (*"✅ SHIPPED (v1) … Route: ARD ✅ →
spec ✅ → …"*) and a **"Deferred (not v1)"** list records scope consciously cut, each
item with its constraining ticket ("share notifications (needs owner-scoped notify
path, T7)"). The build route lives *inside the map document* but below a hard line: the
map plans, the route builds, and route steps are deliverables while tickets never are.

---

## 2. Ticket anatomy by type

Common to every type (both exemplars): the body opens with a **`## Question`
heading / `**Q:**` line** — tickets are phrased as questions, not work items
("Does the Mac ever own a PTY?", "What reaps a session the app has forgotten?"); edges
to what the answer blocks or depends on; and a resolution that names what it unblocks.

### 2.1 `wayfinder:research` (≈ eoscrusher AFK)

An agent can resolve it by investigation; no live human judgment required.

**Required fields, observed in #2, #19, #29, #38, #39:**
- *Why it matters / what it blocks* — first line after the question: "Blocks #7, which
  cannot pick a data model without knowing what the source data actually looks like"
  (#19); "Everything downstream hangs on this" (#2).
- *The claims at stake* — #19 lists the two map claims "established by inference, not by
  reading one" that the research must test.
- *Enumerated sub-questions* — sampled research tickets list 4–6 concrete probes
  ("Schema. … Size and growth. … Write pattern. … State the sample size."), usually
  numbered (#2's four are unnumbered bullets).
- *Prescribed output location and shape* — "Record findings in
  `docs/research/claude-transcript-shape.md`, following
  `docs/research/muxy-fork-divergence.md` for shape" (#19; same formula in #29, #38,
  #39). One existing doc is the canonical shape reference for all later ones.
- *Scope guardrails* — an explicit do-not line separating evidence from decision: "**Do
  not design the bus** — that is #7's decision, and this ticket supplies its inputs"
  (#19); "**Do not recommend a reaping policy** — that is #15" (#39); "Answer with the
  evidence, not a judgement — the routing decision is a separate ticket" (#2).
- *Safety constraints where relevant* — #29: "**Hard constraint: do not exhaust,
  degrade, or meaningfully spend any account**"; #39: "Do not kill any process you did
  not start."
- *Epistemic standard* — "Numbers and rerunnable commands, not impressions" (#39);
  "Every claim gets a rerunnable command or a file and line" (#38); "An idle agent and
  an idle shell may be indistinguishable, which is itself the answer — do not stretch a
  weak signal into a strong one" (#39).

**Resolution:** a PR that "Resolves #N" lands the evidence file in `docs/research/*.md`
(PRs #18, #22, #25, #26, #30, #40, #43 all follow this shape), the map gains a
decisions-so-far entry, and — on the early tickets — a full answer is also posted as
the **closing comment** (#2, #19). The closing comment leads with the headline
("**Answer: yes — and by a better route than the one we were looking for**"), carries
real captured output, states negative results and untested things plainly ("Stability
could not be tested, and that was reported rather than papered over"), includes a
**Verification** section re-checking the worker's claims independently (#19: "Checked
independently of the worker that produced it"), and ends with what it unblocks.
Follow-up correction PRs are normal and named as such (#23 "Correct the screen
autodetach default…", #31 "Correct the allowance term: it is readable, not invisible").
Later research tickets (#29, #37, #39) closed **with no comment at all** — resolution
lives only in the merging PR + map entry + doc (see divergence §5.3). #38 closed with a
literal `"-"` comment and its prescribed `session-mapping-sites.md` never appeared in
`docs/research/` — if its findings survive anywhere it is the map's measured-facts
(the `MUXY_PANE_ID` join-key item matches #38's question, though that fact cites
#19/#21, so the attribution is plausible, not attested). The convention wobbles here;
a skill must pin it.

### 2.2 `wayfinder:grilling` (≈ eoscrusher HITL)

A decision requiring live human judgment, worked as an interview/stress-test (the map's
Notes name the skills: "Skills every session should consult: `grilling` and
`domain-modeling`").

**Required fields, observed in #8, #10, #12, #15, #16, #35:**
- *The decision space laid out as options with their costs* — #12 gives "Option A /
  Option B … mutually exclusive per pane"; #16 gives the two worlds as bullets; #10
  gives three candidate policies.
- *The facts that bear on it, cited to the research that established them* — #12: "The
  facts that bear on it, established in #2 and #3", then a bullet list each anchored to
  a finding.
- *Where the output goes* — #8: "Whatever comes out of this goes in `CONTEXT.md` as the
  glossary for the whole project."

**Resolution:** a closing comment that leads with the decision in bold ("**Answer:
Option A — raw PTY bytes from a Linux-ported `muxy-session`; the undocumented frame
channel is not used at all**"), then the argument, the named-and-accepted costs ("Named
cost, accepted unmarked: …" in #16's map entry), what stays provisional and what would
reopen it (#12: "**This one is provisional.** Revisit if a ~10Hz poll proves too
laggy"), and what it unblocks ("Unblocks #10 and #11"). Two recording styles exist in
sequence: early grillings (#8, #10, #12, all 2026-08-16) carry the **full decision as
the closing comment**; late ones (#15, #16, #35, 2026-08-20) leave a **summary comment
pointing at the map** ("Decided on the map: … Decision line on #1.") with the full text
living in #1's Decisions-so-far. When a grilling mints vocabulary, a PR lands it in
`CONTEXT.md` (#28 for #8; #33 for #14; #41 for #34 — "The decision itself is the
resolution comment on the issue and a line on the map; this PR carries the vocabulary
it produced").

In eoscrusher, HITL tickets (T1, T2, T6) are structurally identical to AFK ones but may
end with a "**Recommendation to react to:**" block (T6) — the agent proposes, the human
disposes.

### 2.3 `wayfinder:task`

Exactly one instance: #13 "Capture a real rate-limit envelope". It is **manual human
work producing evidence, not a decision**: *"This is manual work, not a decision.
Exhaust a quota … capture the full event sequence and the final envelope verbatim."*
Required fields mirror research (why it matters, what is/isn't confirmed) plus a
verbatim-output requirement: *"Record the raw JSON in the answer — later tickets will
read the field names off it, so paraphrase is not enough."* Its lifecycle also shows
tasks are **demotable**: research #29 was spun up expressly to shrink it ("Blocks #13,
and may answer it outright"), answered most of it for $0.058, and the redraw then
downgraded #13 to "optional curiosity … Leaving open as a someday-task" — still OPEN
against a 25/26-complete map. A task's output lands in the ticket thread itself (raw
capture), not necessarily in `docs/research/`.

### 2.4 `wayfinder:prototype`

Label defined in herdrmux (`#5319E7`), **zero instances in either exemplar**. The only
external anchor is the `prototype` skill in this ecosystem ("Build a throwaway
prototype to answer a design question"), which rhymes with the convention's
tickets-resolve-questions rule — a prototype ticket would answer a design question with
a throwaway build rather than with reading or interviewing. But required fields,
resolution protocol, and output location are **unattested**. A skill encoding the
convention must either define this type from first principles (question + guardrail
that the prototype is discarded + where the finding lands) or ship it as reserved.

---

## 3. Rules stated in exemplar prose

These are the load-bearing sentences, quoted, because the skill should encode them
rather than paraphrases of them.

### 3.1 One HITL ticket per session; AFK exempt

eoscrusher header: *"A session resolves **at most one HITL ticket** (AFK/research
tickets excepted), records the answer as a resolution line, checks the box, and appends
a pointer to Decisions so far."* Stated **only** in the markdown exemplar; herdrmux
prose nowhere repeats it, and its closure timestamps do not independently support it
(#11 and #12 closed 20 minutes apart on 2026-08-16; #15, #35, #9, #7 within 26 minutes
on 2026-08-20 — consistent with batch-closing after separate sittings, but the
artifacts cannot show session boundaries either way). Likewise eoscrusher's three
same-day HITL resolutions attest dates only, not sessions. **The rule is attested as
stated prose, not as observed behavior** — a skill adopts it as a prescriptive pacing
choice, not because the exemplars prove it was followed.

### 3.2 Maps plan, don't build

Both exemplars, independently phrased. eoscrusher: *"It **plans, it doesn't build**."*
herdrmux #1: *"Building is downstream of the map."* Corollary in eoscrusher's route
header: *"The map is a plan; these are the deliverable steps."*

### 3.3 Tickets resolve questions, not deliverables

eoscrusher: *"Each ticket resolves **a question**, not a deliverable."* herdrmux
enforces it structurally — every ticket body opens `## Question`, titles are
interrogative, and research tickets carry explicit do-not-decide guardrails (§2.1). The
inverse boundary also holds: deliverables live on the build route or in PRs, never as
tickets.

### 3.4 Measured facts, do not re-derive

herdrmux #1 keeps a map-level section literally titled *"Measured facts, do not
re-derive"* — ~30 bullets of empirical findings (byte counts, verified session-UUID
joins, env-var precedence), each stated as fact with its measurement context, corrected
by explicit withdrawal when falsified (§1.2). The section is the map's cache of
expensive observations so no session repeats a probe. eoscrusher has no such section;
its equivalent discipline is file:line citations inside resolutions ("`authz.ts:20-22`",
"`tool_registry.json:9639`", "Exact precedent: `migrations/0052_boring_mandrill.sql`").

### 3.5 Append-only decisions log

eoscrusher: section titled *"🗺️ Decisions log (append-only)"* — dated one-liners, one
per event, ending with the frontier-clear entry; nothing above it is ever rewritten.
herdrmux's analogue, "Decisions so far" on #1, honors append-only in spirit — earlier
entries are corrected by **appending dated correction sub-bullets**, never by rewriting
(#10's fork-point correction, #11's device-inventory correction) — but it is per-ticket
and undated at the entry level (see divergence §5.4).

### 3.6 Secondary rules worth encoding

- **Epistemic honesty is mandated in ticket text**: "do not stretch a weak signal into a
  strong one" (#39); "reported rather than papered over" (#19); recorded-as-provisional
  markers ("recorded as provisional, not fact" — #9's transcript-carry).
- **Evidence and decision are separated by construction**: research supplies inputs,
  a different ticket decides (#19/#7, #39/#15, #29/#13, #2's "the routing decision is a
  separate ticket").
- **Independent verification**: resolutions get checked by a second pass (#19's
  "Verification" section; PRs #23/#24 exist purely as verification-pass corrections).
- **Named costs are accepted explicitly, not silently**: "Named cost, accepted
  unmarked" (#16); "a limitation taken knowingly" (#35); eoscrusher's "**Accepted
  tension:**" block (T1).
- **Glossary discipline**: cross-ticket vocabulary lands in `CONTEXT.md` ("This is the
  glossary for the whole project. It defines what terms mean, not how anything is
  built"), with *Avoid:* anti-term lists per entry.

---

## 4. Where things land — the full artifact table

| Artifact | herdrmux (GitHub backing) | eoscrusher (markdown backing) |
|---|---|---|
| Map | Issue #1, `wayfinder:map` label | `docs/wayfinder/<name>.md` |
| Ticket | Sub-issue of #1, typed by label | `### ☐/☑ Tn · title · HITL/AFK` section |
| Type marker | 5 labels (`map`/`research`/`grilling`/`task`/`prototype`) | HITL/AFK legend + checkbox |
| Edges | Native blocked-by/blocking + parent sub-issue | Prose: "→ informs Tn", "per T3", "→ gate for T-spec" |
| Resolution | Closing comment (early) / map decision line (late) / merging PR | "**Resolution (date):**" line in the ticket section |
| Research evidence | `docs/research/*.md` via a "Resolves #N" PR | Inline in the resolution, file:line citations |
| Decisions log | "Decisions so far" on #1, one entry per closed ticket | "Decisions log (append-only)", dated one-liners |
| Glossary | `CONTEXT.md` at repo root | — (none) |
| Measured facts | Map section "Measured facts, do not re-derive" | — (inline citations instead) |
| Fog / deferral | "Not yet specified" + "Out of scope" on #1 | "Out of scope" in Destination + "Deferred (not v1)" |
| Build route | Not yet reached (deliberately last fog item) | "🚦 Build route" section in the map file |

---

## 5. Divergences the skill must resolve or delegate

Each item below is a real disagreement between the exemplars. For each: what each side
does, and whether a skill should **pick a side** or **delegate to the backing store**
(feeds steig/skills#21).

1. **Where the decisions log lives and what shape it has.** herdrmux: per-closed-ticket
   entries on the map issue, undated at entry level, corrected by appended dated
   sub-bullets. eoscrusher: a separate dated append-only one-liner log, *plus* a
   distinct "Decisions so far (locked trunk)" for grill-inherited decisions, *plus* the
   full resolution living in the ticket section. **Delegate the location** (it follows
   the backing store) **but pick the invariants**: append-only, dated, one entry per
   resolution event, corrections appended never rewritten.

2. **Where a resolution is recorded.** herdrmux itself is internally split (full
   closing comment on 2026-08-16 tickets; "Decided on the map … Decision line on #1"
   stub on 2026-08-20 tickets; no comment at all on PR-closed research #29/#37/#39; a
   bare `"-"` on #38). eoscrusher: always a resolution line inside the ticket section.
   **Pick a side**: the late-herdrmux shape is the trajectory the author converged on —
   canonical decision text lives on the map, the ticket gets at minimum a pointer
   comment, and silent closure (#29/#38-style) should be prohibited: a ticket with no
   resolution text of its own forces readers to diff the map to learn its answer.
   > **Superseded 2026-08-25 by steig/skills#21:** the map settled this differently —
   > canonical decision text lives in the **in-repo markdown log** (split-by-role),
   > resolutions recorded twice (full closing comment + log line). The silent-closure
   > prohibition survives as the "closed ticket with no log line" check.

3. **Where research evidence lands.** herdrmux: `docs/research/*.md` in-repo, delivered
   by a PR that closes the ticket, all docs following one canonical shape file
   (`muxy-fork-divergence.md`). eoscrusher: no research docs at all — evidence is
   compressed into the resolution with citations. **Pick a side conditioned on size**:
   prescribe `docs/research/*.md` whenever the backing is a repo and the evidence
   exceeds what a resolution comment holds; the "following X for shape" formula is
   worth encoding verbatim since it is how herdrmux keeps nine docs uniform. Also
   encode #38's failure mode as a check: a research ticket that prescribes a doc path
   must not close without that doc existing.

4. **How edges are represented.** herdrmux: native GitHub blocked-by/blocking relations
   plus parent/sub-issue attachment — machine-queryable, and the "Unblocks #N" line in
   resolutions mirrors them. eoscrusher: prose cross-references ("→ informs T2, T4"),
   which express *informs* (soft, output-feeds-input) but never *blocks* (hard,
   cannot-start). **Delegate the mechanism, pick the semantics**: both directions
   (blocked-by for hard ordering, informs for soft) must exist in any backing;
   markdown backing needs an explicit syntax for blocked-by that eoscrusher lacks.

5. **Ticket typing.** herdrmux: five labels; grilling/research/task/prototype under a
   map. eoscrusher: a two-value HITL/AFK legend. The mapping is grilling≈HITL,
   research≈AFK, and eoscrusher has no task or prototype at all — its build route
   absorbed what tasks would be. **Pick a side**: the label taxonomy is strictly more
   expressive and the HITL/AFK bit is derivable from it (grilling and task are HITL;
   research and prototype are AFK). Encode HITL/AFK as an attribute, the four types as
   the taxonomy. Prototype must be given a definition (§2.4) or dropped from the
   claimed set.

6. **Numbering and identity.** herdrmux: repo-global issue numbers shared with PRs
   (hence the non-contiguous 1–39 with PR gaps). eoscrusher: map-local T1…Tn plus
   pseudo-ticket names (T-spec, T-build) that were referenced before existing.
   **Delegate**: identity comes from the backing store; the skill only needs stable
   cite-ability and should ban forward references to tickets that are never created
   (eoscrusher's T-spec/T-build never appear as sections — they became build-route
   steps 2 and 4–6 — so the "→ gate for T-spec" references dangle).

7. **Map-level fact cache.** herdrmux's "Measured facts, do not re-derive" section has
   no eoscrusher counterpart. **Pick a side**: require it. It is where herdrmux's
   correction/withdrawal protocol operates, and it is the mechanism that makes the
   redraw auditable; eoscrusher got away without one only because its frontier lasted
   one day.

8. **One-HITL-per-session rule.** Stated only in eoscrusher's prose (§3.1); herdrmux
   never states it. **Pick a side**: state it in the skill, since it is the convention's
   only pacing rule and costs nothing where sessions are short.

9. **Where the build route lives and when the map closes.** eoscrusher: route is a
   section of the map file; map header mutates to SHIPPED; deferred list appended.
   herdrmux: route not yet reached; the map issue stays OPEN at 25/26 with an
   explicitly demoted someday-task open, and "first build slice" is itself the final
   map question. **Pick the sequencing rule** (frontier clear must be declared before
   any route step; route steps are gated deliverables; deferred list is mandatory at
   handoff) and **delegate the container** (route section in the map doc vs. a
   successor structure in the backing).
   > **Constrained 2026-08-25 by steig/skills#20 Settled-6:** the schema-mapped skill
   > keeps the build route *outside* the map entirely; the container question is
   > #27's (frontier-clear/handoff), not the backing's.

10. **Redraw fan-out surface.** herdrmux's protocol (§1.3) touches the constraint, the
    risk register, and open tickets by comment. eoscrusher never redrew (its trunk
    D1–D5 survived intact), so the markdown backing has **no attested redraw syntax**.
    **Pick a side**: encode herdrmux's protocol (in-place dated edit + original text
    preserved + reason + reversibility + fan-out comments) as the convention, and
    define its markdown projection (an *(Redrawn YYYY-MM-DD; originally …)* annotation
    plus a decisions-log entry).
