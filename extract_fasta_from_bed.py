import sys
from Bio import SeqIO

if len(sys.argv) != 4:
    print(f"Usage: python {sys.argv[0]} <input_bed> <chrom_fasta> <output_fasta>")
    sys.exit(1)

input_bed = sys.argv[1]
chrom_fasta = sys.argv[2]
output_fasta = sys.argv[3]

# Load chromosome sequence
record = next(SeqIO.parse(chrom_fasta, "fasta"))
chrom = record.id
seq = str(record.seq)

with open(input_bed) as bed, open(output_fasta, "w") as out:
    for line in bed:
        fields = line.strip().split('\t')
        if len(fields) < 3:
            continue
        start, end = int(fields[1]), int(fields[2])
        subseq = seq[start:end]
        header = f">{chrom}:{start+1}-{end}"
        out.write(f"{header}\n{subseq}\n") 