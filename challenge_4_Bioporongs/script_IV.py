# Import Libraries

from collections import defaultdict
from Bio import SeqIO
import sys

# Check if there is a valid FASTA file as input

###

pathogenic_seqs = []
non_pathogenic_seqs = []

# Read Fasta file
for record in SeqIO.parse("input.fasta", "fasta"):
    if record.id.startswith("pathogenic"):
        pathogenic_seqs.append(str(record.seq))
    elif record.id.startswith("non_pathogenic"):
        non_pathogenic_seqs.append(str(record.seq))

if not pathogenic_seqs or not non_pathogenic_seqs:
        print("Error: Missing sequences for comparison.")


# Check all sequences have the same length

## Establish a standard length for comparison
standard_length = len(pathogenic_seqs[0])

## Look sequences with a different length
for sequence in pathogenic_seqs:
     if len(sequence) != standard_length:
          print("Warning: not all the sequencen provided have the same length. Check your alignments!")

for sequence in non_pathogenic_seqs:
     if len(sequence) != standard_length:
          print("Warning: not all the sequencen provided have the same length. Check your alignments!")

seq_length = len(pathogenic_seqs[0])
mutation_positions = {}

for i in range(seq_length):
    pathogenic_residues = {seq[i] for seq in pathogenic_seqs}
    non_pathogenic_residues = {seq[i] for seq in non_pathogenic_seqs}
        
    # Find mutations unique to pathogenic strains
    if pathogenic_residues != non_pathogenic_residues:
        mutation_positions[i + 1] = (pathogenic_residues, non_pathogenic_residues)

# Look for valid aminoacids

valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")

for pos, (pathogenic, non_pathogenic) in mutation_positions.items():
     pathogenic.intersection_update(valid_amino_acids)
     non_pathogenic.intersection_update(valid_amino_acids)

# Print results
for pos, (pathogenic, non_pathogenic) in mutation_positions.items():
    if pathogenic != non_pathogenic:
        print(f"Position {pos}: Pathogenic -> {pathogenic}, Non-Pathogenic -> {non_pathogenic}")