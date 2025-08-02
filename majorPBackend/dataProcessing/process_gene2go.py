import csv
import os
import glob
from collections import defaultdict

def process_gene2go(input_file, output_file, tax_id="9606"):
    """
    Process gene2go file to extract functional annotations for human genes.
    
    Args:
        input_file (str): Path to input gene2go file
        output_file (str): Path to output file
        tax_id (str): Tax ID to filter (default: "9606")
    Returns:
        tuple: (total_rows_processed, filtered_rows) for the file
    """
    print(f"Processing file: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist.")
        return 0, 0
    
    # Define required columns and their indices
    required_columns = {
        'tax_id': 0,
        'GeneID': 1,
        'GO_ID': 2,
        'Evidence': 3,
        'Category': 7
    }
    
    # Dictionary to store GO annotations per gene
    gene_annotations = defaultdict(lambda: {
        'tax_id': tax_id,  # Added tax_id
        'Function': set(),
        'Process': set(),
        'Component': set(),
        'evidence_codes': set(),
        'go_terms': set()
    })
    
    row_count = 0
    filtered_count = 0
    
    try:
        with open(input_file, 'r', newline='') as infile:
            reader = csv.reader(infile, delimiter='\t')
            
            for row in reader:
                row_count += 1
                
                # Check if row has enough columns
                if len(row) < max(required_columns.values()) + 1:
                    continue
                
                # Filter for human genes
                if row[required_columns['tax_id']] == tax_id:
                    gene_id = row[required_columns['GeneID']]
                    go_id = row[required_columns['GO_ID']]
                    evidence = row[required_columns['Evidence']]
                    category = row[required_columns['Category']]
                    
                    # Store annotations
                    gene_annotations[gene_id]['go_terms'].add(go_id)
                    gene_annotations[gene_id]['evidence_codes'].add(evidence)
                    gene_annotations[gene_id][category].add(go_id)
                    
                    filtered_count += 1
                
                if row_count % 10000 == 0:
                    print(f"Processed {row_count} rows in {os.path.basename(input_file)}...")
        
        # Write processed data to output file
        with open(output_file, 'a', newline='') as outfile:
            writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
            
            # Write header if file is empty
            if os.path.getsize(output_file) == 0:
                writer.writerow([
                    'tax_id',           # Added tax_id
                    'GeneID',
                    'total_go_terms',
                    'Function_terms',
                    'Process_terms',
                    'Component_terms',
                    'unique_evidence_codes',
                    'go_terms_list'
                ])
            
            # Write gene annotations
            for gene_id, annotations in gene_annotations.items():
                writer.writerow([
                    annotations['tax_id'],  # Added tax_id
                    gene_id,
                    len(annotations['go_terms']),
                    len(annotations['Function']),
                    len(annotations['Process']),
                    len(annotations['Component']),
                    len(annotations['evidence_codes']),
                    '|'.join(sorted(annotations['go_terms']))
                ])
        
        print(f"Completed {input_file}. Total rows: {row_count}, Filtered rows: {filtered_count}")
        return row_count, filtered_count
            
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")
        return row_count, filtered_count

if __name__ == "__main__":
    # Directory and file pattern
    input_dir = r"C:\Users\Deepak Singh\Documents\majorProjectDocs\gene2go"
    file_pattern = "split_part_gene2go_*"
    output_tsv = r"C:\Users\Deepak Singh\Desktop\majorPBackend\dataProcessing\finalDataset\gene2go.tsv"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_tsv), exist_ok=True)
    
    # Find all matching files
    input_files = glob.glob(os.path.join(input_dir, file_pattern))
    print(f"Found {len(input_files)} files matching pattern '{file_pattern}':")
    for f in input_files:
        print(f" - {os.path.basename(f)}")
    
    if not input_files:
        print(f"No files found in {input_dir} matching pattern '{file_pattern}'.")
    else:
        total_rows_all = 0
        total_filtered_all = 0
        
        # Process each file
        for input_file in input_files:
            rows, filtered = process_gene2go(input_file, output_tsv)
            total_rows_all += rows
            total_filtered_all += filtered
        
        print(f"\nAll files processed. Total rows across all files: {total_rows_all}")
        print(f"Total human gene annotations extracted: {total_filtered_all}")
        print(f"Results saved to: {output_tsv}")