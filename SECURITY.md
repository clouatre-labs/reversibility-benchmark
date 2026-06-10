# Security Policy

## Reporting

Please report vulnerabilities or corpus integrity issues privately via
[GitHub's private vulnerability reporting](https://github.com/clouatre-labs/reversibility-benchmark/security/advisories/new).

Do not open public issues for sensitive matters.

## Scope

This is a research data repository. The primary security concern is corpus integrity: ensuring
that scenario descriptions, annotations, and results have not been tampered with after the
annotation freeze documented in [PROTOCOL.md](PROTOCOL.md).

Report privately if you discover:

- Evidence that sealed annotation files (`corpus/annotations-a.json`,
  `corpus/annotations-b.json`) were modified after their sealing commit
- A script that reads or writes data in a way that could introduce label leakage
- Credentials or secrets committed to the repository

## Branch Protection

The `main` branch is protected by a GitHub ruleset with the following rules:

- **Required signatures**: all commits must be GPG-signed
- **No force push**: history cannot be rewritten on main
- **No deletion**: the main branch cannot be deleted
- **Squash-only merges**: all PRs are squashed on merge

These controls ensure the git history is an auditable record of all changes to the corpus
and experimental results.

## Response SLA

| Severity | Acknowledgement | Remediation target |
|---|---|---|
| Critical (corpus tampering, credential leak) | Within 72 hours | Within 14 days |
| Low (script data-handling issue) | Within 72 hours | Next regular commit |

## Reporter Credit

Reporters who disclose issues responsibly will be credited in the relevant commit message or
release notes, unless they request anonymity.
