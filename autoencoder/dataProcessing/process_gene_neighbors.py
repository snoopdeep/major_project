import csv
import os
import pandas as pd

def process_gene_neighbors(input_file, output_file):
    """
    Process gene_neighbors file to extract spatial features for human genes.
    
    Args:
        input_file (str): Path to input gene_neighbors file
        output_file (str): Path to output file
    Returns:
        tuple: (total_rows_processed, processed_rows) for the file
    """
    print(f"Processing file: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist.")
        return 0, 0
    
    # Define required columns and their indices
    required_columns = {
        'GeneID': 1,
        'start_position': 4,
        'end_position': 5,
        'chromosome': 7,
        'GeneIDs_on_left': 8,
        'distance_to_left': 9,
        'GeneIDs_on_right': 10,
        'distance_to_right': 11,
        'overlapping_GeneIDs': 12
    }
    
    row_count = 0
    processed_count = 0
    
    try:
        with open(input_file, 'r', newline='') as infile, \
             open(output_file, 'w', newline='') as outfile:
            
            reader = csv.reader(infile, delimiter='\t')
            writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
            
            # Write header
            writer.writerow([
                'GeneID',
                'start_position',
                'end_position',
                'chromosome',
                'gene_length',
                'left_neighbors_count',
                'right_neighbors_count',
                'overlapping_genes_count',
                'distance_to_left',
                'distance_to_right'
            ])
            
            for row in reader:
                row_count += 1
                
                # Check if row has enough columns
                if len(row) < max(required_columns.values()) + 1:
                    continue
                
                # Extract and process required columns
                gene_id = row[required_columns['GeneID']]
                start_pos = int(row[required_columns['start_position']])
                end_pos = int(row[required_columns['end_position']])
                chromosome = row[required_columns['chromosome']]
                
                # Calculate gene length
                gene_length = end_pos - start_pos
                
                # Process left neighbors
                left_neighbors = row[required_columns['GeneIDs_on_left']]
                left_neighbors_count = len(left_neighbors.split('|')) if left_neighbors != '-' else 0
                distance_to_left = int(row[required_columns['distance_to_left']]) if row[required_columns['distance_to_left']] != '-' else -1
                
                # Process right neighbors
                right_neighbors = row[required_columns['GeneIDs_on_right']]
                right_neighbors_count = len(right_neighbors.split('|')) if right_neighbors != '-' else 0
                distance_to_right = int(row[required_columns['distance_to_right']]) if row[required_columns['distance_to_right']] != '-' else -1
                
                # Process overlapping genes
                overlapping_genes = row[required_columns['overlapping_GeneIDs']]
                overlapping_genes_count = len(overlapping_genes.split('|')) if overlapping_genes != '-' else 0
                
                # Write processed row
                processed_row = [
                    gene_id,
                    start_pos,
                    end_pos,
                    chromosome,
                    gene_length,
                    left_neighbors_count,
                    right_neighbors_count,
                    overlapping_genes_count,
                    distance_to_left,
                    distance_to_right
                ]
                writer.writerow(processed_row)
                processed_count += 1
                
                if processed_count % 1000 == 0:
                    print(f"Processed {processed_count} rows...")
            
            print(f"Completed processing. Total rows: {row_count}, Processed rows: {processed_count}")
            return row_count, processed_count
            
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return row_count, processed_count

if __name__ == "__main__":
    # File paths
    input_file = r"C:\Users\Deepak Singh\Desktop\majorPBackend\dataProcessing\gene_neighbours_9606.tsv"
    output_file = r"C:\Users\Deepak Singh\Desktop\majorPBackend\dataProcessing\finalDataset\gene_spatial_features.tsv"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Process the file
    total_rows, processed_rows = process_gene_neighbors(input_file, output_file)
    
    print(f"\nProcessing complete:")
    print(f"Total rows in input file: {total_rows}")
    print(f"Rows processed and saved: {processed_rows}")
    print(f"Output saved to: {output_file}")