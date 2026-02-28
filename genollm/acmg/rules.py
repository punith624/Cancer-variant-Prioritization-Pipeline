def rule_pvs1(variant):
    """
    PVS1: Null variant in tumor suppressor gene
    """
    if variant["impact"] == "HIGH" and variant["gene_role"] == "TSG":
        return "PVS1"
    return None


def rule_pm2(variant):
    """
    PM2: Absent or extremely low in population databases
    """
    af = float(variant.get("gnomad_af", 0))
    if af < 0.0001:
        return "PM2"
    return None


def rule_ba1(variant):
    """
    BA1: High population frequency (Benign)
    """
    af = float(variant.get("gnomad_af", 0))
    if af > 0.05:
        return "BA1"
    return None
