# Honeypot Evaluation Framework for SMEs

A weighted multi-criteria framework for evaluating open-source honeypot solutions in Small and Medium Enterprises.

> **Associated paper:** *A Weighted Multi-Criteria Evaluation Framework for Open-Source Honeypot Solutions in Small and Medium Enterprises* — submitted to the [Journal of Cybersecurity and Privacy (JCP)](https://www.mdpi.com/journal/jcp).

---

## The Framework

The framework evaluates honeypot solutions across **20 criteria** in **4 categories**, producing an **SME Suitability Grade** (A+ through C) as its output.

### Base Category Weights

| Category | Weight | What it measures |
|----------|--------|-----------------|
| **Cost & Resources** | 25% | Licensing, hardware, cloud hosting costs |
| **Deployment Complexity** | 30% | Installation, configuration, documentation, usability, scalability |
| **Detection Effectiveness** | 25% | Protocol coverage, interaction depth, logging, fingerprinting resistance, malware capture, threat intel |
| **Operational Manageability** | 20% | Monitoring, alerting, stability, community support |

These base weights were derived from a structured synthesis of SME cybersecurity literature (ENISA, BSI, Awan et al., Sachidananda et al.). Full justification is provided in the paper.

### Criteria per Category

<details>
<summary><strong>C1 — Cost & Resources (3 criteria, equally weighted)</strong></summary>

| ID | Criterion |
|----|-----------|
| C1.1 | Software Licensing Cost |
| C1.2 | Hardware Requirements |
| C1.3 | Cloud/Hosting Cost |

</details>

<details>
<summary><strong>C2 — Deployment Complexity (6 criteria, equally weighted)</strong></summary>

| ID | Criterion |
|----|-----------|
| C2.1 | Installation Process |
| C2.2 | Configuration Complexity |
| C2.3 | Documentation Quality |
| C2.4 | Update/Maintenance Process |
| C2.5 | Non-Specialist Usability |
| C2.6 | Scalability |

</details>

<details>
<summary><strong>C3 — Detection Effectiveness (6 criteria, non-equal sub-weights)</strong></summary>

| ID | Criterion | Sub-Weight |
|----|-----------|-----------|
| C3.1 | Protocol Coverage | 20% |
| C3.2 | Interaction Level | 18% |
| C3.3 | Logging Quality | 18% |
| C3.4 | Fingerprinting Resistance | 20% |
| C3.5 | Malware/Payload Capture | 12% |
| C3.6 | Threat Intelligence Output | 12% |

</details>

<details>
<summary><strong>C4 — Operational Manageability (5 criteria, equally weighted)</strong></summary>

| ID | Criterion |
|----|-----------|
| C4.1 | Monitoring Interface |
| C4.2 | Alert Integration |
| C4.3 | Runtime Resource Consumption |
| C4.4 | Stability/Reliability |
| C4.5 | Community Support |

</details>

### SME Suitability Grading Scale

| Grade | Score | Interpretation |
|-------|-------|----------------|
| A+ | 4.50–5.00 | Highly suitable for SME deployment |
| A | 4.00–4.49 | Suitable with minor limitations |
| B+ | 3.50–3.99 | Conditionally suitable |
| B | 3.00–3.49 | Suitable only with significant caveats |
| C | < 3.00 | Not recommended for SMEs |

---

## Share Your Expert Opinion

We are collecting professional perspectives on how these categories should be weighted. **Your input helps validate and refine the framework.**

### How to contribute (2–5 minutes)

1. Click **[Issues → New Issue](../../issues/new/choose)**
2. Select **"Framework Weight Response"**
3. Fill in your proposed category weights (must sum to 100%)
4. Optionally redistribute sub-weights within any category
5. Submit

You can also explain your rationale — especially valuable if you have hands-on honeypot deployment experience or work with SMEs.

### What we do with responses

All responses are public and will be aggregated to compare **community-derived weights** against the **literature-derived base weights**. Results will be published as part of follow-up research. No personal data beyond your GitHub username is collected.

---

## Interactive Calculator

An interactive web-based calculator is available that lets you:
- Customise category and sub-category weights
- Score multiple honeypot solutions
- See per-category winners and overall SME Suitability Grades
- Run sensitivity analysis with adjustable weight sliders

<!-- TODO: Add GitHub Pages link once deployed -->
<!-- **[Try the Calculator →](https://username.github.io/honeypot-framework/)** -->

---

## Repository Structure

```
├── framework/
│   └── base_weights.json       # Base framework definition (machine-readable)
├── scripts/
│   └── aggregate.py            # Aggregate responses from GitHub Issues
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── weight-response.yml # Structured form for weight submissions
└── README.md
```

### Aggregating Responses

```bash
# Basic usage (public repo, no auth needed)
python scripts/aggregate.py --repo owner/honeypot-framework

# With auth token (for private repos or higher rate limits)
python scripts/aggregate.py --repo owner/honeypot-framework --token ghp_xxx

# Output raw JSON for further analysis
python scripts/aggregate.py --repo owner/honeypot-framework --json > data.json
```

---

## Citation

If you use this framework in your research, please cite:

```bibtex
@article{kathrotiya2026honeypot,
  title={A Weighted Multi-Criteria Evaluation Framework for Open-Source Honeypot Solutions in Small and Medium Enterprises},
  author={Kathrotiya, Bhargav Dharmik and Mayer, Andreas and Keller, Markus},
  journal={Journal of Cybersecurity and Privacy},
  year={2026},
  publisher={MDPI}
}
```

---

## License

The framework specification and base weights are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The aggregation scripts are released under [MIT](LICENSE).
