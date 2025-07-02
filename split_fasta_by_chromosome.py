import sys
import os
from Bio import SeqIO

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <input_fasta> <output_dir>")
    sys.exit(1)

input_fasta = sys.argv[1]
output_dir = sys.argv[2]

os.makedirs(output_dir, exist_ok=True)

for record in SeqIO.parse(input_fasta, "fasta"):
    chrom_name = record.id.replace("|", "_")
    out_path = os.path.join(output_dir, f"{chrom_name}.fasta")
    with open(out_path, "w") as out_f:
        SeqIO.write(record, out_f, "fasta") 