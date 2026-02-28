import streamlit as st
import tempfile
from genollm.pipeline import run_pipeline

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
