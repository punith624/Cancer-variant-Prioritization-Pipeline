from .parser import parse_vcf
from .prioritizer import filter_variants
from .acmg.engine import classify_variant


def run_pipeline(vcf_path):

    variants = parse_vcf(vcf_path)
    prioritized = filter_variants(variants)

    results = []

    for v in prioritized:
        classification, evidence = classify_variant(v)

        v["acmg_classification"] = classification
        v["acmg_evidence"] = evidence

        results.append(v)

    return {
        "total_variants": len(variants),
        "prioritized_variants": len(results),
        "findings": results
    }
