#!/usr/bin/python3

import sys

def find_feature(gff_path, feature_type, attribute, value):
    """
    Find a feature in a GFF3 file based on the feature type, attribute, and value.
    Returns a dictionary with the feature data or None if no match is found.

    Args:
        gff_path (str): The path to the GFF3 file.
        feature_type (str): The type of feature to search for.
        attribute (str): The attribute to search for.
        value (str): The value of the attribute to search for.

    Returns:
        dict or None: A dictionary with the feature data or None if no match is found.
    """
    matches = []

    try:
        with open(gff_path, 'r', encoding='utf-8') as gff_file:
            for line in gff_file:
                line = line.strip()

                if line.startswith("#"):    # skip the header lines
                    continue

                columns = line.split('\t')  # split by columns
                if len(columns) != 9:
                    continue

                seqid, source, f_type, start, end, score, strand, phrase, attributes = columns
                #print(f" attributes: {attributes}")

                if f_type == feature_type:
                    attr_dict = {}
                    for kv in attributes.split(";"):
                        if "=" in kv:
                            key, val = kv.split("=", 1) 
                            key = key.strip()
                            val = val.strip()
                            attr_dict[key] = val       # add the key-value pair to the dictionary

                    # print(f"Line attributes: {attributes}")
                    # print(f"Parsed attr_dict: {attr_dict}")
                    # print(f"Looking for {attribute}={value}")
                    # print(f"Found value: {attr_dict.get(attribute)}")
                    if attr_dict.get(attribute) == value:   # search for attribute with matching value
                        #print(f"Matching attribute found: {attr_dict}")
                        # add the feature data to the matches list
                        matches.append({
                            "seqid": seqid,
                            "start": int(start),
                            "end": int(end),
                            "strand": strand
                        })
                        break
        if len(matches) >1:     # taking the first match if multiple matches are found
            print(f"Warning: Multiple matches found. Using the first one.")
        elif len(matches) == 0:
            return None
        
        return matches[0]

    except FileNotFoundError:
        print(f"Error: The file {gff_path} could not be found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def extract_fasta(gff_path):
    """
    Extract the FASTA sequence from a GFF3 file, and return the FASTA sequence as a string
    or None if no FASTA region is found.

    Args:
        gff_path (str): The path to the GFF3 file.

    Returns:
        str or None: The FASTA sequence or None if no FASTA region is found.
    """
    fasta_sequence = []
    fasta_region = False

    try:
        with open(gff_path, 'r', encoding='utf-8') as gff_file:
            for line in gff_file:
                line = line.strip()

                if line.startswith("##FASTA"):
                    fasta_region = True
                    continue

                if fasta_region and line:
                    if line.startswith(">"):
                        continue
                    else:
                        fasta_sequence.append(line)

        return "".join(fasta_sequence)
    
    except Exception as e:
        print(f"Error extracting FASTA: {e}")    
        return None

def extract_sequence(fasta_data, feature):
    """
    Extract the sequence from a FASTA file based on the feature data.
    Returns the sequence as a string or None if no sequence is found.

    Args:
        fasta_data (str): The FASTA sequence as a string.
        feature (dict): A dictionary with the feature data.

    Returns:
        str or None: The sequence or None if no sequence is found.
    """
    if not fasta_data or not feature:
        return None
    
    start = feature["start"] - 1
    end = feature["end"]
    strand = feature["strand"]

    sequence = fasta_data[start:end]

    if strand == '-':   # if the strand is negative, take the complement of the sequence
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 
                     'a': 't', 't': 'a', 'c': 'g', 'g': 'c',
                     'N': 'N', 'n': 'n'}
        sequence = ''.join(complement.get(base, base) for base in sequence[::-1])
    
    return sequence



def main():
    """
    Take in the input arguments from the command line, and use the above functions to find the feature,
    extract the sequence, and print the FASTA sequence in the 60 character format.
    """
    if len(sys.argv) != 5:
        print("Usage: python3 export_gff3_feature.py <source_gff> <type> <attribute> <value>")
        print("Example: python3 export_gff3_feature.py Saccharomyces_cerevisiae_S288C.annotation.gff gene ID YAR003W")
        sys.exit(1)

    source_gff = sys.argv[1]
    feature_type = sys.argv[2]
    attribute = sys.argv[3]
    value = sys.argv[4]

    feature = find_feature(source_gff, feature_type, attribute, value)

    if not feature:
        print(f"No matching feature found for type={feature_type}, attribute={attribute}, value={value}.")
        return

    fasta_data = extract_fasta(source_gff)
    if not fasta_data:
        print(f"No FASTA data found in the GFF3 file {source_gff}.")
        return

    try:
        sequence = extract_sequence(fasta_data, feature)
        if sequence:
            header = f">{feature_type}:{attribute}:{value}"
            sequence_chunks = []
            for i in range(0, len(sequence), 60):   # split the sequence into 60 character chunks to print out at a time
                chunk = sequence[i:i+60]
                sequence_chunks.append(chunk)

            formatted_sequence = "\n".join(sequence_chunks)
            # print header from the feature and corresponding sequence
            print(header)
            print(formatted_sequence)
        else:
            print(f"No sequence found for feature {feature_type}:{attribute}:{value}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

