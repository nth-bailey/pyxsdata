# Security Policy

## Supported Versions

Security updates are actively applied to the latest major and minor release versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

If you discover a security vulnerability in `pyxsdata`, please do **NOT** open a public
issue.

Instead, please report security vulnerabilities using one of the following methods:

1. **GitHub Private Vulnerability Reporting** (Preferred):
   - Navigate to the
     [Security tab](https://github.com/nth-bailey/pyxsdata/security/advisories) on
     GitHub and click **"Report a vulnerability"**.

2. **Email**:
   - Send an email to [bailey.tan.nguyen@gmail.com](mailto:bailey.tan.nguyen@gmail.com)
     with the subject line `[SECURITY] pyxsdata vulnerability report`.

### What to Include

Please provide as much information as possible to help us reproduce and address the
issue quickly:

- Type of issue (e.g. XXE, XML entity expansion / Billion Laughs, ReDoS, arbitrary code
  execution).
- Steps to reproduce, including minimal sample schemas/XML and Python code.
- Any potential impact or attack vectors.
- Suggested mitigations, if known.

### Response Timeline

- **Initial Acknowledgement**: Within 48 hours of receipt.
- **Assessment & Triage**: Within 5 business days.
- **Fix & Advisory Release**: Coordinated responsibly, with CVE publication and release
  notes once patched.
