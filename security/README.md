# Security Artifacts

This directory stores security deliverables produced for the infrastructure and DevOps project.

## VEX

The file `trivy.openvex.json` is a local OpenVEX document intended to complement the Trivy scan.

It currently documents vulnerabilities that were assessed as not affecting the production deployment because they belong to frontend development or build tooling that is not shipped in the runtime images.

It does not suppress backend runtime vulnerabilities such as Django-related findings. Those should be fixed through dependency upgrades rather than waived.

Example usage with Trivy:

```bash
trivy fs . --vex security/trivy.openvex.json --show-suppressed
```
