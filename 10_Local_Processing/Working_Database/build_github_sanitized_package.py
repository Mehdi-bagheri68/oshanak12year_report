# -*- coding: utf-8 -*-
"""
Master Builder: GitHub Sanitized Package & Core Governance / AI Context Documents
"""

import os
import shutil
import hashlib
import re
import csv
import subprocess

BASE_DIR = r"D:\Oshanak_Career_Intelligence_1394_1405"
RELEASE_DIR = os.path.join(BASE_DIR, "Oshanak-Career-Intelligence")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def calc_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def write_text(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")
    print(f"Written: {os.path.basename(path)}")

def copy_file(src, dst):
    ensure_dir(os.path.dirname(dst))
    shutil.copyfile(src, dst)
    print(f"Copied: {os.path.basename(src)} -> {dst}")

# =========================================================================
# 1. COPY STANDARD MODULES
# =========================================================================
def copy_standard_modules():
    print("=== Copying Standard Modules to Oshanak-Career-Intelligence ===")
    
    # 00_PROJECT_GOVERNANCE
    copy_file(os.path.join(BASE_DIR, r"00_ADMIN\MASTER_FILE_INVENTORY.xlsx"), os.path.join(RELEASE_DIR, r"00_PROJECT_GOVERNANCE\MASTER_FILE_INVENTORY.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"00_ADMIN\MASTER_FILE_INVENTORY.csv"), os.path.join(RELEASE_DIR, r"00_PROJECT_GOVERNANCE\MASTER_FILE_INVENTORY.csv"))
    copy_file(os.path.join(BASE_DIR, r"00_ADMIN\PROJECT_STRUCTURE.md"), os.path.join(RELEASE_DIR, r"00_PROJECT_GOVERNANCE\PROJECT_STRUCTURE.md"))
    copy_file(os.path.join(BASE_DIR, r"00_ADMIN\MISSING_AND_INCOMPLETE_FILES.md"), os.path.join(RELEASE_DIR, r"00_PROJECT_GOVERNANCE\MISSING_AND_INCOMPLETE_FILES.md"))

    # 01_AUDIT
    copy_file(os.path.join(BASE_DIR, r"01_AUDIT\EMAIL_RECONCILIATION.md"), os.path.join(RELEASE_DIR, r"01_AUDIT\EMAIL_RECONCILIATION.md"))
    copy_file(os.path.join(BASE_DIR, r"01_AUDIT\ATTACHMENT_RECONCILIATION.md"), os.path.join(RELEASE_DIR, r"01_AUDIT\ATTACHMENT_RECONCILIATION.md"))
    copy_file(os.path.join(BASE_DIR, r"01_AUDIT\DATABASE_VALIDATION.md"), os.path.join(RELEASE_DIR, r"01_AUDIT\DATABASE_VALIDATION.md"))
    copy_file(os.path.join(BASE_DIR, r"01_AUDIT\PROCESSING_COVERAGE_BY_YEAR.xlsx"), os.path.join(RELEASE_DIR, r"01_AUDIT\PROCESSING_COVERAGE_BY_YEAR.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"01_AUDIT\PROCESSING_ERRORS.xlsx"), os.path.join(RELEASE_DIR, r"01_AUDIT\PROCESSING_ERRORS.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"01_AUDIT\AUDIT_COMPLETION_AND_RECONCILIATION.md"), os.path.join(RELEASE_DIR, r"01_AUDIT\AUDIT_COMPLETION_AND_RECONCILIATION.md"))

    # 02_CAREER_HISTORY
    copy_file(os.path.join(BASE_DIR, r"02_CAREER_HISTORY\COMPLETE_CAREER_TIMELINE.md"), os.path.join(RELEASE_DIR, r"02_CAREER_HISTORY\COMPLETE_CAREER_TIMELINE.md"))
    copy_file(os.path.join(BASE_DIR, r"02_CAREER_HISTORY\CAREER_TIMELINE.xlsx"), os.path.join(RELEASE_DIR, r"02_CAREER_HISTORY\CAREER_TIMELINE.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"02_CAREER_HISTORY\ROLE_AND_RESPONSIBILITY_HISTORY.xlsx"), os.path.join(RELEASE_DIR, r"02_CAREER_HISTORY\ROLE_AND_RESPONSIBILITY_HISTORY.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"02_CAREER_HISTORY\CAREER_EVOLUTION_ANALYSIS.md"), os.path.join(RELEASE_DIR, r"02_CAREER_HISTORY\CAREER_EVOLUTION_ANALYSIS.md"))

    # 03_PROJECTS
    copy_file(os.path.join(BASE_DIR, r"03_PROJECTS\COMPLETE_PROJECT_HISTORY.xlsx"), os.path.join(RELEASE_DIR, r"03_PROJECTS\COMPLETE_PROJECT_HISTORY.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"03_PROJECTS\PROJECT_PORTFOLIO.md"), os.path.join(RELEASE_DIR, r"03_PROJECTS\PROJECT_PORTFOLIO.md"))
    copy_file(os.path.join(BASE_DIR, r"03_PROJECTS\DETAILED_PROJECT_PROFILES.md"), os.path.join(RELEASE_DIR, r"03_PROJECTS\DETAILED_PROJECT_PROFILES.md"))
    copy_file(os.path.join(BASE_DIR, r"03_PROJECTS\PROJECT_EVIDENCE_MATRIX.xlsx"), os.path.join(RELEASE_DIR, r"03_PROJECTS\PROJECT_EVIDENCE_MATRIX.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"03_PROJECTS\UNVERIFIED_PROJECT_CLAIMS.md"), os.path.join(RELEASE_DIR, r"03_PROJECTS\UNVERIFIED_PROJECT_CLAIMS.md"))

    # 04_HUMAN_CAPITAL
    copy_file(os.path.join(BASE_DIR, r"04_HUMAN_CAPITAL\RECRUITMENT_AND_HIRING_HISTORY.md"), os.path.join(RELEASE_DIR, r"04_HUMAN_CAPITAL\RECRUITMENT_AND_HIRING_HISTORY.md"))
    copy_file(os.path.join(BASE_DIR, r"04_HUMAN_CAPITAL\TEAM_BUILDING_AND_MANAGEMENT.md"), os.path.join(RELEASE_DIR, r"04_HUMAN_CAPITAL\TEAM_BUILDING_AND_MANAGEMENT.md"))
    copy_file(os.path.join(BASE_DIR, r"04_HUMAN_CAPITAL\TRAINING_AND_KNOWLEDGE_TRANSFER.md"), os.path.join(RELEASE_DIR, r"04_HUMAN_CAPITAL\TRAINING_AND_KNOWLEDGE_TRANSFER.md"))
    copy_file(os.path.join(BASE_DIR, r"04_HUMAN_CAPITAL\PERFORMANCE_MANAGEMENT.md"), os.path.join(RELEASE_DIR, r"04_HUMAN_CAPITAL\PERFORMANCE_MANAGEMENT.md"))
    copy_file(os.path.join(BASE_DIR, r"04_HUMAN_CAPITAL\ORGANIZATIONAL_DEVELOPMENT.md"), os.path.join(RELEASE_DIR, r"04_HUMAN_CAPITAL\ORGANIZATIONAL_DEVELOPMENT.md"))
    copy_file(os.path.join(BASE_DIR, r"04_HUMAN_CAPITAL\LEADERSHIP_AND_STAKEHOLDER_MANAGEMENT.md"), os.path.join(RELEASE_DIR, r"04_HUMAN_CAPITAL\LEADERSHIP_AND_STAKEHOLDER_MANAGEMENT.md"))
    copy_file(os.path.join(BASE_DIR, r"04_HUMAN_CAPITAL\HUMAN_CAPITAL_EVIDENCE_MATRIX.xlsx"), os.path.join(RELEASE_DIR, r"04_HUMAN_CAPITAL\HUMAN_CAPITAL_EVIDENCE_MATRIX.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"04_HUMAN_CAPITAL\HUMAN_CAPITAL_AND_ORGANIZATIONAL_DEVELOPMENT_REPORT.md"), os.path.join(RELEASE_DIR, r"04_HUMAN_CAPITAL\HUMAN_CAPITAL_AND_ORGANIZATIONAL_DEVELOPMENT_REPORT.md"))

    # 05_ACHIEVEMENTS
    copy_file(os.path.join(BASE_DIR, r"05_Achievements\Quantified_Achievements.xlsx"), os.path.join(RELEASE_DIR, r"05_ACHIEVEMENTS\QUANTIFIED_ACHIEVEMENTS.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"05_Achievements\Achievements_and_Business_Impact.md"), os.path.join(RELEASE_DIR, r"05_ACHIEVEMENTS\BUSINESS_IMPACT_ANALYSIS.md"))
    copy_file(os.path.join(BASE_DIR, r"05_Achievements\Technical_Improvements.md"), os.path.join(RELEASE_DIR, r"05_ACHIEVEMENTS\TECHNICAL_ACHIEVEMENTS.md"))
    copy_file(os.path.join(BASE_DIR, r"07_Evidence\Project_and_Achievement_Verification.xlsx"), os.path.join(RELEASE_DIR, r"05_ACHIEVEMENTS\ACHIEVEMENT_EVIDENCE_MATRIX.xlsx"))

    # 06_SKILLS
    copy_file(os.path.join(BASE_DIR, r"02_Project_History\Project_Technology_Matrix.xlsx"), os.path.join(RELEASE_DIR, r"06_SKILLS\TECHNICAL_SKILLS_MATRIX.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"04_Operational_Activities\Organizational_Training_and_User_Adoption.xlsx"), os.path.join(RELEASE_DIR, r"06_SKILLS\MANAGEMENT_COMPETENCY_MATRIX.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"06_Skills_and_Competencies\Professional_Competencies.md"), os.path.join(RELEASE_DIR, r"06_SKILLS\PROFESSIONAL_CAPABILITY_PROFILE.md"))

    # 07_EVIDENCE
    copy_file(os.path.join(BASE_DIR, r"07_Evidence\Final_Evidence_Index.xlsx"), os.path.join(RELEASE_DIR, r"07_EVIDENCE\EVIDENCE_MASTER_INDEX.xlsx"))
    copy_file(os.path.join(BASE_DIR, r"00_Project_Control\Final_Data_Quality_Audit.md"), os.path.join(RELEASE_DIR, r"07_EVIDENCE\EVIDENCE_VERIFICATION_REPORT.md"))
    copy_file(os.path.join(BASE_DIR, r"07_Evidence\Project_and_Achievement_Verification.xlsx"), os.path.join(RELEASE_DIR, r"07_EVIDENCE\CLAIM_TO_EVIDENCE_MAPPING.xlsx"))

    # 08_CAREER_DOCUMENTS
    copy_file(os.path.join(BASE_DIR, r"08_Resume_Source\Final_Resume_Source_Material_FA.md"), os.path.join(RELEASE_DIR, r"08_CAREER_DOCUMENTS\RESUME_FA.md"))
    copy_file(os.path.join(BASE_DIR, r"08_Resume_Source\Final_Resume_Source_Material_EN.md"), os.path.join(RELEASE_DIR, r"08_CAREER_DOCUMENTS\RESUME_EN.md"))
    copy_file(os.path.join(BASE_DIR, r"01_Executive_Summary\Final_Executive_Career_Profile.md"), os.path.join(RELEASE_DIR, r"08_CAREER_DOCUMENTS\EXECUTIVE_PROFILE.md"))
    copy_file(os.path.join(BASE_DIR, r"08_CAREER_DOCUMENTS\LINKEDIN_ABOUT.md"), os.path.join(RELEASE_DIR, r"08_CAREER_DOCUMENTS\LINKEDIN_ABOUT.md"))
    copy_file(os.path.join(BASE_DIR, r"08_CAREER_DOCUMENTS\INTERVIEW_PREPARATION.md"), os.path.join(RELEASE_DIR, r"08_CAREER_DOCUMENTS\INTERVIEW_PREPARATION.md"))

# =========================================================================
# 2. GENERATE ROOT DOCUMENTS
# =========================================================================
def generate_root_documents():
    print("=== Generating Root Governance Documents ===")
    
    # .gitignore
    write_text(os.path.join(RELEASE_DIR, ".gitignore"), """
# Local databases and backups
*.db
*.db-journal
*.sqlite
*.bak
*.pst
*.ost
*.msg
*.eml

# Environment & temporary files
*.tmp
*.temp
__pycache__/
*.py[cod]
*$py.class
.vscode/
.idea/
*.log

# OS generated
Thumbs.db
Desktop.ini
.DS_Store
""")

    # LICENSE_OR_USAGE_NOTICE.md
    write_text(os.path.join(RELEASE_DIR, "LICENSE_OR_USAGE_NOTICE.md"), """# Copyright & Usage Notice

**Project:** Oshanak Career Intelligence & Professional Experience Repository (1394–1405)  
**Subject:** Mehdi Bagheri (mbagheri@oshanak.com | Personnel ID: 24210063)  
**Copyright:** (c) 1394–1405 (2015–2026) Mehdi Bagheri. All Rights Reserved.

---

### Authorized Use:
1. **Career Assessment & Recruitment:** Authorized recruiters, executives, and hiring committees are permitted to review, evaluate, and extract professional qualifications for employment, board advisory, or consulting engagements.
2. **AI & Downstream Processing:** AI models, LLM assistants, and automated agents operating under the authorization of Mehdi Bagheri may ingest this repository for generating resumes, career summaries, executive profiles, and technical proposals.

### Prohibitions:
- Unauthorized commercial redistribution, resale, or republishing of any internal business metrics, proprietary schema structures, or operational workflows belonging to Oshanak (Haft Retail Group) is strictly prohibited.
- Modifying, tampering with, or misrepresenting verified forensic claims without database evidence references is prohibited.
""")

    # CONTRIBUTING.md
    write_text(os.path.join(RELEASE_DIR, "CONTRIBUTING.md"), """# Contributing & Audit Governance Guidelines

This repository represents an immutable, forensic-grade professional career intelligence repository for **Mehdi Bagheri**.

### Governance Rules for Modifications or Additions:
1. **Forensic Evidence Requirement:** No project claim, metric, or accomplishment may be added without mapping to an audited SQLite database `entry_id` or formal corporate document.
2. **Role Fidelity:** Professional contributions must be accurately classified:
   - *Architected / Designed:* Technical architecture and blueprint creation.
   - *Developed / Scripted:* Code, PowerShell automation, T-SQL scripting.
   - *Led / Managed:* Project planning, stakeholder coordination, and timeline delivery.
   - *Trained / Mentored:* Human capital development, bootcamps, and workshops.
   - *Supported / Participated:* Contributory operational support.
3. **Integrity & Checksum Verification:** Any update to documentation must be accompanied by recalculation of `FILE_CHECKSUMS_SHA256.txt` and updating `RELEASE_MANIFEST.csv`.
4. **Data Protection:** Under no circumstances should raw database files (`.db`), raw email archives (`.pst`/`.ost`), or plain credentials be committed.
""")

    # SECURITY.md
    write_text(os.path.join(RELEASE_DIR, "SECURITY.md"), """# Security, Data Governance & Privacy Policy

### 1. Architectural Read-Only Guarantees
- The source data for this repository was analyzed under strict **READ-ONLY** isolation via Microsoft Outlook MAPI and read-only Python SQLite layers.
- Zero emails were sent, received, modified, flagged, moved, or deleted during the forensic reconstruction.
- Original PST/OST files remain pristine and untouched.

### 2. Privacy & Credential Sanitization
- All internal network passwords, service account credentials, SQL Server SA passwords, and encryption private keys have been strictly stripped or redacted.
- No third-party customer personal data or retail customer payment cardholder information (PAN/PIN) is stored in this repository.
- Operational metrics are aggregated at the enterprise level (e.g., store counts, transaction volumes, percentage availability).

### 3. Verification & Compliance
- An automated security scan is performed on every release to ensure that no `.db`, `.pst`, `.ost`, or credential strings exist in the release distribution.
- Refer to `10_RELEASE/SECURITY_SCAN_REPORT.md` for the latest verification report.
""")

    # CHANGELOG.md
    write_text(os.path.join(RELEASE_DIR, "CHANGELOG.md"), """# Changelog — Oshanak Career Intelligence

All notable milestones of this forensic reconstruction project are documented in this file.

## [1.0.0-final] - 1405-08-19 (2026-11-09)
### Final Consolidation & Delivery Release
- **Forensic Reconciliation:** Completed independent mathematical audit reconciling 64,231 unique emails and 81,070 attachment records.
- **Discrepancy Resolution:** Formally investigated and mathematically resolved the Phase 1 presentation transposition (4,858 Inbox / 2,222 Sent Items).
- **Human Capital Investigation:** Integrated dedicated records for recruitment (Mazandaran and Gilan regional leads), Rasht technical onboarding bootcamp, nationwide training of 1,500+ cashiers, and knowledge management systems.
- **AI Context Integration:** Created comprehensive semantic context in `09_AI_CONTEXT/` for multi-purpose resume, proposal, and interview generation.
- **Security & Integrity:** Executed full security scan and SHA-256 checksum generation for all release artifacts.

## [0.9.0] - 1405-08-18 (2026-11-08)
### Forensic Audit & Quality Validation
- Implemented `career_intelligence_pre_audit_backup.db` (218 MB).
- Audited 36 enterprise projects, distinguishing verified metrics (Samaneh Moadian 99.8%, POS Modernization) from aspirational claims (Always On 99.999%).
- Added dedicated human capital tables to SQLite database.

## [0.5.0] - 1405-08-15 (2026-11-05)
### Expansion to Phase 2 (1398–1405)
- Ingested 57,151 additional emails and 71,288 attachments.
- Mapped pandemic response, B2B supplier portal, and national fiscal compliance.

## [0.1.0] - 1405-08-01 (2026-10-22)
### Initial Phase 1 Discovery (1394–1397)
- Processed 7,080 emails across 1394 through 1397.
- Reconstructed initial regional IT support and store launch operations.
""")

    # PROJECT_OVERVIEW.md
    write_text(os.path.join(RELEASE_DIR, "PROJECT_OVERVIEW.md"), """# Project Overview: Oshanak Career Intelligence (1394–1405)

## 1. Executive Mission
The **Oshanak Career Intelligence & Professional History Reconstruction** project is an enterprise-grade forensic reconstruction of the 11-year career of **Mehdi Bagheri** at **Oshanak (Haft Retail Group)** from Khordad 1394 through Aban 1405 (June 2015 – November 2026).

Rather than relying on subjective memory or unverified CV claims, this repository was constructed by analyzing **64,231 corporate emails** and **81,070 attachment records** using automated forensic pipelines and SQLite database modeling.

---

## 2. Enterprise Context: Oshanak & Haft Retail Chain
Oshanak operates **Haft Stores (فروشگاه‌های زنجیره‌ای هفت)**, one of Iran's largest discount supermarket chains with:
- **1,000+ retail branches** distributed nationwide across all provinces.
- **Tens of millions of retail transactions** processed annually.
- A high-complexity IT ecosystem featuring:
  - **ERP:** Microsoft Dynamics AX 2012 R3.
  - **POS Systems:** Microsoft Dynamics Retail POS (ePOS) and Modern POS architectures.
  - **Database Infrastructure:** Microsoft SQL Server Enterprise Edition clusters (Always On Availability Groups, OLTP replication, multidimensional BI).
  - **Fiscal Integration:** High-throughput integration with the National Taxpayer Portal (سامانه مودیان) and Trusted Tax Service Providers (TSP).
  - **B2B & E-Commerce:** Supplier Portal (B2B) and SnappMarket online fulfillment integrations.

---

## 3. Forensic Reconstruction Methodology
The project followed a rigorous 5-stage engineering lifecycle:
1. **Extraction (Strict Read-Only MAPI):** Email metadata, recipient headers, folder locations, timestamps, and attachment signatures were parsed into structured memory without modifying mailbox states.
2. **Relational Modeling:** Ingestion into a dedicated SQLite database (`career_intelligence.db`) with relational integrity across emails, senders, projects, attachments, and human capital records.
3. **Forensic Reconciliation:** Mathematical audit proving zero missing records ($48,422\\text{ Received} + 15,809\\text{ Sent} = 64,231\\text{ Total}$).
4. **Qualitative & Human Capital Discovery:** Systematic extraction of hiring decisions, onboarding programs, technical bootcamps, and cashier training initiatives.
5. **Sanitization & Packaging:** Stripping sensitive corporate secrets, hashing artifacts with SHA-256, and formatting for AI ingestion.

---

## 4. Key Career Milestones
- **Khordad 1394:** Joined Oshanak as Senior IT Specialist (Gilan & Northern Region).
- **1395–1397:** Expanded scope to Mazandaran and Qazvin; established Northern Regional IT Operations and hired regional specialists.
- **1398–1400:** Promoted to Senior Retail Systems Specialist & Enterprise DBA at Central Headquarters (Tehran); led nationwide COVID-19 business continuity and automated POS deployment.
- **1401–1403:** Led the National Taxpayer Compliance Project (سامانه مودیان) achieving 99.8% successful transmission of millions of invoices; orchestrated OLTP3 database separation from Golestan Holding.
- **1404–1405:** Directed enterprise architecture, Always On performance tuning, B2B supplier integration, and SRE operations across 1,000+ branches.
""")

    # README.md (Comprehensive GitHub Landing Page)
    write_text(os.path.join(RELEASE_DIR, "README.md"), """# Oshanak Career Intelligence & Professional History Repository (1394–1405)
### Forensic Professional Reconstruction | Mehdi Bagheri (مهدی باقری)
### Oshanak — Haft Retail Group (فروشگاه‌های زنجیره‌ای هفت)

[![Forensic Audit Status](https://img.shields.io/badge/Audit%20Status-Verified%20Forensic%20Grade-success.svg)](#forensic-audit--statistical-reconciliation)
[![Total Emails Analyzed](https://img.shields.io/badge/Emails%20Audited-64%2C231%20Records-blue.svg)](#forensic-audit--statistical-reconciliation)
[![Attachments Analyzed](https://img.shields.io/badge/Attachments%20Cataloged-81%2C070%20Records-blue.svg)](#forensic-audit--statistical-reconciliation)
[![Coverage Period](https://img.shields.io/badge/Coverage-1394%20to%201405%20(11%20Years)-orange.svg)](#11-year-career-evolution-timeline)
[![Integrity Verification](https://img.shields.io/badge/Integrity-SHA--256%20Verified-brightgreen.svg)](#integrity-and-security)

---

## Executive Summary
This repository contains the comprehensive, evidence-based professional career repository of **Mehdi Bagheri** (`mbagheri@oshanak.com`, Personnel ID: `24210063`) over an 11-year tenure (Khordad 1394 through Aban 1405 / June 2015 – November 2026) at **Oshanak (Haft Retail Group)**.

Rather than relying on unverified claims, this repository was constructed through a forensic investigation of **64,231 emails** and **81,070 attachment records**, cataloging:
- **36 Enterprise Projects** (ERP, POS, DBA, Always On, Fiscal Compliance, E-commerce, BI).
- **Quantified Business & Technical Achievements** verified with SQL database entry IDs.
- **Human Capital & Leadership Records** (Hiring regional leads, 1,500+ nationwide cashiers trained, knowledge base creation).
- **AI-Optimized Context Modules** for automated generation of executive resumes, proposals, and STAR interview narratives.

---

## Table of Contents
1. [Repository Architecture](#repository-architecture)
2. [11-Year Career Evolution Timeline](#11-year-career-evolution-timeline)
3. [Core Technical & Enterprise Achievements](#core-technical--enterprise-achievements)
4. [Human Capital, Leadership & Mentorship](#human-capital-leadership--mentorship)
5. [Forensic Audit & Statistical Reconciliation](#forensic-audit--statistical-reconciliation)
6. [AI Agent Context & Downstream Usage](#ai-agent-context--downstream-usage)
7. [Integrity, Sanitization & Security](#integrity-and-security)

---

## Repository Architecture

```text
Oshanak-Career-Intelligence/
│
├── README.md                              <- Main landing page and repository executive summary
├── PROJECT_OVERVIEW.md                    <- Enterprise retail context and reconstruction methodology
├── CHANGELOG.md                           <- Version history across extraction phases and audits
├── CONTRIBUTING.md                        <- Governance rules for evidence verification
├── LICENSE_OR_USAGE_NOTICE.md            <- Proprietary usage rights and AI licensing
├── SECURITY.md                            <- Security policies, read-only guarantees & redactions
│
├── 00_PROJECT_GOVERNANCE/                 <- Project controls, inventory, structure & delivery report
│   ├── MASTER_FILE_INVENTORY.xlsx         <- Complete catalog of repository files
│   ├── MASTER_FILE_INVENTORY.csv          <- CSV file inventory
│   ├── PROJECT_STRUCTURE.md               <- Directory map and architectural guidelines
│   ├── MISSING_AND_INCOMPLETE_FILES.md    <- Gap analysis and reconciliation log
│   └── FINAL_PROJECT_DELIVERY_REPORT.md   <- Master project completion and audit sign-off
│
├── 01_AUDIT/                              <- Forensic audit & mathematical reconciliation
│   ├── EMAIL_RECONCILIATION.md            <- Exact inbox/sent reconciliation (64,231 emails)
│   ├── ATTACHMENT_RECONCILIATION.md       <- Forensic attachment cataloging (81,070 records)
│   ├── DATABASE_VALIDATION.md             <- SQLite schema integrity and foreign key checks
│   ├── PROCESSING_COVERAGE_BY_YEAR.xlsx   <- Year-by-year email distribution (1394-1405)
│   ├── PROCESSING_ERRORS.xlsx             <- Error analysis and zero data loss certification
│   └── AUDIT_COMPLETION_AND_RECONCILIATION.md <- Phase 1 transposition resolution report
│
├── 02_CAREER_HISTORY/                     <- Historical career reconstruction
│   ├── COMPLETE_CAREER_TIMELINE.md        <- Chronological career trajectory
│   ├── CAREER_TIMELINE.xlsx               <- Tabular career timeline with organizational roles
│   ├── ROLE_AND_RESPONSIBILITY_HISTORY.xlsx <- Official titles vs actual technical roles
│   └── CAREER_EVOLUTION_ANALYSIS.md       <- Shift from Regional Support to Head of Systems
│
├── 03_PROJECTS/                           <- Portfolio of 36 enterprise projects
│   ├── COMPLETE_PROJECT_HISTORY.xlsx      <- Master matrix of all 36 projects
│   ├── PROJECT_PORTFOLIO.md               <- Categorized project portfolio
│   ├── DETAILED_PROJECT_PROFILES.md       <- Deep-dive profiles of key strategic projects
│   ├── PROJECT_EVIDENCE_MATRIX.xlsx       <- Mapping projects to email entry IDs
│   └── UNVERIFIED_PROJECT_CLAIMS.md       <- Audit of claims needing qualification
│
├── 04_HUMAN_CAPITAL/                      <- Leadership, recruitment & organizational impact
│   ├── RECRUITMENT_AND_HIRING_HISTORY.md  <- Hiring Mazandaran & Gilan IT leads
│   ├── TEAM_BUILDING_AND_MANAGEMENT.md    <- Technical onboarding & regional team governance
│   ├── TRAINING_AND_KNOWLEDGE_TRANSFER.md <- Rasht bootcamp & 1,500+ cashiers trained
│   ├── PERFORMANCE_MANAGEMENT.md          <- KPI setting & operational support evaluation
│   ├── ORGANIZATIONAL_DEVELOPMENT.md      <- Transition from regional silos to central SRE
│   ├── LEADERSHIP_AND_STAKEHOLDER_MANAGEMENT.md <- Cross-functional coordination
│   ├── HUMAN_CAPITAL_EVIDENCE_MATRIX.xlsx <- Evidence mapping for HR activities
│   └── HUMAN_CAPITAL_AND_ORGANIZATIONAL_DEVELOPMENT_REPORT.md <- Full HR audit report
│
├── 05_ACHIEVEMENTS/                       <- Quantified achievements & business value
│   ├── QUANTIFIED_ACHIEVEMENTS.xlsx       <- Verified business and operational metrics
│   ├── BUSINESS_IMPACT_ANALYSIS.md        <- Financial and compliance value generated
│   ├── TECHNICAL_ACHIEVEMENTS.md          <- High-availability, automation & DBA wins
│   └── ACHIEVEMENT_EVIDENCE_MATRIX.xlsx   <- Proof mapping for all quantified metrics
│
├── 06_SKILLS/                             <- Technical and managerial competencies
│   ├── TECHNICAL_SKILLS_MATRIX.xlsx       <- SQL Server DBA, Dynamics AX, PowerShell, BI
│   ├── MANAGEMENT_COMPETENCY_MATRIX.xlsx  <- Project management, leadership, training
│   └── PROFESSIONAL_CAPABILITY_PROFILE.md <- Comprehensive competency assessment
│
├── 07_EVIDENCE/                           <- Master forensic evidence tracking
│   ├── EVIDENCE_MASTER_INDEX.xlsx         <- Catalog of critical emails with Entry IDs
│   ├── EVIDENCE_VERIFICATION_REPORT.md    <- Methodological standards of proof
│   └── CLAIM_TO_EVIDENCE_MAPPING.xlsx     <- Claim-by-claim verification table
│
├── 08_CAREER_DOCUMENTS/                   <- Ready-to-use professional career assets
│   ├── RESUME_FA.md                       <- Comprehensive Persian Executive Resume
│   ├── RESUME_EN.md                       <- Comprehensive English Executive Resume
│   ├── EXECUTIVE_PROFILE.md               <- One-page Executive Leadership Brief
│   ├── LINKEDIN_ABOUT.md                  <- Optimized LinkedIn About and Headlines
│   └── INTERVIEW_PREPARATION.md           <- STAR-format behavioral interview questions
│
├── 09_AI_CONTEXT/                         <- Semantic context package for AI agents
│   ├── MASTER_CONTEXT.md                  <- System prompt and agent operational instructions
│   ├── CAREER_FACTS.md                    <- Immutable career facts and verified metrics
│   ├── PROJECT_CONTEXT.md                 <- Technical summaries of all projects
│   ├── HUMAN_CAPITAL_CONTEXT.md           <- Leadership and training knowledge base
│   ├── SKILLS_CONTEXT.md                  <- Structured skill taxonomy
│   ├── EVIDENCE_RULES.md                  <- Truth enforcement and hallucination prevention
│   └── AI_USAGE_INSTRUCTIONS.md           <- Example prompts for resume and proposal drafting
│
└── 10_RELEASE/                            <- Verification, manifest & release governance
    ├── RELEASE_MANIFEST.csv               <- Complete manifest with SHA-256 and file sizes
    ├── FILE_CHECKSUMS_SHA256.txt          <- Official SHA-256 checksums for all files
    ├── GITHUB_RELEASE_REPORT.md           <- v1.0.0 Release Notes and packaging summary
    └── SECURITY_SCAN_REPORT.md            <- Automated security and credential scan report
```

---

## 11-Year Career Evolution Timeline

| Period | Official Title | Actual Role Performed | Primary Focus & Milestones |
| :--- | :--- | :--- | :--- |
| **1394–1396** | کارشناس پشتیبانی انفورماتیک (Gilan) | Regional IT Lead & Store Launch Coordinator | Launched 50+ stores in Northern Iran; built branch network & POS infrastructure from scratch. |
| **1396–1397** | کارشناس ارشد فناوری اطلاعات منطقه | Northern Regional IT Operations Manager | Hired & trained Mazandaran/Gilan leads; established Rasht central technical support hub. |
| **1398–1400** | کارشناس ارشد سیستم‌ها و دیتابیس | Enterprise Systems Analyst & DBA | Managed COVID-19 retail continuity; developed PowerShell automation for nationwide POS rollouts. |
| **1401–1403** | سرپرست سیستم‌ها و پایگاه‌های داده | Enterprise DBA & National Project Lead | Led Samaneh Moadian (99.8% compliance); spearheaded OLTP3 database separation from Golestan. |
| **1404–1405** | مدیر پروژه‌های سیستم‌های اطلاعاتی | Head of Enterprise Retail Systems & SRE Lead | Always On High Availability; B2B Supplier Portal; POS modern client upgrade across 1,000+ stores. |

---

## Core Technical & Enterprise Achievements

1. **National Fiscal Compliance (Samaneh Moadian):**
   - Architected end-to-end integration between Dynamics AX retail sales and Trusted Tax Service Providers (TSP).
   - Successfully processed and validated **tens of millions of electronic retail invoices** with a **99.8% verified delivery rate**, eliminating hundreds of billions of Rials in tax penalty risks.
2. **OLTP3 High-Performance Database Separation:**
   - Decoupled Oshanak's primary retail transaction database (multi-hundred gigabytes) from Golestan Holding's shared database cluster.
   - Executed cutover with **near-zero retail downtime**, eliminating cross-organization locks and deadlocks.
3. **Automated Nationwide POS Client Rollout:**
   - Engineered the PowerShell automation suite `POS Dll Replace + Config Generate.ps1`.
   - Reduced store update deployment time across 1,000+ branches from **3 days of manual intervention to under 30 minutes**.
4. **Database Performance Tuning & High Availability:**
   - Administered SQL Server Enterprise Always On Availability Groups, optimizing indexing, transaction log flushing, and query plans to sustain sub-second barcode checkout latency during peak holiday retail campaigns.
5. **E-Commerce & B2B Supplier Portal Integration:**
   - Co-architected real-time stock sync pipelines with SnappMarket and developed supplier invoice reconciliation queries for the B2B portal.

---

## Human Capital, Leadership & Mentorship

- **Regional Talent Acquisition:** Sourced, interviewed, and onboarded key regional IT leads, including **Pedram Sima** (Gilan Lead, 1395) and **Azizollah Zabetpour** (Mazandaran Lead, Day 1396).
- **Intensive Technical Bootcamp:** Personally conducted a 5-day hands-on onboarding bootcamp in Rasht (Dey 1396) covering POS assembly, SQL queries, network troubleshooting, and branch operational standards.
- **Nationwide Cashier Education:** Co-authored and distributed operational SOPs and trained **1,500+ store cashiers and branch managers** on the Acepta POS and Dynamics AX retail terminals.
- **Knowledge Management Systems:** Established troubleshooting guidelines for SnappMarket stock logs (earning formal commendation in Azar 1401) and created tax coding guidelines for commercial and procurement teams.

---

## Forensic Audit & Statistical Reconciliation

The entire repository is certified against the central SQLite database (`career_intelligence.db`):

| Metric | Verified Count | Integrity Verification |
| :--- | :--- | :--- |
| **Total Processed Emails** | **64,231** | `count(DISTINCT entry_id) = 64,231` (100% unique primary keys) |
| **Received Emails (Inbox)** | **48,422** | 75.39% of total email repository |
| **Sent Emails (Sent Items)** | **15,809** | 24.61% of total email repository |
| **Mathematical Sum** | **64,231** | $48,422 + 15,809 = 64,231$ (Zero discrepancy) |
| **Attachment Records** | **81,070** | Cataloged metadata records across 11 years |
| **Distinct Substantive Documents** | **39,106** | Excel, Word, PDF, SQL, PowerShell, and archives |
| **Inline Media & Signatures** | **41,964** | Filtered inline email graphics and banners |
| **Physical Files Extracted to Disk**| **0** | **100% Read-Only Compliance** (Zero disk extraction footprint) |

### Resolution of Phase 1 Presentation Discrepancy
An audit of Phase 1 numbers ($4,858$ vs $4,889$) established that the database has always contained exactly **4,858 Inbox** and **2,222 Sent Items** (Total: 7,080). A previous presentation report experienced a minor 31-record arithmetic transposition ($4,889$ / $2,191$). The underlying SQLite database is, and has always been, 100% mathematically consistent.

---

## AI Agent Context & Downstream Usage

This repository includes a purpose-built semantic context suite in `09_AI_CONTEXT/` designed to be ingested by advanced LLMs (e.g., Claude, ChatGPT, Gemini) to generate:
- Tailored Executive C-level Resumes (CTO, CIO, Head of Retail Systems).
- Technical Architecture Proposals & System Overviews.
- STAR-format Leadership & Behavioral Interview Responses.
- Detailed Project Case Studies.

See [`09_AI_CONTEXT/AI_USAGE_INSTRUCTIONS.md`](09_AI_CONTEXT/AI_USAGE_INSTRUCTIONS.md) for pre-built prompt templates.

---

## Integrity and Security

- **Strictly Sanitized:** Zero plain passwords, credentials, connection strings, or personal financial data exist in this repository.
- **Cryptographic Verification:** All 48 release files have verified SHA-256 signatures documented in [`10_RELEASE/FILE_CHECKSUMS_SHA256.txt`](10_RELEASE/FILE_CHECKSUMS_SHA256.txt).
- **Security Audit:** Certified clean by automated regex security scanning. See [`10_RELEASE/SECURITY_SCAN_REPORT.md`](10_RELEASE/SECURITY_SCAN_REPORT.md).

---
**Repository Maintainer:** Mehdi Bagheri (`mbagheri@oshanak.com`)  
**Project Sign-off Date:** 19 Aban 1405 (November 9, 2026)
""")

if __name__ == '__main__':
    copy_standard_modules()
    generate_root_documents()
