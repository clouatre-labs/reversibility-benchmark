# Contributing to reversibility-benchmark

This is a research data repository. Contributions are most valuable as corpus corrections,
methodology questions, and reproducibility reports.

## What to Contribute

- **Corpus issues**: factual errors in scenario descriptions, label disagreements with documented
  evidence, missing seed source attribution
- **Data schema issues**: missing fields, type mismatches, undocumented fields in output files
- **Reproducibility reports**: differences between your results and the published aggregate
  CSVs when running `scripts/classify.py` or `scripts/score.py`
- **Documentation clarifications**: ambiguities in PROTOCOL.md, DATA_DICTIONARY.md, or
  METHODOLOGY.md

**Do not open issues requesting new scenarios or label changes after annotation freeze.**
The protocol is locked pre-annotation (see [PROTOCOL.md](PROTOCOL.md) Amendment Log).
Post-freeze amendments that affect outcome direction are not permitted.

## Reporting Issues

Open a GitHub issue with the appropriate label (`corpus`, `data`, `protocol`, `documentation`,
or `bug`). Include:

- The file and field or section in question
- The observed value or text
- What you expected or what the discrepancy is
- Relevant evidence (e.g., citation for a scenario seed, output from a script run)

## Pull Requests

All changes go through a pull request. No direct pushes to `main`.

### Setup

```bash
git clone https://github.com/your-username/reversibility-benchmark.git
cd reversibility-benchmark
```

For script changes, Python 3.14+ is required. No additional dependencies beyond the standard
library and `boto3` (for Bedrock access).

### Before Submitting

- Run the affected script and verify output matches the schema in DATA_DICTIONARY.md
- Confirm no secrets or API keys are present in any file
- Update DATA_DICTIONARY.md if you add or rename fields

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>
```

Types: `fix`, `docs`, `data`, `chore`, `refactor`, `test`

Examples:

```bash
git commit -S --signoff -m "fix(corpus): correct seed source attribution for scenario-012"
git commit -S --signoff -m "docs(dictionary): document leakage_flag field in verdict.json"
git commit -S --signoff -m "data(aggregate): regenerate summary.csv after scoring fix"
```

## Developer Certificate of Origin (DCO)

All commits must be signed off:

```bash
git commit -S --signoff -m "Your commit message"
```

The `-S` flag GPG-signs the commit (required by branch protection). The `--signoff` flag adds
`Signed-off-by: Your Name <email>`, certifying you agree to the
[DCO](https://developercertificate.org/).

## Pull Request Checklist

- [ ] Commits GPG-signed and signed off (`git commit -S --signoff`)
- [ ] No secrets, credentials, or PII in any file
- [ ] DATA_DICTIONARY.md updated if schema changed
- [ ] Clear PR description explaining the correction and evidence

## License

By contributing, you agree your contributions are licensed under [Apache-2.0](LICENSE).
