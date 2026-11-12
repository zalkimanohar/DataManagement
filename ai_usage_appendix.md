# Appendix: Declaration of Artificial Intelligence (AI) Tool Usage

**Project Title:** Curated, Quality-Assessed, and FAIR-Documented Formula 1 World Championship Race Results (1950–2025)  
**Compliance Statement:** In strict adherence to course guidelines, AI-assisted coding and writing tools were utilized exclusively for **syntax assistance, debugging boilerplate code, and structural formatting**. All architectural design, data profiling logic, FAIR metadata assessments, graph modeling, individual component reports, and reflection logs represent the original, independent work of the respective team members.

---

## 1. Summary of AI Tools Utilized

| Tool Name | Model / Version | Primary Purpose | Scope of Assistance |
| :--- | :--- | :--- | :--- |
| **Google Gemini** | Gemini 3 Flash | Syntax verification & documentation structuring | Assisted with Parquet schema inspection queries, Markdown table formatting, and slide presentation narrative structuring. |
| **GitHub Copilot / ChatGPT** | GPT-4o / Codex | Python & PySpark syntax help | Provided boilerplate syntax for `pandas` data profiling functions, `NetworkX` graph traversal methods, and regex validation patterns. |

---

## 2. Granular Usage Log by Project Component

### Component A: FAIR Assessment & Metadata Enrichment
* **Team Member:** Chirag Adhikari (`src/fair_assessment.py`, `src/metadata.py`, `src/pid_enrichment.py`)
* **AI Tool Used:** Google Gemini / ChatGPT
* **Nature of Assistance:** 
  * Checked XML/XSD validation syntax for DataCite 4.5 schema compliance.
  * Generated standard JSON-LD boilerplate templates for dataset metadata records.
* **Human Verification:** All FAIR indicator scores (F-UJI / RDA metrics), Wikidata entity linking logic, and license reconciliation decisions (`CC BY-NC-SA 4.0` vs. `MIT`) were manually researched, executed, and verified against source documentation.

### Component B: Data Quality & Profiling
* **Team Member:** Manohar Zalki (`src/profiling.py`, `src/quality_charts.py`)
* **AI Tool Used:** Google Gemini
* **Nature of Assistance:** 
  * Verified syntax for extracting column/row dimensions and metadata headers from Apache Spark Parquet files.
  * Assisted with formatting the summary Data Quality & Profiling Markdown table.
* **Human Verification:** All anomaly detection thresholds (e.g., identifying sentinel value `grid = 0` in issue `B04` and Indianapolis 500 IQR outlier fences in `C08`), statistical distributions, and quality charts were independently designed and validated.

### Component C: Data Cleaning & Pipeline
* **Team Member:** Nicolas Bonilla (`src/cleaning.py`, `src/vocabularies.py`, `src/schema.py`)
* **AI Tool Used:** GitHub Copilot
* **Nature of Assistance:** 
  * Autocompleted standard `pandas` string normalization and regex syntax for harmonizing driver and constructor identifiers.
  * Assisted with syntax for handling mixed JSON / JSON Lines file encodings (`B28`).
* **Human Verification:** All cleaning rules (`C01`–`C08`), referential integrity constraints across the gold dataset tables, and SHA-256 checksum verification pipelines were authored and tested independently.

### Group Sections & Graph Modeling / Interactive Dashboard
* **Team Members:** All Members (`dashboard/app.py`, `dashboard/app_classic.py`, Graph Model, Report Intro/Conclusion)
* **AI Tool Used:** Google Gemini
* **Nature of Assistance:** 
  * Provided syntax examples for `Streamlit` layout containers and `NetworkX` shortest-path query formatting.
  * Helped structure speaker transition notes to clarify baseline vs. post-enrichment pipeline metrics during presentation rehearsal.
* **Human Verification:** The underlying graph topology (teammate chains and constructor networks), hybrid RAG retrieval architecture, and all written analytical conclusions in the group report were collaboratively written and verified by the team without AI text generation.

---

## 3. Academic Integrity Attestation

We hereby confirm that:
1. No AI tool was used to generate entire code modules, analytical essays, or individual reflection logs.
2. Every snippet of syntax suggested by an AI assistant was reviewed, understood, adapted, and tested by the responsible team member.
3. All external data sources (Jolpica-F1, Ergast, Wikidata) and software libraries are properly cited in the main bibliography and `README.md`.