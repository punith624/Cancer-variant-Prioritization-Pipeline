import pandas as pd 
import json
import streamlit as st
import tempfile
from genollm.pipeline import run_pipeline
from genollm.pdf_report import generate_pdf

st.set_page_config(
    page_title="Cancer Variant Interpretation Platform",
    layout="wide"
)

st.title("🧬 Cancer Variant Interpretation Platform")
st.markdown("**Oncology-focused ACMG classification system**")

st.sidebar.header("About")
st.sidebar.info("""
This platform performs:
- VEP parsing
- Cancer gene prioritization
- ACMG rule-based classification
- Structured interpretation output
""")

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

        with st.spinner("Running variant prioritization and ACMG classification..."):
            report = run_pipeline(temp_path)

        st.divider()

        col1, col2 = st.columns(2)

        col1.metric("Total Variants", report["total_variants"])
        col2.metric("Prioritized Variants", report["prioritized_variants"])

        # ---- Classification Summary ----
        classifications = [v["acmg_classification"] for v in report["findings"]]
        summary_df = pd.Series(classifications).value_counts().reset_index()
        summary_df.columns = ["Classification", "Count"]

        st.subheader("📊 Classification Summary")
        st.bar_chart(summary_df.set_index("Classification"))

        # ---- Variant Findings ----
        st.subheader("🔬 Variant Findings")

        for variant in report["findings"]:

            classification = variant["acmg_classification"]

            with st.expander(f"{variant['gene']} — {classification}"):

                if classification == "Pathogenic":
                    st.error("Pathogenic")
                elif classification == "Likely Pathogenic":
                    st.warning("Likely Pathogenic")
                elif classification == "Benign":
                    st.success("Benign")
                else:
                    st.info("Variant of Uncertain Significance")

                st.json(variant)

        # ---- Download Section ----
        st.subheader("⬇️ Download Report")

        st.download_button(
            label="Download JSON Report",
            data=json.dumps(report, indent=4),
            file_name="case_report.json",
            mime="application/json"
        )

pdf_path = generate_pdf(report)

with open(pdf_path, "rb") as f:
    st.download_button(
        label="Download PDF Clinical Report",
        data=f,
        file_name="clinical_report.pdf",
        mime="application/pdf"
    )
