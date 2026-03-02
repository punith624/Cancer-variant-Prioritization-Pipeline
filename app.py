import os
import pandas as pd
import json
import streamlit as st
import tempfile
import time
from genollm.pipeline import run_pipeline
from genollm.pdf_report import generate_pdf

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Cancer Variant Interpretation Platform",
    layout="wide"
)

# ---------------------------
# Oncogene List
# ---------------------------
ONCOGENES = [
    "TP53", "BRCA1", "BRCA2", "EGFR",
    "KRAS", "NRAS", "PIK3CA", "ALK", "BRAF"
]

# ---------------------------
# Title + Landing
# ---------------------------
st.title("🧬 Cancer Variant Interpretation Platform")

st.markdown("""
This platform enables oncology-focused interpretation of **VEP-annotated VCF files**
using a modular **ACMG-based classification engine**.

Generate:
- Structured JSON reports
- Clinical-grade PDF reports
- Exportable CSV tables
""")

st.divider()

# ---------------------------
# Case Information
# ---------------------------
st.subheader("🧾 Case Information")

case_id = st.text_input("Case ID", placeholder="e.g., CLN-2026-001")

with st.expander("Patient Metadata (Optional)"):
    col1, col2 = st.columns(2)

    patient_age = col1.number_input("Age", min_value=0, max_value=120, step=1)
    patient_gender = col2.selectbox("Gender", ["Male", "Female", "Other"])
    tumor_type = st.text_input("Tumor Type", placeholder="e.g., Lung Adenocarcinoma")

st.divider()

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.title("Navigation")

mode = st.sidebar.radio(
    "Select Mode",
    ["🚀 Demo Mode", "📂 Upload Clinical VCF"]
)

st.sidebar.divider()
st.sidebar.markdown("**Engine Workflow:**")
st.sidebar.markdown("""
1. VEP CSQ Parsing  
2. Cancer Gene Prioritization  
3. ACMG Rule Classification  
4. Structured Report Generation  
""")

# ---------------------------
# Function: Display Report
# ---------------------------
def display_report(report):

    # Attach Case Metadata
    report["case_id"] = case_id
    report["metadata"] = {
        "age": patient_age,
        "gender": patient_gender,
        "tumor_type": tumor_type
    }

    st.divider()

    # ---------------------------
    # Case Summary
    # ---------------------------
    st.subheader("📋 Case Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Variants", report["total_variants"])
    col2.metric("Prioritized Variants", report["prioritized_variants"])
    col3.metric("Reportable Findings", len(report["findings"]))

    st.divider()

    # ---------------------------
    # Classification Summary Chart
    # ---------------------------
    classifications = [
        v["acmg_classification"]
        for v in report["findings"]
    ]

    summary_df = (
        pd.Series(classifications)
        .value_counts()
        .reset_index()
    )

    summary_df.columns = ["Classification", "Count"]

    st.subheader("📊 Classification Summary")
    st.bar_chart(summary_df.set_index("Classification"))

    # ---------------------------
    # Variant Findings
    # ---------------------------
    st.subheader("🔬 Variant Findings")

    for variant in report["findings"]:

        classification = variant["acmg_classification"]
        gene_name = variant["gene"]

        # Oncogene Highlight
        if gene_name in ONCOGENES:
            gene_display = f"🔥 {gene_name}"
        else:
            gene_display = gene_name

        # Color Badge
        if classification == "Pathogenic":
            badge = "🔴 Pathogenic"
        elif classification == "Likely Pathogenic":
            badge = "🟠 Likely Pathogenic"
        elif classification == "Benign":
            badge = "🟢 Benign"
        else:
            badge = "🔵 VUS"

        with st.expander(f"{gene_display} — {badge}"):
            st.json(variant)

    # ---------------------------
    # Downloads
    # ---------------------------
    st.subheader("⬇️ Download Reports")

    # JSON
    st.download_button(
        label="Download JSON Report",
        data=json.dumps(report, indent=4),
        file_name=f"{case_id or 'case'}_report.json",
        mime="application/json"
    )

    # CSV
    if report["findings"]:
        findings_df = pd.DataFrame(report["findings"])
        csv = findings_df.to_csv(index=False)

        st.download_button(
            label="Download CSV Table",
            data=csv,
            file_name=f"{case_id or 'case'}_variants.csv",
            mime="text/csv"
        )

    # PDF
    pdf_path = generate_pdf(report)

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="Download PDF Clinical Report",
            data=f,
            file_name=f"{case_id or 'case'}_clinical_report.pdf",
            mime="application/pdf"
        )


# ---------------------------
# Function: Run Engine with Progress
# ---------------------------
def run_with_progress(path):

    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.text("Step 1/3: Parsing VEP annotations...")
    progress_bar.progress(30)
    time.sleep(0.5)

    status_text.text("Step 2/3: Cancer gene prioritization...")
    progress_bar.progress(60)
    time.sleep(0.5)

    status_text.text("Step 3/3: Applying ACMG classification...")
    progress_bar.progress(90)
    time.sleep(0.5)

    report = run_pipeline(path)

    progress_bar.progress(100)
    status_text.text("Analysis complete ✅")

    return report


# ---------------------------
# DEMO MODE
# ---------------------------
if mode == "🚀 Demo Mode":

    st.subheader("Run Demo Using Sample Cancer Dataset")

    if st.button("Run Demo Analysis"):

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        demo_path = os.path.join(BASE_DIR, "data", "cancer_related.vcf")

        with st.spinner("Executing clinical interpretation engine..."):
            report = run_with_progress(demo_path)

        display_report(report)


# ---------------------------
# UPLOAD MODE
# ---------------------------
elif mode == "📂 Upload Clinical VCF":

    uploaded_file = st.file_uploader(
        "Upload VEP-annotated VCF file",
        type=["vcf"]
    )

    if uploaded_file:

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.getvalue())
            temp_path = tmp.name

        st.success("File uploaded successfully")

        if st.button("Run Analysis"):

            with st.spinner("Executing clinical interpretation engine..."):
                report = run_with_progress(temp_path)

            display_report(report)


# ---------------------------
# Footer Branding
# ---------------------------
st.divider()
st.caption("Developed by Punith Kumar | Clinical Genomics & Bioinformatics")
