# Security Deliverables

This directory groups the security-related deliverables produced for the infrastructure and DevOps project.

## Scope

The security work completed in this repository currently includes:

- a Trivy dependency and vulnerability scan integrated into CI
- an OpenVEX file documenting findings assessed as not affecting the production deployment
- an OpenSSF Scorecard execution performed from the command line against the GitHub repository

## Repository Elements

- CI workflow: [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)
- Trivy VEX document: [`security/trivy.openvex.json`](../../security/trivy.openvex.json)
- VEX notes: [`security/README.md`](../../security/README.md)
- Scorecard output: [`deliverables/security/scorecard-result.txt`](./scorecard-result.txt)

## Trivy And VEX

Trivy is executed in CI and exports a SARIF report.

The VEX document is used to record vulnerabilities that were reviewed and considered not affecting the deployed production runtime, mainly when the affected package is only part of frontend development or build tooling.

This VEX file does not suppress backend runtime issues such as Django-related vulnerabilities. Those remain relevant and should be addressed through dependency updates.

## OpenSSF Scorecard

OpenSSF Scorecard was executed from the command line against:

- `github.com/Kaliwa/14_ValorisationDonneeMeteo`

The raw result is stored in:

- [`scorecard-result.txt`](./scorecard-result.txt)

### Aggregate score

- `3.1 / 10`

### What the score means

This is a low score and it should not be presented as a strong security posture.

However, the result needs interpretation:

- some failed checks are process and governance maturity checks rather than immediate exploitable flaws
- other failed checks do point to concrete security weaknesses that should be improved

### Positive points

The repository scored well on:

- `CI-Tests`: CI is detected and active
- `Dangerous-Workflow`: no dangerous GitHub workflow patterns were detected
- `Binary-Artifacts`: no binaries were committed to the repository
- `License`: a license file is present
- `Packaging`: packaging or release-related workflow patterns were detected

### Weak points with real impact

These findings matter and should be treated seriously:

- `Token-Permissions = 0/10`
  Some GitHub workflow tokens are broader than necessary.
- `Security-Policy = 0/10`
  No `SECURITY.md` policy file was detected.
- `Vulnerabilities = 0/10`
  Scorecard detected 65 known vulnerabilities.
- `Pinned-Dependencies = 0/10`
  Dependencies are not pinned by hash in the way Scorecard expects.

### Weak points that are more about project maturity

These are weaker signals for a student or early-stage repository, but they still lower the score:

- `Branch-Protection = ?`
  The Scorecard CLI could not read classic branch protection rules with the token that was used. This should be interpreted as an authentication or visibility limitation for the check, not automatically as proof that protection is absent.
- `Code-Review = 0/10`
  No approved reviewed changesets were detected in the repository history Scorecard analyzed.
- `Dependency-Update-Tool = 0/10`
  No automated dependency update tool such as Dependabot was detected.
- `Fuzzing = 0/10`
  No fuzzing setup was detected.
- `Maintained = 0/10`
  The repository appears too recent for this check to score well.
- `Contributors = 0/10`
  Scorecard did not detect multiple contributing organizations.
- `CII-Best-Practices = 0/10`
  No Best Practices badge effort was detected.

## Severity Assessment

The current security posture is best described as:

- **not critical in the sense of “the repository is obviously compromised”**
- **but clearly immature from a security governance perspective**
- **and carrying real dependency-risk that should not be ignored**

In practical terms:

- the low aggregate score is not caused by one catastrophic issue alone
- it is mainly the combination of missing security policy, broad workflow permissions, known dependency vulnerabilities, and several governance checks that score poorly

So the result is serious enough to justify follow-up work, but it is not evidence of an active breach or a fundamentally broken codebase.

## Recommended Next Improvements

The most valuable follow-up actions would be:

1. keep branch protection enabled on `main` and, if needed, rerun Scorecard with a token that can read the configured protection model
2. reduce GitHub Actions token permissions to the minimum needed
3. add a `SECURITY.md` file
4. update backend runtime dependencies with known vulnerabilities
5. add an automated dependency update tool such as Dependabot
6. later, improve review practices and repository governance
