#!/bin/bash
set -e

INPUT_FASTA="GCF_020520425.1_BTI_SOV_V1_genomic.fna"
CHROM_DIR="chromosomes"
UNIQ_DIR="unique_regions"

mkdir -p "$CHROM_DIR" "$UNIQ_DIR"

# Step 1: Split genome into chromosome files
python split_fasta_by_chromosome.py "$INPUT_FASTA" "$CHROM_DIR"

# Step 2: For each chromosome, align to the rest and extract unique regions
for chrom_fasta in "$CHROM_DIR"/*.fasta; do
    chrom_name=$(basename "$chrom_fasta" .fasta)
    # Create reference genome excluding this chromosome
    ref_fasta="${chrom_name}_ref_temp.fasta"
    grep -v -A 1 ">${chrom_name}" "$INPUT_FASTA" | grep -v "--" > "$ref_fasta"
    # Align with minimap2
    paf_file="${chrom_name}_vs_rest.paf"
    minimap2 -x asm5 "$ref_fasta" "$chrom_fasta" > "$paf_file"
    # Extract unique regions
    python extract_unique_regions_from_paf.py "$chrom_fasta" "$paf_file" "$UNIQ_DIR/${chrom_name}_unique.bed"
    # Clean up
    rm "$ref_fasta" "$paf_file"
done 