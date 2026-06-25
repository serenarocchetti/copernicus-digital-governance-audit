# Digital Governance and Audit of Spatial Information Systems  
### A Python Framework for Copernicus Program Performance Monitoring via OData APIs

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Library-Pandas-orange.svg)](https://pandas.pydata.org/)
[![API](https://img.shields.io/badge/Protocol-OData%20%2F%20REST-green.svg)](https://www.odata.org/)

## 📌 Project Overview

This repository contains the technical framework developed for the Master's Thesis in *Digital Governance e Audit dei Sistemi Informativi Spaziali* at UnitelmaSapienza University (Rome).

The project addresses a key challenge in European digital governance:  
the continuous auditing and validation of Earth Observation data flows.

A Python-based automated framework was developed to monitor Copernicus data services (CREODIAS infrastructure), with a focus on Sentinel-2 satellite products.
The framework transforms raw satellite metadata into structured governance metrics for operational monitoring and audit purposes.

## 🧠 Core Objectives

- Automate data extraction from OData APIs
- Monitor performance of Copernicus data services
- Define measurable KPIs for data governance
- Ensure transparency and reliability of Earth Observation data pipelines


## 🛠️ Technical Skills Applied

### 📊 Data Extraction & API Engineering
- REST API querying using OData protocol
- Advanced filtering with `$filter`, `$select`, `$expand`

### 🧹 Data Processing
- JSON/XML parsing and transformation
- Data cleaning and structuring with Pandas
- Time-series handling of satellite metadata

### 📈 KPI & Performance Monitoring
- **Ingestion Latency (Data Freshness)**  
  Time difference between acquisition and publication
- **Data Integrity Checks**  
  Validation using checksum and metadata consistency
- **Spatial Validation**  
  Geolocation footprint analysis
- **Data Lifecycle Monitoring**  
  Tracking of online vs archived datasets based on lifecycle and eviction policies


## 🏗️ Framework Architecture
The system is structured around three analytical dimensions:

- **Availability & Persistence** → system reliability and data access
- **Metadata Integrity** → completeness and correctness of distributed datasets
- **Temporal Performance** → latency analysis for operational efficiency


## 📁 Repository Structure

- `audit_creodias_master.py` → main automation pipeline (API + KPIs)
- `README.md` → project documentation


## 📊 Key Impact

- Improved transparency in Earth Observation data flows
- Enabled automated KPI tracking for Copernicus services
- Supported monitoring of SLA compliance in EU space infrastructure


## 🚀 Author

Master’s Degree in Data Analysis and Modeling  
Focus: Data Governance, API Analytics, and Space Data Systems


## ▶️ How to run

```bash
pip install -r requirements.txt
python audit_creodias_master.py
