# Security Policy

As the owner of this project, I retain **100% authority over the repository, its direction, final decisions, and what code is approved or rejected**.

Because I am not a cybersecurity professional, this project relies on **contributors and GitHub’s automated security systems** to maintain a safe, high-quality codebase. All contributors agree to follow the requirements below.

---

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 5.1.x   | Yes       |
| 4.0.x   | Yes       |
| < 4.0   | No        |

Only supported versions may receive security patches.

---

## Reporting a Vulnerability

To report a security issue:

1. **Do not disclose it publicly.**
2. Email: **security@[yourdomain].com**
3. Provide:

   * Description of the vulnerability
   * Steps to reproduce
   * Potential risks

Acknowledgment will be sent within **48 hours** and triage will begin within **5 business days**.

---

## Contributor & Automated Agent Security Responsibilities

All human contributors and GitHub automated tools (Copilot, Dependabot, code scanning, etc.) are **responsible for ensuring the ongoing security of this project**.

The following requirements are mandatory:

### 1. Enforce Secure Code Practices

Contributors and agents must:

* Remove unsafe or insecure code patterns
* Avoid unsafe libraries or deprecated functions
* Ensure input validation, authorization, and correct error handling
* Prevent any logic that can be exploited by attackers
* Follow GitHub code scanning and Dependabot alert recommendations

### 2. Protect Secrets and Sensitive Data

It is strictly prohibited to commit:

* API keys
* Passwords
* Tokens
* Private configuration values
* Any sensitive data

If a secret is committed, contributors must immediately rotate and remove it.

### 3. Mandatory PR Security Checks

Every pull request must:

* Pass all automated test suites
* Pass all GitHub security scans (code scanning, secret scanning, dependency checks)
* Describe any new permissions or sensitive operations introduced
* Receive approval from at least one reviewer
* Resolve all security alerts before merge

No PR is exempt.

### 4. Responsibility for Fixes

Contributors agree to:

* Respond promptly to security issues related to code they authored
* Submit corrective PRs when vulnerabilities are found
* Support maintainers by clarifying risks and recommended fixes

---

## Owner Authority

To avoid confusion:

* I maintain **full ownership, control, and final decision-making authority** over the repository.
* I may accept, reject, or request changes to any contribution at my discretion.
* Security responsibilities do **not** transfer ownership in any way.

Contributors and automated tools support the project; they do not control it.

---

## Maintainer Role (Simplified)

My responsibilities as maintainer include:

* Receiving security reports
* Approving merges once automated security checks pass
* Coordinating disclosure timelines
* Releasing updated versions

I rely on contributors and automated GitHub systems for security enforcement.

---

## Security Contact

Urgent issues: **security@[yourdomain].com**
General security discussions: please use the repository’s “Security” Discussion category.
