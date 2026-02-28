def parse_vcf(vcf_path):

    variants = []

    with open(vcf_file) as f:
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

                try:
                    gnomad_af = float(parts[-5])
                except:
                    gnomad_af = 0.0

                variants.append({
                    "chrom": chrom,
                    "position": pos,
                    "gene": gene,
                    "consequence": consequence,
                    "impact": impact,
                    "clinical_significance": clin_sig,
                    "gnomad_af": gnomad_af
                })

    return variants
