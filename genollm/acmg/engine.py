from .rules import rule_pvs1, rule_pm2, rule_ba1
from .weights import EVIDENCE_STRENGTH


def assign_evidence(variant):
    rules = [rule_pvs1, rule_pm2, rule_ba1]
    evidence = []

    for rule in rules:
        result = rule(variant)
        if result:
            evidence.append(result)

    return evidence


def classify_variant(variant):
    evidence = assign_evidence(variant)

    if "BA1" in evidence:
        return "Benign", evidence

    if "PVS1" in evidence and "PM2" in evidence:
        return "Likely Pathogenic", evidence

    if "PVS1" in evidence:
        return "Likely Pathogenic", evidence

    return "VUS", evidence
