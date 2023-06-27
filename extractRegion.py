import sys
import csv


# Extract arguments from command line
if len(sys.argv) != 4:
    print("Usage: python fasta_region_extraction.py <input.fasta> <output.fasta> <res.tsv>")
    sys.exit(1)


in_fasta = sys.argv[1]
out_fasta = sys.argv[2]
in_csv = sys.argv[3]




with open(in_csv, "r") as file:
    reader = csv.reader(file, delimiter="\t")
    header = next(reader)  # Read the header row
    
    # Get the values of the 7th and 8th columns from the header
    start = int(header[6])
    end = int(header[7])




def strip_fasta(input_fasta):
    stripped_sequence = ''
    with open(input_fasta, 'r') as fasta_file:
        for line in fasta_file:
            line = line.strip()
            if line.startswith('>'):
                header = line
                stripped_sequence += header + '\n'
                next_line_is_sequence = True
            elif next_line_is_sequence:
                sequence = line[:len(line)]
                stripped_sequence += sequence
                next_line_is_sequence = True

    with open("stripped.fasta", 'w') as output:
        output.write(stripped_sequence)





def extract_region_from_fasta(output_fasta, start_position, end_position):
    extracted_sequence = ''
    with open('stripped.fasta', 'r') as fasta_file:
        for line in fasta_file:
            line = line.strip()

            if line.startswith('>'):
                header = line
                extracted_sequence += header + '\n'
            else:
                sequence = line[start_position-1:end_position]
                extracted_sequence += sequence + '\n'


    with open(output_fasta, 'w') as output:
        output.write(extracted_sequence)




# Call the function to extract the region
strip_fasta(in_fasta)



extract_region_from_fasta(out_fasta, start, end)
print("Extraction completed. Extracted region saved to", out_fasta)

