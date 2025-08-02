import csv
import os
import glob

def process_gene_info(input_file, output_file, tax_id="9606"):
    """
    Process gene_info file to extract human genes and specific columns.
    
    Args:
        input_file (str): Path to input gene_info file
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
        'Symbol': 2,
        'chromosome': 6,
        'type_of_gene': 8,
        'description': 7
    }
    
    row_count = 0
    filtered_count = 0
    
    try:
        with open(input_file, 'r', newline='') as infile, \
             open(output_file, 'a', newline='') as outfile:
            
            reader = csv.reader(infile, delimiter='\t')
            writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
            
            # Write header if file is empty
            if os.path.getsize(output_file) == 0:
                writer.writerow(['tax_id', 'GeneID', 'Symbol', 'chromosome', 'type_of_gene', 'description'])
            
            for row in reader:
                row_count += 1
                
                # Check if row has enough columns
                if len(row) < max(required_columns.values()) + 1:
                    continue
                
                # Filter for human genes and extract required columns
                if row[required_columns['tax_id']] == tax_id:
                    filtered_row = [
                        row[required_columns['tax_id']],
                        row[required_columns['GeneID']],
                        row[required_columns['Symbol']],
                        row[required_columns['chromosome']],
                        row[required_columns['type_of_gene']],
                        row[required_columns['description']]
                    ]
                    writer.writerow(filtered_row)
                    filtered_count += 1
                    
                    if filtered_count % 1000 == 0:
                        print(f"Filtered {filtered_count} rows in {os.path.basename(input_file)}...")
                
                if row_count % 10000 == 0:
                    print(f"Processed {row_count} rows in {os.path.basename(input_file)}...")
            
            print(f"Completed {input_file}. Total rows: {row_count}, Filtered rows: {filtered_count}")
            return row_count, filtered_count
            
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")
        return row_count, filtered_count

if __name__ == "__main__":
    # Directory and file pattern
    input_dir = r"C:\Users\Deepak Singh\Documents\majorProjectDocs\gene_info"
    file_pattern = "split_part_gene_info*"
    output_tsv = r"C:\Users\Deepak Singh\Desktop\majorPBackend\dataProcessing\finalDataset\human_genes_info.tsv"
    
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
            rows, filtered = process_gene_info(input_file, output_tsv)
            total_rows_all += rows
            total_filtered_all += filtered
        
        print(f"\nAll files processed. Total rows across all files: {total_rows_all}")
        print(f"Total human genes extracted: {total_filtered_all}")
        print(f"Results saved to: {output_tsv}")