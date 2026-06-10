# AGENTS.md

## Status

**Experiment complete (2026-06-10).** All classifier runs, scoring, and aggregation are done.
Corpus, annotations, and results are frozen. METHODOLOGY.md records the executed procedure.

## Project structure

Research data repository for a classifier benchmark. No compiled code; no CI.

```
corpus/          -- annotated scenarios and sealed annotation files
experiments/     -- per-item classifier outputs and aggregate CSVs
scripts/         -- Python runners (annotate.py, classify.py, score.py, aggregate.py)
params.json      -- single source of truth for model, provider, pricing, temperature
PROTOCOL.md      -- pre-registered experimental protocol; locked pre-annotation
METHODOLOGY.md   -- executed procedure; written after experiment completion
DATA_DICTIONARY.md -- schemas for every file in corpus/ and experiments/
```

## Commands

```bash
uv run python3 scripts/annotate.py --pass a --output corpus/annotations-a.json
uv run python3 scripts/annotate.py --pass b --output corpus/annotations-b.json
uv run python3 scripts/classify.py --classifier A --runs 3
uv run python3 scripts/classify.py --classifier B --runs 3
uv run python3 scripts/classify.py --classifier C --runs 3
uv run python3 scripts/score.py
uv run python3 scripts/aggregate.py
```

All scripts read `params.json` at runtime for model ID, provider, pricing, and timeout.
Always invoke via `uv run python3`, not `python3` directly.

## Protocol lock -- read before touching corpus/ or experiments/

`PROTOCOL.md` is locked from the moment the first scenario is written. The rules that follow
are non-negotiable; they exist to prevent circularity and confirmation bias.

- **Do not write classifier prompts before corpus freeze.** Ground-truth labels must be sealed
  before any classifier sees the scenarios.
- **Do not modify sealed annotation files.** `corpus/annotations-a.json` and
  `corpus/annotations-b.json` are immutable once written. Never edit them.
- **Do not modify `corpus/scenarios.json` after freeze.** Post-freeze label changes require an
  Amendment Log entry in `PROTOCOL.md` with date, commit SHA, change, and rationale.
  Outcome-direction amendments are not permitted.
- **Do not read pass-1 output during pass-2 annotation.** Each annotator pass is a separate
  agent invocation with no shared context.
- **Do not add fields to classifier output that `score.py` does not read**, and do not score
  fields the classifier was not instructed to produce. Run the rubric-runner cross-check
  (documented in PROTOCOL.md) before any classifier run.

## Corpus design

60 one-action-per-scenario items. Each scenario is a single action string plus one sentence of
context. Items are stratified across a 2x2 matrix (risk label x reversibility):

| | Low Risk | High Risk |
|---|---|---|
| **Reversible** | ~20 | ~10 |
| **Irreversible** | ~15 | ~15 |

The "low risk + irreversible" cell is the headline test class for Fisher's exact test.

Ground-truth labels: `reversibility` (`reversible`, `bounded_reversible`, `irreversible`) and
`risk_tier` (`low`, `medium`, `high`). Items with per-item Cohen's kappa below 0.7 are
discarded before any classifier prompt is written.

Annotation kappa (actual): 0.89 (reversibility), 0.92 (risk tier). 0 items discarded.

## Classifiers

- **A** -- multi-factor risk label: scores severity + blast radius + rollback availability;
  halts on severity >= 4 OR blast_radius >= 4
- **B** -- reversibility gate: halts on any match against `mutates_persistent_state`,
  `external_side_effect`, or `no_rollback_procedure`
- **C** -- combined: halts on Classifier A OR Classifier B signal

Classifier B's prompt must name each IRREVERSIBLE_MARKER explicitly by the identifiers above.

## Results (summary)

60 scenarios, 3 classifiers, 3 runs each. 0 invalid runs. All verdicts consistent (std=0).

| Classifier | Halt rate | Miss rate (irreversible) | False-positive rate | Fisher p (low+irrev, n=5) |
|---|---|---|---|---|
| A (multi-factor risk) | 75.0% | 13.8% | 64.5% | 0.0747 |
| B (reversibility gate) | 96.7% | 0.0% | 93.6% | 0.4921 |
| C (combined A OR B) | 85.0% | 0.0% | 71.0% | 0.0020 |

Full results: `experiments/aggregate/summary.csv`. Full methodology: `METHODOLOGY.md`.

## Output schemas

See DATA_DICTIONARY.md for the full schema of every file. Key files:

- `corpus/scenarios.json` -- 60 items with final adjudicated labels
- `experiments/results/{classifier}/{scenario_id}/run-{N}/verdict.json` -- per-run output
- `experiments/aggregate/summary.csv` -- headline metrics per classifier
- `experiments/aggregate/consistency.csv` -- cross-run variance per item
- `experiments/aggregate/failure-classifications.csv` -- miss/false-positive breakdown per item

## Runs and consistency

3 runs per item per classifier at temperature 0.3. Consistency flag if verdict std = 0 across
all 3 runs. Invalid runs (API failure after retry) are excluded from rate calculations and
counted in `summary.csv`.

## Do not

- Commit secrets, credentials, or PII
- Modify sealed annotation files (`corpus/annotations-a.json`, `corpus/annotations-b.json`)
- Change `corpus/scenarios.json` labels without an Amendment Log entry in `PROTOCOL.md`
- Write classifier prompts before corpus freeze
- Score fields not explicitly instructed in the classifier prompt
