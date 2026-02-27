def interpret_variant(variant):

    gene = variant["gene"]
    consequence = variant["consequence"]
    impact = variant["impact"]

    interpretation = f"""
Variant Interpretation
---------------------
Gene: {gene}
Consequence: {consequence}
Impact: {impact}

Clinical Assessment:
This variant is prioritized based on cancer relevance and pathogenicity.
Further clinical correlation is recommended.
"""

    return interpretation




