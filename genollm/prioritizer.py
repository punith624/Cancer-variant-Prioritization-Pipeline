def filter_variants(variants):
    """
    Apply cancer gene filtering + impact + population frequency filtering
    """

    filtered = []

    for v in variants:

        impact = v.get("impact")
        af = float(v.get("gnomad_af", 0))

        # Keep HIGH or MODERATE impact
        if impact in ["HIGH", "MODERATE"]:

            # Remove common population variants
            if af < 0.01:
                filtered.append(v)

    return filtered
