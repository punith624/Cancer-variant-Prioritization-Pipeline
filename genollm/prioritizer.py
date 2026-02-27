CANCER_GENES = [
    "TP53","BRCA1","BRCA2","MSH6","MLH1",
    "APC","KRAS","PIK3CA","PTEN","BRAF"
]

def prioritize_variants(variants):

    prioritized = []

    for v in variants:

        if v["gene"] not in CANCER_GENES:
            continue

        if v["impact"] not in ["HIGH","MODERATE"]:
            continue

        if "pathogenic" not in v["clinical_significance"].lower():
            continue

        if v["gnomad_af"] > 0.01:
            continue

        prioritized.append(v)

    return prioritized
