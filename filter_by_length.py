import sys
from Bio import SeqIO

if len(sys.argv) != 6:
    print(f"Usage: python {sys.argv[0]} <input_bed> <chrom_fasta> <min_len> <max_len> <output_bed>")
    sys.exit(1)

input_bed = sys.argv[1]
chrom_fasta = sys.argv[2]
min_len = int(sys.argv[3])
max_len = int(sys.argv[4])
output_bed = sys.argv[5]

# Get chromosome name
record = next(SeqIO.parse(chrom_fasta, "fasta"))
chrom = record.id

with open(input_bed) as in_bed, open(output_bed, "w") as out_bed:
    for line in in_bed:
        fields = line.strip().split('\t')
        if len(fields) < 3: continue
        start, end = int(fields[1]), int(fields[2])
        length = end - start
        if min_len <= length <= max_len:
            out_bed.write(f"{chrom}\t{start}\t{end}\n") 