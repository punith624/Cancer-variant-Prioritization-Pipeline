# 🧬 Cancer Variant Prioritization & Clinical Interpretation Pipeline

## 📌 Overview

This project implements an oncology-focused variant prioritization workflow for VEP-annotated VCF files derived from clinical Next-Generation Sequencing (NGS) data.

The pipeline parses CSQ annotations, applies cancer-specific filtering logic, prioritizes pathogenic variants, and generates structured clinical-style JSON case reports.

---

## 🚀 Key Highlights

- Built an end-to-end oncology variant prioritization workflow  
- Implemented CSQ annotation parsing directly from VCF files  
- Designed cancer gene panel filtering logic  
- Applied impact, pathogenicity, and population frequency thresholds  
- Developed custom prioritization framework for clinically relevant variants  
- Generated structured JSON-based clinical case reports  
- Modular pipeline architecture (parser → prioritizer → interpreter)

---

## 🔬 Workflow
VCF (VEP Annotated)
↓
CSQ Annotation Parsing
↓
Cancer Gene Filtering
↓
Impact & Pathogenicity Filtering
↓
Variant Prioritization
↓
Structured JSON Case Report

---

## ⚙️ Features

- VEP CSQ annotation parsing
- Cancer gene panel prioritization
- HIGH / MODERATE impact filtering
- Pathogenicity-based variant selection
- Population frequency (gnomAD-style) thresholding
- Structured JSON case report generation
- Modular and extensible pipeline design

---

## 📂 Project Structure
data/ → Sample VCF file
genollm/ → Core pipeline modules
output/ → Generated case reports


---

## ▶️ How to Run

```bash
cd genollm
bash run_pipeline.sh


```

## 📄 Output

The pipeline generates a structured clinical-style report:

output/case_report.json

The report includes:

- Case summary
- Number of variants parsed
- Number of prioritized variants
- Gene-level findings
- Interpretation summaries


## 🧠 Technologies Used

- Python
- Bash
- VCF (Variant Call Format)
- VEP CSQ annotation format
- Clinical genomics filtering logic


## 🎓 Learning Outcomes

This project demonstrates:

- Understanding of VCF file structure
- Interpretation of VEP CSQ annotations
- Clinical genomics variant prioritization logic
- Oncology-focused filtering strategies
- Modular bioinformatics pipeline design


## 📌 Future Improvements

- ACMG classification simulation
- Integration with ClinVar annotations
- Streamlit-based web dashboard
- PDF clinical report generation
- Docker containerization


## 👨‍💻 Author

Punith Kumar  
Bioinformatics & Clinical Genomics Enthusiast
