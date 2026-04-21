# gabe-teach v2 — Dogfood Baseline

**Purpose.** Capture the output of the 8 verification checks from `gabe-teach-v2-patch.md` so we have a regression baseline for future `/gabe-teach` changes. Per D5=B: "eyeball + keep a screenshot."

**How to use this file.**
1. Open a fresh Claude Code session with this project as CWD.
2. Run each `Command` below in order.
3. Paste the rendered output into the `Actual` block.
4. Tick `[x]` if the `Expected behavior` is met; otherwise leave `[ ]` and add a note under `Notes`.
5. Commit this file when all 8 pass.

Source commits:
- Refactor: `ddeb3e7` (gabe_lens), `ff8fe60` (refrepos mirror)
- New surfaces: `381c6df` (gabe_lens), `23e25ae` (refrepos mirror)

---

## Check 1 — Bare invocation auto-picks a lesson

**Command:** `/gabe-teach`

**Expected behavior:** Auto-routes to `topics` if pending candidates exist; else `arch next`; else `retro`; else "you're current." **Never shows a dashboard first.** Ends with the Universal Action Menu (`[explain]/[next]/[test]/[skip]`).

**Actual:**

```
(paste output)
```

**Result:** `[ ]` pass `[ ]` fail

**Notes:**

---

## Check 2 — `arch` (bare) teaches immediately

**Command:** `/gabe-teach arch`

**Expected behavior:** Picks a concept via progressive-pressure rule (Tier 1 → 2 → 3). On an empty STATE.md, uses the seed-pick collapse: one header line (`ARCH NEXT — picked by adjacency (seed pick — STATE empty)`) then the Step 9c lesson renders directly. **No dashboard, no `[teach]/[skip]/[cancel]` pick prompt.** Ends with Universal Action Menu.

**Actual:**

```
(paste output)
```

**Result:** `[ ]` pass `[ ]` fail

**Notes:**

---

## Check 3 — `arch dashboard` renders legacy tier × spec map

**Command:** `/gabe-teach arch dashboard`

**Expected behavior:** Renders the Step 9a dashboard — per-tier progression bars, recent HISTORY.md events, suggested-next block. Admin mode — no teaching, no Universal Action Menu.

**Actual:**

```
(paste output)
```

**Result:** `[ ]` pass `[ ]` fail

**Notes:**

---

## Check 4 — `retro` surfaces skipped topics + superseded decisions

**Command:** `/gabe-teach retro`

**Expected behavior:** Picks a retro candidate (T4 is skipped in this project's KNOWLEDGE.md; D1 was superseded). Renders the retrospective 6-part template with `RETRO — picked by [rule]` header. **Skips any DECISIONS row whose Status contains `operational`** (L6 filter). Ends with Universal Action Menu.

**Actual:**

```
(paste output)
```

**Result:** `[ ]` pass `[ ]` fail

**Notes:**

---

## Check 5 — `tour` walks wells G1 → G_N

**Command:** `/gabe-teach tour`

**Expected behavior:** Renders stop 1 of K. For G1: Analogy + Purpose + Path glob + file list (capped at 5, with `… and N more` if overflowing) + Key decisions (up to 3) from the well's Docs. Ends with Universal Action Menu; `[next]` advances to G2.

**Actual:**

```
(paste output)
```

**Result:** `[ ]` pass `[ ]` fail

**Notes:**

---

## Check 6 — Topic lesson header carries plan lineage

**Command:** `/gabe-teach topics` (or bare `/gabe-teach` if it auto-routes to topics)

**Expected behavior:** Topic header renders two lines:
```
T[N] (G[M] <Well>, <CLASS>) — <title>
     ← Plan: "<goal>" · Phase <N>/<M>: <name> · Commit <sha>
```
If commit isn't mapped to any plan phase by date range: `← Plan: (unmapped) · Commit <sha>`.

**Actual:**

```
(paste output — just the header block is enough)
```

**Result:** `[ ]` pass `[ ]` fail

**Notes:**

---

## Check 7 — Further-reading always renders

**Command:** Same topic lesson as Check 6 (inspect the lesson body).

**Expected behavior:** `Further reading:` section is present. At minimum, one line for the topic's well doc. Annotation varies by state:
- Well Docs path set + file exists: `(well doc — N verified topics, last updated YYYY-MM-DD)`
- Well Docs path set + file missing: `(⚠ not found — run /gabe-teach init-wells to scaffold)`
- Well Docs path empty: `(⚠ G[M] has no Docs path set — run /gabe-teach wells → [docs N] to assign one)`

Up to 2 additional lines from `.kdbp/DOCS.md` mappings.

**Actual (Further reading section only):**

```
(paste the Further reading: block)
```

**Result:** `[ ]` pass `[ ]` fail

**Notes:**

---

## Check 8 — End-of-lesson menu shows only the 4 universal verbs

**Command:** Any teach-mode lesson above (pick one and inspect its tail).

**Expected behavior:** The lesson ends with exactly these four options (in any visual layout): `[explain]`, `[next]`, `[test]`, `[skip]`. **No mode-specific verbs** (no `quick-check`, `skip-check`, `teach`, `cancel`, `verified`, `pending`, `skipped`, `already-known`).

**Actual (menu block only):**

```
(paste the final menu)
```

**Result:** `[ ]` pass `[ ]` fail

**Notes:**

---

## Overall outcome

`[ ]` All 8 pass — v2 is verified on this project.
`[ ]` Some failed — list which and open a follow-up.

**Session date:** (fill in)
**Claude model used:** (fill in)
