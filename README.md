# Digital Governance and Audit of Spatial Information Systems
## A Python Framework for Copernicus Program Performance Monitoring via OData APIs


### 📌 Project Overview
This repository contains the technical architecture and source code developed for the Master's Thesis project titled **"Digital Governance e Audit dei Sistemi Informativi Spaziali"** at UnitelmaSapienza University (Rome). 

The project addresses a core challenge of European **Digital Governance** in the Big Data era: the validation and continuous auditing of Earth Observation data flows. A **fully automated audit framework** was designed and implemented in Python to monitor the **CREODIAS** cloud infrastructure in real-time, focusing the computational analysis on the data products of the **Sentinel-2** satellite mission.

### 🛠️ Technical Competencies & Data Skills
As a **Data Analyst / Information Systems Auditor**, developing this framework involved the practical application of the following core data skills:
* **Advanced Data Extraction (Metadata Engineering):** Programmatic and systematic interrogation of the `EODATA` catalog by constructing REST queries filtered using the international **OData** protocol (utilizing `$filter`, `$expand`, and `$select` operators).
* **Data Processing & Manipulation:** Cleaning, parsing temporal dimensions, and structuring complex JSON/XML metadata responses into tabular DataFrames using **Pandas**.
* **Defining and Monitoring Performance KPIs:**
  * **Ingestion Latency (Data Freshness):** Statistical modeling and calculation of the temporal gap (in hours) between satellite image acquisition (`ContentDate`) and actual cloud catalog publication (`PublicationDate`).
  * **Data Integrity:** Verification of algorithmic consistency checks via **Checksum** validation.
  * **Spatial Consistency:** Parsing geometric geolocation metadata (`GeoFootprint` / `Footprint`).
  * **Data Persistence Audit:** Monitoring online vs. archived data states based on scheduled lifecycle deletion policies (`EvictionDate`).

### 📐 Audit Framework Architecture
The conceptual framework is built around three fundamental analytical dimensions:
1. **Availability & Persistence:** Infrastructure health checks and catalog availability metrics.
2. **Metadata Integrity:** Information completeness validation across distributed data packets (Level-1C and Level-2A).
3. **Temporal Performance:** Empirical latency analysis to guarantee operational resilience for environmental monitoring and emergency response systems.

### 💻 Repository Structure
* `audit_creodias_master.py` - The core Python script containing the automated pipeline for OData API querying, data manipulation with Pandas, and KPI/latency calculations.
* `README.md` - Documentation and project overview.

### 📈 Key Takeaways
This framework transforms complex infrastructure logs into transparent business and governance metrics. It enables a continuous auditing model that minimizes technological silos and verifies Service Level Agreements (SLAs) compliance according to European spatial directives (INSPIRE).
