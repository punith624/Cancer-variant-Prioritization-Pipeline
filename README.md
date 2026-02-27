Cancer Variant Prioritization & Clinical Interpretation Pipeline
Overview

This project implements an oncology-focused variant prioritization workflow for VEP-annotated VCF files derived from clinical NGS data.

The pipeline parses CSQ annotations, applies cancer gene filtering, prioritizes pathogenic variants, and generates structured clinical-style reports.

Workflow
VCF → CSQ Parsing → Cancer Gene Filtering → 
Impact & Pathogenicity Filtering → 
Variant Scoring → JSON Case Report

Features

VEP CSQ annotation parsing

Cancer gene panel filtering

HIGH/MODERATE impact prioritization

Pathogenicity-based filtering

Population frequency thresholding

Structured JSON case report output


Project Structure
data/      → Sample VCF file
genollm/   → Core pipeline modules
output/    → Generated reports

Run Pipeline
cd genollm
bash run_pipeline.sh

Output:
output/case_report.json

Technologies Used
Python
Bash
VCF (Variant Call Format)
Clinical genomics logic
