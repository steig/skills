# What herdr and worktender can do across repositories today

Resolves [#2](https://github.com/steig/skills/issues/2), child of map
[#1](https://github.com/steig/skills/issues/1) (global fleet-coordinator skill).

Audited 2026-08-24 against:

- installed `herdr` 0.8.0 (protocol 20, live server on this machine) — `--help`, `--skill`, and one read-only live probe
- installed worktender 0.9.1 (plugin root `/nix/store/nkcm0g93rlj7zdsskgkw24h9i8whh9r7-worktender-0.9.1`, pinned by `packages/worktender/default.nix` in nixos-config)
- source: [steig/worktender](https://github.com/steig/worktender) at v0.9.1 tip (`67c23f5`) — file:line refs below are into that tree
- [steig/herdrmux](https://github.com/steig/herdrmux) clone at `~/projects/herdrmux` (research docs, esp. `docs/research/herdr-headless-supervision.md`)
- the installed coordinator skill, `~/.claude/skills/coordinator/SKILL.md`

No live state was mutated: help output, source reading, and `ls`/`status`/`agent list` reads only.

## Works cross-repo today

### `worktender ls --all-repos --reports --json` — yes, verified live

`lsCommand` (`main.go:435-478`): with `--all-repos` it takes **no repository
session at all** — it dials herdr, calls `openRepositories(client)`
(`startup.go:81`), and lists every distinct repository herdr has a **worktree
workspace** open for. Runs from anywhere, including outside any repository.
JSON is grouped per repository (`internal/wt/ls.go:568`: `repositories` vs
`worktrees`, exactly one non-null); a per-repository failure is recorded on
that repo's `error` field and costs the others nothing.

`--reports` explicitly works across repositories — the source says so
(`main.go:454-457`): "the lookup is one herdr call on a pane herdr already told
us about, so there is no wrong repository to ask." Reports live as herdr pane
metadata, read back per pane.

Live probe on this machine (from `/tmp`, outside any repo): one document
covering **two repositories** — `~/projects/shopcrm` (20 worktrees) and
`~/projects/boring` (1) — each row with `agent_status`, session-wide
`agent_status_seq`, and `report`.

The one refusal: `--pr` cannot combine with `--all-repos` (`main.go:461-463`) —
the PR lookup is one serial `gh` call per branch scoped to a single repository.

### `gate --any` across repositories — yes, by construction

`gateCommand` (`gate.go:144-161`): "It takes no repository lock and needs no
invocation context, but it does need herdr." Targets are herdr **agent names or
pane IDs**, and herdr's agent namespace is session-global — so
`gate --any <agent-in-repo-A>,<agent-in-repo-B>` resolves both against the same
session with no repo concept anywhere in the code path. Exit codes
(0 released / 3 blocked / 4 timeout-or-died / 1 unresolvable / 2 machine) are
repo-agnostic; `--json` names which target released.

### `worktender start` against a repo other than the cwd — yes, `--repo <path>`

`start.go:40,63-74`: `--repo` wins outright over herdr's injected context
(`newSessionIn`, `main.go:241-270`, resolves the named path to a repo root and
never falls back). The whole pipeline then runs against that root:

- issue fetch: `issueFor` (`start.go:371`) runs `gh issue view` with
  `cmd.Dir = root` **and** `--repo <origin remote URL>` — pinned to the right
  GitHub repo, not the caller's.
- worktree creation: `client.WorktreeCreate(s.root, ...)` — herdr's own
  `worktree create` takes the location explicitly (CLI: `--cwd <PATH>`), so
  herdr is repo-agnostic here too.
- `prune` / `prune-apply` take the same `--repo` flag. Added in 0.8.0 after a
  live incident: a dry run inside one repository planned against a different
  project's checkout (comment on `newSessionIn`).

### Repository-digest agent namespace — the collision problem is solved

`internal/reconcile/names.go:64-82`: agent name = truncated slug + `-` + first
6 hex chars of `sha256(resolved repo root + "\x00" + slug)`, inside herdr's
32-char limit. herdr's namespace is global and **refuses** duplicates
(`agent_name_taken`, measured against protocol 18), so without the digest two
repos with issue #12 each would break; with it, names are fleet-safe.
Verified live: `herdr agent list` shows digest-suffixed workers from multiple
repos flat in one namespace (`wt-372-hand-written-comma-c7a1c4`, ...).
`start --json` / `dispatch --json` return `agent_name` and a ready
`gate_command` so a controller never re-derives the digest.

### `--permission-mode` passthrough — yes, on both `start` and `dispatch`

`dispatch.go:111-143` (`agentArgsFor`, shared by `start.go:137`): the mode is
appended verbatim to the agent args. `bypassPermissions` and `acceptEdits` get
a stderr warning, never a refusal: worktender cannot sandbox (`claude` takes no
sandbox flag; the plugin does not write agent config), so the boundary — a
sandbox profile or separate uid — is the caller's to provide. Nothing here is
repo-scoped; it works identically wherever the pane is.

### herdr primitives are repo-agnostic throughout

Panes/agents are addressed by opaque IDs (`w5:p1`) or global names; `agent
prompt|wait|read|get`, `pane run|read|wait-output` carry no repository concept.
`worktree create` names its repo via `--cwd`. Nothing in `herdr --skill` or the
CLI help assumes one repository.

## Missing or single-repo for fleet use

1. **Fleet scope = "repos herdr has a worktree workspace open for", nothing
   more.** `openRepositories` (`startup.go:81-105`) derives roots only from
   workspaces herdr reports as worktrees; a repository with no open worktree
   workspace is invisible to `ls --all-repos`, `startup`, and `doctor`. There
   is **no discovery** of repos a controller *could* staff — `start --repo`
   needs a path the caller already knows, and nothing maps a GitHub issue to
   its local checkout.
2. **No cross-repo PR view.** `--pr` is refused with `--all-repos`; verifying a
   `done` means a per-repo `gh` call the controller runs itself. Since reports
   are in-flight only (pane metadata dies with the pane — deliberate,
   CHANGELOG 0.9.0: "`ls` is a projection over git and herdr, not a database"),
   PRs are the *only* durable record, and they have no fleet-wide surface.
3. **`sync` has no `--repo`.** `main.go:533`: `newSession(false, herdrRequired)`
   — it reconciles only the repository of its invocation context. Multi-repo
   reconcile exists only as `startup` (all open repos, one pass each, gated by
   the `WORKTENDER_EVENTS` opt-in) or per-repo event hooks.
4. **One herdr session is the fleet boundary.** Every command dials the current
   session's socket (`dialHerdrIfPresent`). Agents in other named sessions or
   on other machines don't exist to `ls`/`gate`; `herdr --remote` is TUI
   attach, not a CLI federation surface (herdrmux
   `herdr-headless-supervision.md` shows the daemon driven remotely via
   `remote-client-bridge`/`terminal session control`, but that is pane-level
   plumbing, not a fleet API).
5. **Gate is a blocking single-release wait.** `--any` releases once; the
   controller loops "gate, act, re-gate on the rest" (coordinator SKILL.md).
   No subscription/callback; default timeout 15m, no indefinite wait.
6. **`dispatch --name` is caller-chosen.** Only `start`/`sync` derive
   digest-safe names; a controller hand-dispatching across repos must avoid
   global collisions itself (or reuse `AgentName`'s scheme).
7. **The coordinator skill self-scopes to one repo's flow.** It already teaches
   `ls --all-repos --reports --json` for coming back after a clear, but its
   framing ("worktender's own agents... not a general orchestration framework"),
   verification examples (`go test` in *the* repo), and stacking/merge-order
   guidance all assume one repository's slices. A fleet skill sits above it,
   not inside it.
8. **Autonomy at fleet scale has no boundary story.** `--permission-mode`
   passes through with a warning only; sandbox/uid isolation is external per
   worker, and nothing provisions it per repo.

## Bottom line

The mechanics a fleet controller needs already work cross-repo and are
deliberate, recent (0.8.0–0.9.0) features: global digest-named agents, fleet
listing with reports from anywhere, repo-parameterised `start`/`prune`,
repo-free `gate --any`, permission-mode passthrough. What's missing is the
layer above: repo discovery/registry (issue → checkout), a cross-repo PR/done
verification surface, multi-repo `sync`, anything spanning sessions or
machines, and a coordinator doctrine written for N repos instead of one.
