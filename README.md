# GFF3 Feature Extraction Tool

A comprehensive command-line bioinformatics tool for parsing GFF3 annotation files and extracting specific genomic features with their corresponding DNA sequences.

## 🧬 Overview

This tool processes GFF3 (Generic Feature Format Version 3) files to extract genomic features based on user-specified criteria. It handles both annotation parsing and embedded FASTA sequence extraction, making it valuable for genomic analysis workflows.

## ✨ Features

- **GFF3 File Parsing**: Reads and parses complex genomic annotation files
- **Feature Search**: Finds specific features by type, attribute, and value
- **FASTA Sequence Extraction**: Extracts embedded FASTA sequences from GFF3 files
- **Strand-Aware Processing**: Properly handles forward and reverse complement sequences
- **Sequence Formatting**: Outputs properly formatted FASTA sequences (60 characters per line)
- **Error Handling**: Robust error handling for file operations and data validation

## 🚀 Usage

```bash
python3 export_gff3_feature.py <source_gff> <type> <attribute> <value>
```

### Parameters:
- `source_gff`: Path to the input GFF3 file
- `type`: Feature type to search for (e.g., "CDS", "gene", "exon")
- `attribute`: Attribute name to match (e.g., "gene", "product")
- `value`: Attribute value to search for

### Example:
```bash
python3 export_gff3_feature.py saccharomyces_cerevisiae.gff3 CDS gene YAL001C
```

## 📁 Input/Output

**Input**: GFF3 files with embedded FASTA sequences
- Supports standard GFF3 format
- Tested with Saccharomyces cerevisiae genome data

**Output**: FASTA-formatted sequences
- Descriptive headers with feature information
- Proper line wrapping (60 characters per line)
- Strand-aware sequence orientation

## 🛠️ Technical Details

- **Language**: Python 3
- **Dependencies**: Standard library only
- **File Handling**: Efficient parsing of large genomic files
- **Algorithm**: Implements proper reverse complement calculation for negative strand features

## 🧪 Real-World Application

This tool processes actual yeast genome data from the Saccharomyces Genome Database, demonstrating practical bioinformatics file handling capabilities essential for genomic research workflows.

## 📊 Data Sources

Tested with:
- Saccharomyces cerevisiae genome annotation (230KB+ files)
- Standard SGD (Saccharomyces Genome Database) format

## 🔬 Biological Context

Essential for:
- Gene sequence extraction
- Protein coding sequence analysis
- Genomic feature annotation
- Comparative genomics studies
- Molecular biology research workflows

## 📝 Author

Rohan Ray - Johns Hopkins University MS Bioinformatics Program
