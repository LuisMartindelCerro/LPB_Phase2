# Import Libraries

import re
import difflib
import sys

def calculate_gc_content(sequence):
    # Calculate GC content as percentage
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    total_bases = len(sequence)
    return (g_count + c_count) / total_bases * 100

def longest_common_substring(seq1, seq2):
    # Find the longest common substring using difflib
    sequence_matcher = difflib.SequenceMatcher(None, seq1, seq2)
    match = sequence_matcher.find_longest_match(0, len(seq1), 0, len(seq2))
    
    # The match will return a tuple (i, j, size) representing the start and end of the substring
    # Extract the longest common substring using the match
    longest_substr = seq1[match.a: match.a + match.size]
    return longest_substr

def analyze_aptamers(file_path):
    
    if len(sys.argv) != 2:
        print("Error: Exactly one argument expected ('input_file'). Provided arguments: {}".format(len(sys.argv) - 1))
        print("Usage: python3 script_v.py <Input_file>")
        sys.exit(1)

    # Get the organism name and output file path from the command line arguments
    file = sys.argv[1]

    # Read input file
    with open(file, 'r') as file:
        data = file.read()

    # Use regular expressions to find sequences and IDs
    matches = re.findall(r'([A-Za-z0-9_]+)\s([ACGT]+)', data)

    num_sequences = len(matches)

    if num_sequences == 1:
        print("Warning: your file only has 1 sequence. Only Length Analysis and GC Content analysis will be computed.")
    elif num_sequences > 2:
        print("Warning: your file has", num_sequences, "sequences.  Only Length Analysis and GC Content analysis will be computed.")
    
    # Initialize output
    output = ""

    # Process sequences
    for i in range(num_sequences):
        seq_id, seq = matches[i]
        seq_length = len(seq)
        output += f"{seq_id} length: {seq_length}\n"

    for i in range(num_sequences):
        seq_id, seq = matches[i]
        seq_gc_content = calculate_gc_content(seq)
        output += f"{seq_id} GC content: {seq_gc_content:.1f}%\n"

    # If there are exactly 2 sequences, compute the longest common substring
    if num_sequences == 2:
        seq1_id, seq1 = matches[0]
        seq2_id, seq2 = matches[1]
        common_substring = longest_common_substring(seq1, seq2)
        output += f"Longest common substring: {common_substring}\n"
    
    # Write output to a file
    with open('output.txt', 'w') as output_file:
        output_file.write(output)
    
    print("Analysis completed!")

    print(output)  # Print to the console as well for immediate feedback

# Example usage:
analyze_aptamers("input.txt")
