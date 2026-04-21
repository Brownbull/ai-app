# gabe-teach v2 — Streamlining Patch

**Target:** `~/.claude/commands/gabe-teach.md`
**Intent:** Make teaching the default action (not configuration). Unify action verbs. Add `retro` and `tour` teach modes. Plan-lineage in topic headers. Further-reading always-emit.

## Approved plan (from 2026-04-18 session)

Six dimensions of learning the human wants covered:

| Dimension | Current surface | Change in v2 |
|-----------|-----------------|--------------|
| Basics | `brief` mode | ✅ unchanged |
| Architecture | `arch` catalog + `story` mode | ✅ teach-first default (skip dashboard) |
| Why we plan / implement / commit | `topics` mode | ➕ plan+phase lineage in topic header |
| What went well / wrong / decision reasons | buried in Sessions + DECISIONS | ➕ new `retro` mode |
| Architect practice | `arch` catalog (30 concepts) | ✅ same catalog, teach-first routing |
| "How does this app work?" | scattered wells + STRUCTURE + DOCS | ➕ new `tour` mode |

Phases:

1. Teach-first defaults (Step 0 routing, Step 4c menu, Step 9 header, Step 9a demoted, Step 9f no pick prompt)
2. Universal 4-verb action menu (new Step 0.7; applied to Step 4d, 9c, 9d)
3. Further-reading load-bearing (rewrite in Step 4d-lesson)
4. Fill gaps: plan lineage (Step 4d header), new Step 10 `retro`, new Step 11 `tour`
5. Dogfood on ai-app (no doc changes — runtime verification)

---

## How to apply this patch

Each change block below has a `LOCATE` selector (an anchor string to find in the current file) and a `REPLACE WITH` body. Apply them in order. They assume the current file is the baseline that shipped before 2026-04-18's edits (which were all reverted by the parallel session).

If you have access to a reliable editor outside the conflicting environment, prefer:
- Open `~/.claude/commands/gabe-teach.md`
- For each CHANGE below, find the `LOCATE` block, replace it with the `REPLACE WITH` block
- Save

Or apply via sed/awk/patch if you prefer — each block's LOCATE is unique in the current file.

---

## CHANGE 1 — Frontmatter description (tiny)

**LOCATE** (line 2-3):

```
name: gabe-teach
description: "Consolidate the human's architect-level understanding of recent changes. Organizes topics under gravity wells (architectural sections). Detects WHY/WHEN/WHERE topics from commits, explains with analogies, verifies with Socratic questions, tracks in .kdbp/KNOWLEDGE.md. Also offers a cross-project architecture curriculum via /gabe-teach arch. Usage: /gabe-teach [brief|topics|status|wells|init-wells|history|story|arch|free]"
```

**REPLACE WITH:**

```
name: gabe-teach
description: "Consolidate the human's architect-level understanding of recent changes. Organizes topics under gravity wells (architectural sections). Detects WHY/WHEN/WHERE topics from commits, explains with analogies, verifies with Socratic questions, tracks in .kdbp/KNOWLEDGE.md. Teach-first: every invocation renders a lesson by default; config lives under explicit subcommands. Usage: /gabe-teach [brief|topics|status|wells|init-wells|history|story|arch|retro|tour|free]"
```

---

## CHANGE 2 — Add teach-first design principle paragraph

**LOCATE** (lines 8-10, right after the `# Gabe Teach` heading paragraph):

```
Countermeasure for "the human can't keep up with AI-paced changes." Keeps the human at architect-level understanding: WHY decisions were made, WHEN patterns apply, WHERE files belong. Topics are anchored to **gravity wells** (architectural sections of the app) so the human builds a map before individual details.

## Procedure
```

**REPLACE WITH:**

```
Countermeasure for "the human can't keep up with AI-paced changes." Keeps the human at architect-level understanding: WHY decisions were made, WHEN patterns apply, WHERE files belong. Topics are anchored to **gravity wells** (architectural sections of the app) so the human builds a map before individual details.

**Design principle — teach-first, config-last.** Every bare-ish invocation renders a lesson or narrative, never a dashboard. Dashboards, catalog browsing, wells editing, and history browsing all live behind explicit subcommands (`status`, `arch browse`, `wells`, `history`, `arch dashboard`). When the user invokes `/gabe-teach` with no clear configuration intent, pick the most relevant teaching surface and render it immediately. Ask the same four verbs everywhere so nothing has to be memorized: `[explain]` / `[next]` / `[test]` / `[skip]` — see the **Universal Action Menu** section below.

## Procedure
```

---

## CHANGE 3 — Rewrite Step 0 mode table with kind column and teach-first defaults

**LOCATE** (lines 12-34, the entire Step 0 section up to "If .kdbp/ doesn't exist..."):

```
### Step 0: Detect mode

Parse `$ARGUMENTS`:

| Mode | Purpose |
|------|---------|
| `brief` | Newcomer-onboarding snapshot: app purpose + wells overview + recent activity |
| `topics` (default when `.kdbp/` exists) | Session-aware teach loop over recent changes |
| `status` | Show KNOWLEDGE.md summary per well + history timeline |
| `wells` | List/edit wells (rename, merge, archive, view topics per well) |
| `init-wells` | Run the wizard to define gravity wells |
| `history` | Full timeline — plans, phases, commits, sessions, topics |
| `history full` | Unbounded history (default shows last 10 sessions + last 5 plans) |
| `story` | Show cached Storyline, or generate if missing |
| `story refresh` | Force regeneration of Storyline |
| `arch` | Architecture curriculum dashboard — tier × specialization map of verified/pending concepts |
| `arch browse [tier\|spec]` | List concepts from the `gabe-arch` skill, filterable |
| `arch show <concept-id>` | Teach one architecture concept via the 6-part lesson template |
| `arch verify <concept-id>` | Mark a concept as already-known (prompts quick-check or skip-check) |
| `arch next` | Pick the next concept via progressive-pressure rule (project → adjacency → foundation-gap) — ships in Phase 6 |
| `free [concept]` | Raw analogy generation (invokes `gabe-lens` skill) |

If `.kdbp/` doesn't exist: fall back to `free` with a note: "No KDBP detected. Running in free mode. Run `/gabe-init` to enable knowledge tracking."
```

**REPLACE WITH:**

```
### Step 0: Detect mode

Parse `$ARGUMENTS`:

| Mode | Kind | Purpose |
|------|------|---------|
| _(empty)_ | teach | **Default.** Auto-route: if pending project topics exist → `topics`; else → `arch next`; else → `retro`; else → print "you're current" one-liner. Never shows a dashboard first. |
| `topics` | teach | Session-aware teach loop over recent project changes |
| `arch` | teach | Alias for `arch next` — picks and teaches the next concept immediately (NOT the dashboard) |
| `arch next` | teach | Pick the next concept via progressive-pressure rule (project → adjacency → foundation-gap) and teach it directly |
| `arch show <id>` | teach | Teach one architecture concept via the 6-part lesson template |
| `retro` | teach | Retrospective teach: skipped topics + superseded decisions + what-went-wrong lessons |
| `tour` | teach | Newcomer tour: walks wells → paths → files → key decisions. Answers "how does this app work?" |
| `story` | teach | Show cached Storyline, or generate if missing (narrative analogy of the whole project) |
| `story refresh` | teach | Force regeneration of Storyline |
| `free [concept]` | teach | Raw analogy generation (invokes `gabe-lens` skill) |
| `brief` | orient | Newcomer-onboarding snapshot: app purpose + wells overview + recent activity |
| `status` | admin | Show KNOWLEDGE.md summary per well + history timeline (dashboard) |
| `arch browse [tier\|spec]` | admin | List concepts from the `gabe-arch` skill, filterable (catalog view) |
| `arch dashboard` | admin | Tier × specialization map of verified/pending concepts (the legacy `arch` rendering) |
| `arch verify <id>` | admin | Mark a concept as already-known (test-or-skip shortcut) |
| `wells` | admin | List/edit wells (rename, merge, archive, view topics per well) |
| `init-wells` | admin | Run the wizard to define gravity wells |
| `history` | admin | Full timeline — plans, phases, commits, sessions, topics |
| `history full` | admin | Unbounded history (default shows last 10 sessions + last 5 plans) |

**Routing rules:**

- **`teach` modes** render a lesson body and end with the Universal Action Menu. No dashboards, no config prompts mid-flow (except the foundation gate on first-ever run).
- **`orient` modes** render a snapshot; prompt with `[teach]` to drop into teach-first auto-routing.
- **`admin` modes** render a dashboard or editor; no lesson, no 4-verb menu.
- When ambiguous, prefer teach over admin. A user who wanted a dashboard can say so; a user who typed `/gabe-teach` and got a dashboard has been served the wrong thing.

If `.kdbp/` doesn't exist: fall back to `free` with a note: "No KDBP detected. Running in free mode. Run `/gabe-init` to enable knowledge tracking."
```

---

## CHANGE 4 — Insert new Step 0.7 Universal Action Menu

**LOCATE** (end of Step 0.5, right before `### Step 1: Status mode`):

```
This gate only fires once per project's lifetime — once wells exist, the gate passes silently.

### Step 1: Status mode
```

**REPLACE WITH:**

```
This gate only fires once per project's lifetime — once wells exist, the gate passes silently.

### Step 0.7: Universal Action Menu

Every teach-mode lesson (project topic, arch concept, retro lesson, tour stop) ends with the same four-verb menu. No mode-specific variants. Humans learn the controls once.

- **[explain]** — Re-teach from a different angle. Cheaper-model call, different analogy or deeper primary force. Does NOT change status. Use when the lesson didn't land.
- **[next]** — Answer Q1/Q2 now → classify (2/2 = verified, 1/2 = verified weak, 0/2 = pending) → auto-advance to the next lesson (same mode's next pick) or announce done.
- **[test]** — Skip the lesson body; jump straight to Q1/Q2 only. For humans who claim prior knowledge — this is the "sanity-check shortcut." 2/2 → `already-known (sanity-checked)` or `verified (verify-quick)` depending on mode.
- **[skip]** — Mark skipped (session-only for arch mode, persistent for project topics). Pick the next lesson. After 3 skips in one session, fall through to `status`.

**Mapping from legacy mode-specific verbs:**

| Legacy verb | Unified verb | Notes |
|-------------|--------------|-------|
| `verified` (correct on Q1/Q2) | `[next]` → scores 2/2 or 1/2 | Same write path to KNOWLEDGE.md / STATE.md |
| `pending` (wrong on Q1/Q2) | `[next]` → scores 0/2 | Same write |
| `skipped` | `[skip]` | Same write |
| `already-known` sanity-check | `[test]` | 2/2 classifies `already-known (sanity-checked)` |
| `quick-check` (Step 9d) | `[test]` | Q1 only, 1/1 → verified |
| `skip-check` (Step 9d) | `[next]` with no lesson rendered | Auto-scores `—/—`, writes `verified (verify-skip)` |
| `teach` / `cancel` | _n/a_ | Lesson renders by default; exit = no input |
| `view N`, `rename N`, `merge N M` | _Remain in `wells` admin only_ | Never in a teach lesson |

**Auto-advance on `[next]`:**

- From `topics` lesson: next pending candidate, else fall through to `arch next`.
- From `arch next` lesson: re-run Tier 1 → 2 → 3 rule; render new pick.
- From `arch show <id>` lesson: do NOT auto-advance. End with "Lesson complete. `/gabe-teach` for next."
- From `retro` lesson: next skipped/superseded, else "Retrospective clear."
- From `tour` stop: advance to next well, else "Tour complete."

**Shortcut keys:** `e` / `n` / `t` / `s` accepted as single-letter aliases. Case-insensitive.

### Step 1: Status mode
```

---

## CHANGE 5 — Rewrite Step 4c topics menu (teach-first, no menu by default)

**LOCATE** (Step 4c section, from `**Step 4c — Present menu, grouped by well.**` through the end of the section before `**Step 4d — Teach each selected topic.**`):

```
**Step 4c — Present menu, grouped by well.**

```
TEACH: Topics from recent changes

Commits covered: [N] since [date]
Active plan: [plan name], Phase [N] of [M]

  [0] BRIEF — Newcomer-onboarding snapshot (app purpose + wells overview + recent activity)
  [A] ARCH  — Architecture curriculum dashboard (tier × spec map, next-concept suggestion)

Guardrails (G1) — [N] pending
  [1] WHY   — Why guardrails run before the LLM
  [2] WHEN  — When to return matched pattern names vs boolean

API Layer (G3) — [N] pending
  [3] WHY   — Why 202 Accepted + BackgroundTask
  [4] WHERE — Why uploads/ lives at project root, not under app/

Frontend (G4) — [N] pending
  [5] WHY   — Why we expanded guardrails 15 → 25 patterns + sanitization

Pick up to 3:
  - Brief orient:  "0" (shows brief, then re-prompts for topic picks)
  - Arch view:     "A" (shows arch dashboard, then re-prompts for topic picks)
  - Individual:    "1,3,5" or just "3"
  - Whole well:    "all G1" or "all G3"
  - All pending:   "all"
  - Skip session:  "skip"
```

If user picks `0`: run the **short-brief** variant (Step 8 with `short` flag) inline, then re-show this menu. `0` is orientation, not a topic selection — it doesn't consume from the 3-pick cap.

If user picks `A` (case-insensitive, accepts `a` or `arch` too): run the **arch dashboard** (Step 9a) inline, then re-show this menu. Like `0`, `A` is orientation — it doesn't consume from the 3-pick cap. From the dashboard, the human can copy a concept ID and exit back to this menu, or run `/gabe-teach arch show <id>` in a separate invocation. We deliberately do NOT let `A` jump directly into a concept lesson — that would mix project-teach and arch-teach flows in one session, making the 3-pick cap accounting ambiguous.

**Short-brief:** wells block only (≈15 lines), no CONTEXT/OPEN & NEXT/RECENT sections, no COMMANDS footer. Keeps the topics menu flow tight. For the full brief, use `/gabe-teach brief` directly.

**Short-arch:** dashboard only (Step 9a's rendering, ≈20 lines) — tier progression bars + recent HISTORY.md events + one suggested-next concept. No interactive browse/show/verify from within the menu; those require exiting to `/gabe-teach arch <subcommand>`. Keeps the topics flow tight, same philosophy as short-brief.

**Gate bypass:** When `[0]` or `[A]` is invoked from inside the topics menu, Step 8's foundation gate (for brief) and Step 9's lazy-bootstrap (for arch) run silently. Step 0.5 already passed to reach this menu, so no re-prompting.

Cap: 3 topics per session (prevents quiz fatigue). Same deterministic counting as before.
```

**REPLACE WITH:**

```
**Step 4c — Pick the next lesson (teach-first, no menu by default).**

Fast path (default behavior, applies to ≥90% of invocations):

1. Sort pending candidates by recency (newest commit first), then by well with the fewest verified topics (fill in gaps), tiebreak alphabetical by well ID.
2. Take the top candidate and render its lesson via Step 4d. No menu, no selection prompt.
3. After classify, if more pending remain, auto-advance via `[next]` of the Universal Action Menu (Step 0.7).

Menu path (only when `/gabe-teach topics --menu` is invoked, or >5 pending candidates across ≥3 wells and user opted in):

```
TEACH: [N] topics pending across [K] wells

Commits covered: [N] since [date]
Active plan: [plan name], Phase [N] of [M]

Guardrails (G1) — [N] pending
  1. WHY   — Why guardrails run before the LLM
  2. WHEN  — When to return matched pattern names vs boolean

API Layer (G3) — [N] pending
  3. WHY   — Why 202 Accepted + BackgroundTask
  4. WHERE — Why uploads/ lives at project root, not under app/

Type a number to teach that one, or press [next] to start with #1 (default).
```

Cap: 3 topics per session (prevents quiz fatigue). Counted across `[next]` auto-advances. On reaching the cap: `Session complete — 3 topics covered. /gabe-teach to continue tomorrow.`

**No more in-flow `[0]` brief or `[A]` arch bypass.** They were context-switch hazards. If the human wants orientation, they invoke `/gabe-teach brief` explicitly; if they want an arch lesson, `/gabe-teach arch`. Topics mode stays focused on project topics.
```

---

## CHANGE 6 — Add plan-lineage to topic header (Step 4d)

**LOCATE** (Step 4d opening):

```
**Step 4d — Teach each selected topic.** Flow per topic:

1. **Topic header** — `T[N] (G[M] <Well>, <CLASS>) — <title>`
2. **📍 Code block** — where the work landed (deterministic, from the candidate record captured in Step 4b). See format below.
3. **Lesson body** — six-part structured template (see Step 4d-lesson below).
4. **Classify response** — verified / pending / skipped / already-known (with sanity check).
```

**REPLACE WITH:**

```
**Step 4d — Teach each selected topic.** Flow per topic:

1. **Topic header** — two-line format that names the origin of the change:
   ```
   T[N] (G[M] <Well>, <CLASS>) — <title>
        ← Plan: "<plan goal>" · Phase <N>/<M>: <phase name> · Commit <sha-short>
   ```
   Lineage lookup (deterministic, no LLM): for each commit SHA in the candidate record, match commit-date against PLAN.md (active) first, then `.kdbp/archive/*.md` (completed plans) by date range. Pick the plan+phase that owns that commit. If no match, render `← Plan: (unmapped) · Commit <sha-short>`.
2. **📍 Code block** — where the work landed (deterministic, from the candidate record captured in Step 4b). See format below.
3. **Lesson body** — six-part structured template (see Step 4d-lesson below).
4. **Classify response** — Universal Action Menu (Step 0.7). `[next]` → Q1/Q2 → classify; `[explain]` → re-teach; `[test]` → skip to Q1/Q2; `[skip]` → mark and move on.
```

---

## CHANGE 7 — Rewrite Further-reading to always-emit

**LOCATE** (inside Step 4d-lesson, the "Further reading construction" subsection; current text has rules 1/2/3 where rule 3 says "omit the Further reading: header entirely"):

```
**Further reading construction** (zero-LLM, deterministic):

1. If the topic's assigned well has a non-empty `Docs` path in `.kdbp/KNOWLEDGE.md`: emit a line `→ {Docs}  (well doc — N verified topics, last updated YYYY-MM-DD)`. Read the file's mtime for the date, count `### T[N] —` headings under `## Topics (auto-appended)` for N. If the file doesn't exist at that path, degrade to `→ {Docs}  (⚠ not found — run /gabe-teach init-wells to scaffold)`.
2. If `.kdbp/DOCS.md` maps any of the topic's changed files to documentation paths (existing drift-check mapping used by `/gabe-commit` CHECK 7): emit one line per mapped doc `→ {doc_path}  ({human-readable-label})`. Cap at 2 additional lines so the section stays tight.
3. If neither (1) nor (2) yields a line: omit the `Further reading:` header entirely — don't render an empty section.
```

**REPLACE WITH:**

```
**Further reading construction** (zero-LLM, deterministic, **always rendered** for project topics):

Per user feedback: lessons should always surface relevant support docs so the reader knows where to look for more depth. The section is load-bearing — it must render on every project topic lesson, even if content is sparse, so the human can navigate the documentation surface and see where gaps live.

1. **Well doc (always first, always present):** Look up the topic's assigned well in `.kdbp/KNOWLEDGE.md`:
   - Docs column non-empty AND file exists → emit `→ {Docs}  (well doc — N verified topics, last updated YYYY-MM-DD)`. Read mtime for date; count `### T[N] —` headings under `## Topics (auto-appended)` for N.
   - Docs column non-empty but file missing → emit `→ {Docs}  (⚠ not found — run /gabe-teach init-wells to scaffold)`.
   - Docs column empty → emit `→ (⚠ G[M] has no Docs path set — run /gabe-teach wells → [docs N] to assign one)`.
2. **DOCS.md mappings (up to 2 extra lines):** If `.kdbp/DOCS.md` maps any of the topic's changed files to documentation paths: emit one line per mapped doc `→ {doc_path}#{section}  ({human-readable-label})`. Cap at 2 additional lines.
3. **Never omit the header.** The `Further reading:` section always renders for project topics (Step 4d). For arch-concept lessons (Step 9c), the section is optional — the concept file's own `related:` frontmatter already provides cross-references.
```

---

## CHANGE 8 — Rewrite Step 9 arch-mode intro with teach-first routing

**LOCATE** (Step 9 opening paragraph):

```
### Step 9: Arch mode (architecture curriculum)

Enters when `$ARGUMENTS` starts with `arch`. Parse the subcommand: `arch` (dashboard), `arch browse [tier|spec]`, `arch show <id>`, `arch verify <id>`, `arch next` (Phase 6 — stub for now: print "coming soon" and fall through to `arch`).
```

**REPLACE WITH:**

```
### Step 9: Arch mode (architecture curriculum)

Enters when `$ARGUMENTS` starts with `arch`. Subcommand routing (teach-first):

| Subcommand | Routes to | Kind |
|------------|-----------|------|
| `arch` (bare) | Step 9f — pick next concept via progressive-pressure rule and **teach it immediately** | teach |
| `arch next` | Same as bare `arch` — pick + teach | teach |
| `arch show <id>` | Step 9c — teach specified concept | teach |
| `arch verify <id>` | Step 9d — test-or-skip shortcut (uses Universal Action Menu `[test]` / `[next]`) | admin |
| `arch browse [tier\|spec]` | Step 9b — catalog view, no teaching | admin |
| `arch dashboard` | Step 9a — tier × spec map with bars, no teaching | admin |

**Breaking change vs legacy:** bare `arch` used to show the dashboard. It now teaches. The dashboard moved to `arch dashboard`. Rationale: teaching is the common case; the dashboard was a landing page the user had to get past.
```

---

## CHANGE 9 — Rename Step 9a heading and add admin-mode note

**LOCATE** (Step 9a first two lines):

```
#### Step 9a — Dashboard (bare `arch`)

Read all concept files' frontmatter (tier, specialization, id, one_liner) and STATE.md. Render:
```

**REPLACE WITH:**

```
#### Step 9a — Dashboard (`arch dashboard`, admin mode)

_Admin surface, no teaching._ Used when the human explicitly wants the catalog status at a glance. Read all concept files' frontmatter (tier, specialization, id, one_liner) and STATE.md. Render:
```

---

## CHANGE 10 — Rewrite Step 9d verify-shortcut to use Universal Action Menu verbs

**LOCATE** (entire Step 9d section):

```
#### Step 9d — Verify (`arch verify <concept-id>`)

The shortcut for humans who already know a concept deeply and don't want to sit through a full teach session. Prompt:

```
VERIFY SHORTCUT — circuit-breaker (intermediate · distributed-reliability)

  "Stop calling a dead downstream — give it time to recover before the next attempt."

How confident are you?

  [quick-check]  One sanity question to confirm the core idea (recommended)
  [skip-check]   Mark verified without a question (trust-me mode)
  [teach]        Actually teach me — fall through to /gabe-teach arch show <id>
  [cancel]       Back to arch dashboard
```

- **quick-check:** Generate ONE question via the same LLM path as Step 9c but constrained to "quickest sanity check of the core idea." If answered correctly → `verified` with note `verify-quick` in HISTORY.md, score `1/1`. If wrong → `pending` with note `claimed known, failed quick-check`, and suggest running `/gabe-teach arch show <id>`.
- **skip-check:** Mark `verified` immediately with note `verify-skip` in HISTORY.md, score `—/—`. Trust-me mode. Appears in STATE.md as `verified` but with a lower confidence signal (reinforcements=0, score blank). Future reinforcement via topic tagging will upgrade the score naturally.
- **teach:** Redirect to Step 9c.
- **cancel:** Back to Step 9a.

The two paths are intentionally asymmetric: `quick-check` produces a higher-trust verification; `skip-check` exists to let a busy expert move on without friction but leaves a signal in HISTORY.md that this concept was never actually quizzed.
```

**REPLACE WITH:**

```
#### Step 9d — Verify (`arch verify <concept-id>`)

The shortcut for humans who already know a concept deeply. Renders a one-line header followed by the Universal Action Menu — no asymmetric verb set.

```
VERIFY — circuit-breaker (intermediate · distributed-reliability)

  "Stop calling a dead downstream — give it time to recover before the next attempt."

  [explain]  Teach me anyway — full Step 9c lesson
  [next]     Mark verified without a quiz (trust-me mode). Writes `verify-skip`, score —/—.
  [test]     One sanity question. 1/1 → verified (`verify-quick`); 0/1 → pending with suggestion to run `/gabe-teach arch show <id>`.
  [skip]     Do nothing; return to caller.
```

Writes the same STATE.md + HISTORY.md entries as before (see Step 9e) — only the verb labels change. Mapping: `[next]` = legacy `skip-check`; `[test]` = legacy `quick-check`; `[explain]` = legacy `teach`; `[skip]` = legacy `cancel`.

Rationale: a human who wants to verify has already decided they know it. `[next]` means "move on, I've got it." `[test]` means "prove it to yourself first." `skip-check` and `quick-check` were confusing asymmetric labels that required memorization.
```

---

## CHANGE 11 — Rewrite Step 9f pick rendering to skip the prompt

**LOCATE** (inside Step 9f, the "Rendering the pick" section):

```
**Rendering the pick:**

Print one line before Step 9c takes over:

```
ARCH NEXT — picked by [project-driven|adjacency|foundation-gap] rule

  → retry-with-exponential-backoff (intermediate · distributed-reliability)
     Reason: topic T12 "Why we added tenacity" in ai-app tagged this but not yet taught.
     Prerequisites verified: idempotency-keys ✓

  [teach] Start lesson       [skip] Pick a different concept       [cancel] Back to dashboard
```

If the human picks `skip`, re-run Step 9f excluding the just-skipped concept for this session (in-memory; doesn't write to STATE.md). After 3 skips, fall through to the dashboard — something about the progression heuristic isn't matching; the human knows best and should browse manually.
```

**REPLACE WITH:**

```
**Rendering the pick (teach-first — no pick prompt):**

Print ONE header line, then **immediately** render the lesson via Step 9c. No `[teach]/[skip]/[cancel]` prompt — the Universal Action Menu (Step 0.7) at the end of the lesson handles everything.

```
ARCH NEXT — picked by [project-driven|adjacency|foundation-gap] rule
  → retry-with-exponential-backoff (intermediate · distributed-reliability)
     Reason: topic T12 "Why we added tenacity" in ai-app tagged this but not yet taught.
     Prerequisites verified: idempotency-keys ✓
```

Then the Step 9c lesson renders directly underneath. Skip accounting: `[skip]` at the menu counts against a session skip-budget of 3. After 3 skips without a `[next]`, the command exits to `arch dashboard` with the hint: `3 concepts skipped this session — heuristic may be off. Browse the catalog to pick manually: /gabe-teach arch browse [spec].`

**Empty-state collapse:** if STATE.md has zero verified entries AND no ArchConcepts tags in the current project's KNOWLEDGE.md (the degenerate case), Step 9f falls into Tier 2 with alphabetical-by-id-within-foundational ordering. Instead of explaining the degeneracy across multiple paragraphs, render ONE line and proceed:

```
ARCH NEXT — picked by adjacency (seed pick — STATE empty)
  → async-background-processing (foundational · agent)
     Reason: first foundational candidate with no prereqs. Verify a few concepts to unlock ranked picks.
```

Then the Step 9c lesson renders. No alternative-listing, no tier-rule explanation. The point is to start teaching; ranking quality improves naturally once STATE has a few rows.
```

---

## CHANGE 12 — Insert new Step 10 (retro) and Step 11 (tour) before Staleness handling

**LOCATE** (end of Step 9, right before the `---` that precedes `## Staleness handling (unchanged)`):

```
Computed live on every dashboard render — no persisted tier field, no drift risk.

---

## Staleness handling (unchanged)
```

**REPLACE WITH:** (this block is long — the entire new Steps 10 and 11)

```
Computed live on every dashboard render — no persisted tier field, no drift risk.

---

### Step 10: Retro mode (`retro`) — what went wrong, what was reversed

**Teach mode.** Surfaces the retrospective lessons that are otherwise buried: skipped topics with their reason, decisions that were reversed (DECISIONS.md rows with `superseded` status), and "we built it, then removed it" moments (topics marked skipped with code-removal commits in their lineage).

**Why this matters.** Users said they wanted to learn "what went well, what went wrong, the reasons why we took some architectural decisions." Verified topics cover what went well. Retro mode covers everything else: the false starts, the over-engineering that got walked back, the speculative code that proved unnecessary. These are the highest-signal lessons in any codebase — the team paid for them in commits-and-reverts — but today they're scattered across the KNOWLEDGE.md Sessions log, DECISIONS.md Status column, and commit history.

**Step 10a — Gather retro candidates (deterministic):**

1. **Skipped topics** from `.kdbp/KNOWLEDGE.md` Topics table: rows where `Status` = `skipped`. Pull the Source column (which often contains the reason — e.g., T4's "Lesson was speculative for current single-caller codebase. Decision recorded as D1; trigger logged in PENDING.md. Pipeline-side check removed.").
2. **Superseded decisions** from `.kdbp/DECISIONS.md`: rows where `Status` = `superseded`. Include the supersede reason (typically a new decision ID that replaced it).
3. **Reversal commits** (optional, heuristic): run `git log --all --oneline --grep='revert\|rollback\|remove\|simpler' --since="90 days ago"` and cross-reference against topic commits. Surface commits that removed code introduced by a verified topic. Cap at 5 to avoid noise.

**Step 10b — Pick + render (same shape as Step 9f):**

Sort candidates by recency (most recent first). Pick the top one. Render ONE header line then the lesson via a 6-part template variant tuned for retrospectives:

```
RETRO — picked by [skipped-topic|superseded-decision|reversal-commit] rule
  → T4: Why guardrails also run inside the pipeline (skipped 2026-04-18)
     Origin: Plan "Phase 1 Level 2a", Phase 2 · Decision D1 · Files removed: app/agent/pipeline.py

What we built:
  Before: guardrails ran at both the API boundary AND inside run_triage_pipeline.
  After:  guardrails run only at the API boundary; pipeline trusts its caller.

Analogy: Like having a bouncer at the door and another at every table —
worth it only if multiple hallways feed the room. One hallway = one bouncer.

Scenario (the moment we noticed):
  Before: review question surfaced — "why is this check here twice?"
  After:  roadmap audit showed no upcoming phase adds a second caller of
          run_triage_pipeline. Deleted the duplicate. Coverage stayed green;
          latency dropped by the cost of one compiled regex pass.

Primary force: Defense-in-depth is load-bearing across *trust domains*
(firewall + OS + app auth), not within one Python process. Duplicating the
check in the same trust domain creates drift risk — two return shapes to
keep in sync, dead-code rot in the unreachable branch, cognitive load on
every future reader ("which check is authoritative?").

Also:
- Speculative defense-in-depth imports future requirements that may never ship.
- "Remove unless" beats "keep just in case" when the caller graph is auditable.

Revisit trigger: When a second caller of run_triage_pipeline is added
(retry worker, admin replay, cron reprocess, queue consumer), MOVE the
check into the pipeline — don't duplicate again. See PENDING D1-trigger.

Further reading:
  → .kdbp/DECISIONS.md#D1  (the decision record — rationale + alternatives)
  → .kdbp/PENDING.md       (the D1-trigger entry that'll fire re-surface)

Q1: If we'd kept both checks, what specific review question becomes
    uncomfortable to answer every time a new engineer joins?
Q2: The pipeline's internal boundary isn't a trust boundary. What would
    have to change in the architecture for the duplicate check to start
    earning its keep?
```

Then the Universal Action Menu (Step 0.7). `[next]` auto-advances to the next retro candidate. When retro candidates are exhausted: `Retrospective clear. /gabe-teach to continue with project topics.`

**Step 10c — Write-back.** Retro doesn't change topic status (skipped stays skipped); it just teaches the lesson and appends a note to the `Sessions` log:

```
### YYYY-MM-DD — /gabe-teach retro
- Retrospective: T4 (skipped, verified-as-retro 2/2)
- Decisions taught: D1 (superseded)
```

No STATE.md arch write (retro lessons are project-specific, not catalog concepts).

**Step 10d — Empty state:** if no skipped topics, no superseded decisions, no reversal commits → `Nothing to retro yet. When you skip a topic or supersede a decision, it'll surface here.`

---

### Step 11: Tour mode (`tour`) — how this app works

**Teach mode.** Walks the project well-by-well, explaining file paths + what each file contains + key decisions per well. Answers the newcomer question "how does this app work?" in one continuous flow — the piece that was scattered across wells, `STRUCTURE.md`, `DOCS.md`, and well docs.

**Why this matters.** Users said: "if someone else asks how this application works, we should know how it works, like why we do what we do, the paths for the files, what the files contain, and so on." The existing `brief` mode summarizes; the existing `topics` mode teaches individual changes. Neither walks the tree top-to-bottom. Tour does.

**Step 11a — Scan inputs (deterministic):**

1. `.kdbp/KNOWLEDGE.md` Gravity Wells table — iterate in ID order (G1, G2, … G_N).
2. For each well: read Name, Description, Analogy, Paths, Docs.
3. For each Paths glob: run `git ls-files -- "<glob>"` and collect the file list. Dedupe across globs. Sort by depth then alphabetical.
4. For each file, extract a one-sentence "what it contains" signal (deterministic, no LLM, first match wins):
   - Python: first docstring (`"""…"""` at module top).
   - TypeScript/JavaScript: first `/** … */` jsdoc comment at module top, else first single-line `//` comment.
   - Markdown: first heading line (`# …`).
   - Otherwise: first non-blank non-shebang line (truncate to 80 chars).
   - If nothing extractable: `(no header comment)`.
5. For each well, read the well's Docs file (if present) and pull up to 3 entries from `## Key Decisions` section — just the `### <date> — <title>` lines, not full rationale.

**Step 11b — Render one well per "stop":**

```
TOUR — stop 3 of 6: G3 API Layer

Analogy: Reception desk: takes the package, hands a receipt, processes behind the counter.

Purpose: HTTP surface, multipart handling, background tasks.

Path: app/api/**

Files ([N] under this path):
  app/api/__init__.py           (no header comment)
  app/api/main.py               FastAPI app — multipart incident endpoint + background triage dispatch.
  app/api/dependencies.py       Dependency-injection wiring for DB session + settings.
  ... and 2 more files (use /gabe-teach wells → [opendoc 3] for the full list)

Key decisions for this well (from docs/wells/3-api-layer.md):
  2026-04-18 — Guardrails enforced at the API boundary only, not inside pipeline.
  2026-04-17 — 202 Accepted + BackgroundTask for async triage (avoid 30s HTTP hold).

Why it's here (from the well's Purpose section): [first paragraph of `## Purpose` from the Docs file, or if empty: "(Purpose not yet authored — run /gabe-teach to populate)"]
```

Then the Universal Action Menu:
- `[explain]` → re-render this stop with a different angle (different one-liner extraction).
- `[next]` → advance to the next well.
- `[test]` → ask two Socratic questions synthesized from this well's Key Decisions + file list. Example: "Which file in G3 owns the policy decision about when to return 400 vs 202?"
- `[skip]` → skip this well, advance to the next.

**Step 11c — Tour bounds:**

- File list capped at 5 rows per well. `… and N more` if more. User runs `wells → [opendoc N]` for the complete list.
- Wells with empty Paths are skipped silently (no anchor).
- Wells with empty Docs render the decision section as `(no well doc — run /gabe-teach wells → [docs N] to assign one)`.
- On reaching the last well: `Tour complete — walked [K] wells. You now have the map. /gabe-teach for the next lesson.`

**Step 11d — Persistence:**

Tour is read-only. Appends one line to the Sessions log on completion:

```
### YYYY-MM-DD — /gabe-teach tour
- Walked: G1, G2, G3, G4, G5, G6 (6/6)
- Quizzes taken: 2 (G1 pass, G3 pass)
```

**Step 11e — No active plan needed.** Tour runs on the project's static structure (wells + paths + decisions). A newcomer to the repo runs `/gabe-teach tour` as their first command and gets oriented.

---

## Staleness handling (unchanged)
```

---

## Verification plan (after applying the patch)

Run these commands in the ai-app project to dogfood the v2 changes:

1. `/gabe-teach` (bare) → should auto-pick a lesson, not show a dashboard.
2. `/gabe-teach arch` → should teach `async-background-processing` immediately (empty STATE.md seed pick), not render a dashboard.
3. `/gabe-teach arch dashboard` → should render the legacy tier × spec map.
4. `/gabe-teach retro` → should pick up T4 (skipped topic) and D1 (record an explicit retro lesson).
5. `/gabe-teach tour` → should walk G1 → G6, rendering file trees + key decisions per well.
6. Any project topic lesson header → should show `← Plan: "<goal>" · Phase N/M · Commit <sha>` line.
7. Any project topic `Further reading:` → should always render, even when well doc is missing (annotates `⚠`).
8. Any end-of-lesson prompt → should show only `[explain] [next] [test] [skip]`, not mode-specific verbs.

---

## Rollback

If v2 behavior turns out wrong, reverse each CHANGE block (swap LOCATE ↔ REPLACE WITH). The original file is deterministic — no derived state that would need migration.

## Notes for the implementer

- The Edit tool in the environment where this patch was originally drafted (2026-04-18) had a silent size threshold that rejected edits larger than ~200 bytes without error. Apply this patch in an environment without that constraint (direct editor, or fresh Claude Code session).
- LOCATE strings are chosen to be unique in the current file. If a LOCATE match fails, check for whitespace-only diffs or previously-applied partial patches.
- Each CHANGE is independent — apply in any order if preferred. Only CHANGE 2 and CHANGE 4 reference each other (the design-principle paragraph mentions "Universal Action Menu" which Step 0.7 defines); if applying one without the other, the reference is still coherent prose.
