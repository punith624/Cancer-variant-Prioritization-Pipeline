import json
from parser import parse_variants
from prioritizer import prioritize_variants
from llm_engine import interpret_variant


VCF_FILE = "../cancer_related.vcf"

print("Parsing variants...")
variants = parse_variants(VCF_FILE)

print("Applying prioritization filters...")
filtered = prioritize_variants(variants)

report = {"case_summary": {}, "variants": []}

report["case_summary"]["total_variants"] = len(variants)
report["case_summary"]["prioritized_variants"] = len(filtered)

print("Generating interpretations...")

for v in filtered:
    interpretation = interpret_variant(v)
    v["interpretation"] = interpretation
    report["variants"].append(v)

with open("case_report.json", "w") as f:
    json.dump(report, f, indent=4)

print("Final report generated → case_report.json")

