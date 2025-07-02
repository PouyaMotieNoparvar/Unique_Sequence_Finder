# Chromosome/species-Specific Unique Sequence Extraction Pipeline

This pipeline extracts unique, chromosome or species-specific DNA segments of 200–500 bp from a FASTA file containing the sequences for chromosomes or various genomic sequences of different species. These segments are ideal for designing PCR markers that are specific to individual chromosomes or species.

## Overview

The pipeline:
1. Splits the genome into separate chromosome files (if your goal is to design species specific primers you can skip this step but the fasta file for species should be a single chromosom file then put the species genomic sequence fasta files in a folder, name the folder "chromosomes". 
2. For each chromosome/organism, aligns it against the rest of the genome to find unique (non-aligned) regions using minimap2.
3. Extracts these unique regions.
4. Filters the unique regions to keep only those between 200–500 bp.

All steps are automated and memory-efficient, making it suitable for large genomes.

---

## Requirements

- **Python 3.7+**
- **[Biopython](https://biopython.org/)**
- **[minimap2](https://github.com/lh3/minimap2)** (must be installed and in your PATH)
- Bash shell (for running the main script)

### Install Python dependencies
```bash
pip install -r requirements.txt
```

### Install minimap2
- Download from [minimap2 releases](https://github.com/lh3/minimap2/releases)
- Unpack and add the binary to your PATH
- Test with: `minimap2 --version`
- OR
---- `conda install bioconda::minimap2` (recomended)
---

## File Descriptions

- **split_fasta_by_chromosome.py**: Splits the genome FASTA into one file per chromosome OR put the species single chromosom genome sequences in the "chromosomes" folder.
- **align_and_extract_unique.sh**: Main pipeline script. For each chromosome, aligns it to the rest of the genome, extracts unique regions, and saves them as BED files.
- **extract_unique_regions_from_paf.py**: Parses minimap2 output to find unique (non-aligned) regions.
- **filter_by_length.py**: Filters BED regions to keep only those between 200–500 bp.
- **requirements.txt**: Python dependencies.

---

## Step-by-Step Usage

### 1. Prepare your genome FASTA
Place your genome file (e.g., `GCF_020520425.1_BTI_SOV_V1_genomic.fna`) in the project directory.

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
Make sure `minimap2` is installed and available in your PATH.

### 3. Run the main pipeline
```bash
bash align_and_extract_unique.sh
```
This will:
- Create a `chromosomes/` directory with one FASTA per chromosome.
- For each chromosome, align it to the rest of the genome and extract unique regions as BED files in `unique_regions/`.

### 4. Filter unique regions by length (200–500 bp)
For each chromosome, run:
```bash
python filter_by_length.py unique_regions/<chromosome>_unique.bed chromosomes/<chromosome>.fasta 200 500 filtered_unique_regions/<chromosome>_unique_200_500.bed
```
You can automate this with a simple loop in bash:
```bash
mkdir -p filtered_unique_regions
for chrom_fasta in chromosomes/*.fasta; do
    chrom=$(basename "$chrom_fasta" .fasta)
    python filter_by_length.py unique_regions/${chrom}_unique.bed $chrom_fasta 200 500 filtered_unique_regions/${chrom}_unique_200_500.bed
done
```

### 5. (Optional) Extract FASTA sequences for filtered regions
To get the actual DNA sequences for your filtered unique regions, use the provided script:
```bash
python extract_fasta_from_bed.py filtered_unique_regions/<chromosome>_unique_200_500.bed chromosomes/<chromosome>.fasta fasta_sequences/<chromosome>_unique_200_500.fasta
```
You can automate this for all chromosomes:
```bash
mkdir -p fasta_sequences
for chrom_fasta in chromosomes/*.fasta; do
    chrom=$(basename "$chrom_fasta" .fasta)
    python extract_fasta_from_bed.py filtered_unique_regions/${chrom}_unique_200_500.bed $chrom_fasta fasta_sequences/${chrom}_unique_200_500.fasta
done
```
This will create FASTA files with the actual sequences for each filtered region, ready for primer design or further analysis.

---

## Output
- `chromosomes/`: Per-chromosome FASTA files
- `unique_regions/`: BED files of unique regions per chromosome
- `filtered_unique_regions/`: BED files of unique regions 200–500 bp per chromosome

---

## Troubleshooting

- **minimap2 not found**: Make sure minimap2 is installed and in your PATH.
- **Python import errors**: Run `pip install -r requirements.txt`.
- **Permission denied**: Make sure scripts are executable (`chmod +x align_and_extract_unique.sh`).
- **Large genome/slow performance**: The pipeline is designed to be memory-efficient, but runtime depends on genome size and your computer's speed.

---

## FAQ

**Q: Can I use this for other species?**  
A: Yes! Just replace the input FASTA with your genome file.

**Q: How do I design primers for these regions?**  
A: Use the filtered BED files to extract sequences, then use a tool like Primer3 or NCBI Primer-BLAST.

**Q: What if I want a different length range?**  
A: Change the `200 500` arguments in the filtering step to your desired range.

---

## Citation
If you use this pipeline, please cite the minimap2 and Biopython papers, and this repository.

---

## License
MIT License (or specify your own) 
