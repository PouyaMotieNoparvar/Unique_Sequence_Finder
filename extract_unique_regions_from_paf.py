import sys
from Bio import SeqIO

if len(sys.argv) != 4:
    print(f"Usage: python {sys.argv[0]} <chrom_fasta> <paf_file> <output_bed>")
    sys.exit(1)

chrom_fasta = sys.argv[1]
paf_file = sys.argv[2]
output_bed = sys.argv[3]

# Get chromosome length
record = next(SeqIO.parse(chrom_fasta, "fasta"))
chrom = record.id
chrom_len = len(record.seq)

# Parse PAF to get aligned regions
aligned = []
with open(paf_file) as f:
    for line in f:
        if line.strip() == "": continue
        fields = line.strip().split('\t')
        if len(fields) < 12: continue
        qstart = int(fields[2])
        qend = int(fields[3])
        aligned.append((qstart, qend))

# Merge overlapping/adjacent intervals
aligned.sort()
merged = []
for start, end in aligned:
    if not merged or start > merged[-1][1]:
        merged.append([start, end])
    else:
        merged[-1][1] = max(merged[-1][1], end)

# Find unaligned (unique) regions
unique = []
prev_end = 0
for start, end in merged:
    if start > prev_end:
        unique.append((prev_end, start))
    prev_end = end
if prev_end < chrom_len:
    unique.append((prev_end, chrom_len))

# Write BED file
with open(output_bed, "w") as out:
    for start, end in unique:
        if end > start:
            out.write(f"{chrom}\t{start}\t{end}\n") 