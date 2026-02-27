import json

# Cancer gene panel
CANCER_GENES = [
    "TP53","BRCA1","BRCA2","MSH6","MLH1",
    "APC","KRAS","PIK3CA","PTEN","BRAF"
]

report = {"variants": []}

with open("cancer_related.vcf") as f:
    for line in f:
        if line.startswith("#"):
            continue

        fields = line.strip().split("\t")

        chrom = fields[0]
        pos = fields[1]
        ref = fields[3]
        alt = fields[4]
        info = fields[7]

        if "CSQ=" not in info:
            continue

        csq_data = info.split("CSQ=")[1]
        transcripts = csq_data.split(",")

        for tx in transcripts:
            parts = tx.split("|")

            gene = parts[3]
            consequence = parts[1]
            impact = parts[2]
            clin_sig = parts[-3]

            # ---- Population Frequency Extraction ----
            try:
                gnomad_af = float(parts[-5])  # gnomAD AF position (may vary)
            except:
                gnomad_af = 0.0

            # ---- Filtering Logic ----

            # 1️⃣ Cancer gene filter
            if gene not in CANCER_GENES:
                continue

            # 2️⃣ Impact filter
            if impact not in ["HIGH", "MODERATE"]:
                continue

            # 3️⃣ Clinical significance filter
            if "pathogenic" not in clin_sig.lower():
                continue

            # 4️⃣ Population frequency filter
            if gnomad_af > 0.01:
                continue

            report["variants"].append({
                "chrom": chrom,
                "position": pos,
                "gene": gene,
                "consequence": consequence,
                "impact": impact,
                "clinical_significance": clin_sig,
                "gnomad_af": gnomad_af
            })

with open("clinical_report.json", "w") as out:
    json.dump(report, out, indent=4)

print("Filtered Oncology Report Generated → clinical_report.json")
