# import csv
# import os

# def filter_tax_id(input_file, output_file, tax_id="9606"):
#     """
#     Filter TSV file rows by tax_id (first column) and append to output file.
    
#     Args:
#         input_file (str): Path to input TSV file
#         output_file (str): Path to output TSV file
#         tax_id (str): Tax ID to filter (default: "9606")
#     """
#     print(f"Input file: {input_file}")
#     print(f"Output file: {output_file}")
    
#     if not os.path.exists(input_file):
#         print(f"Error: Input file {input_file} does not exist.")
#         return
    
#     row_count = 0
#     filtered_count = 0
    
#     try:
#         with open(input_file, 'r', newline='') as infile, \
#              open(output_file, 'a', newline='') as outfile:
            
#             reader = csv.reader(infile, delimiter='\t')
#             writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
            
#             print("Starting to process rows...")
#             for row in reader:
#                 row_count += 1
#                 if row and row[0] == tax_id:  # Check if first column is the desired tax_id
#                     writer.writerow(row)
#                     filtered_count += 1
#                     print(f"Filtered row {filtered_count}: {row[:3]}...")  # Print first 3 columns for brevity
                
#                 if row_count % 1000 == 0:  # Print progress every 1000 rows
#                     print(f"Processed {row_count} rows...")
            
#             print(f"Completed. Total rows processed: {row_count}")
#             print(f"Rows with tax_id {tax_id}: {filtered_count}")
            
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")

# if __name__ == "__main__":
#     # File paths
#     input_tsv = r"C:\Users\Deepak Singh\Documents\majorProjectDocs\gene_neighbors\split_part_gene_neighbors_ac"
#     output_tsv = r"C:\Users\Deepak Singh\Desktop\majorPBackend\dataProcessing\output_9606.tsv"
#     filter_tax_id(input_tsv, output_tsv)


import csv
import os
import glob

def filter_tax_id(input_file, output_file, tax_id="9606"):
    """
    Filter TSV file rows by tax_id (first column) and append to output file.
    
    Args:
        input_file (str): Path to input TSV file
        output_file (str): Path to output TSV file
        tax_id (str): Tax ID to filter (default: "9606")
    Returns:
        tuple: (total_rows_processed, filtered_rows) for the file
    """
    print(f"Processing file: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist.")
        return 0, 0
    
    row_count = 0
    filtered_count = 0
    
    try:
        with open(input_file, 'r', newline='') as infile, \
             open(output_file, 'a', newline='') as outfile:
            
            reader = csv.reader(infile, delimiter='\t')
            writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
            
            for row in reader:
                row_count += 1
                if row and row[0] == tax_id:  # Check if first column is the desired tax_id
                    writer.writerow(row)
                    filtered_count += 1
                    print(f"Filtered row {filtered_count} in {os.path.basename(input_file)}: {row[:3]}...")
                
                if row_count % 1000 == 0:  # Print progress every 1000 rows
                    print(f"Processed {row_count} rows in {os.path.basename(input_file)}...")
            
            print(f"Completed {input_file}. Total rows: {row_count}, Filtered rows: {filtered_count}")
            return row_count, filtered_count
            
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")
        return row_count, filtered_count

if __name__ == "__main__":
    # Directory and file pattern
    input_dir = r"C:\Users\Deepak Singh\Documents\majorProjectDocs\gene_neighbors"
    file_pattern = "split_part_gene_neighbors_*"
    output_tsv = r"C:\Users\Deepak Singh\Desktop\majorPBackend\dataProcessing\output_9606.tsv"
    
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
            rows, filtered = filter_tax_id(input_file, output_tsv)
            total_rows_all += rows
            total_filtered_all += filtered
        
        print(f"\nAll files processed. Total rows across all files: {total_rows_all}")
        print(f"Total rows with tax_id 9606: {total_filtered_all}")
        print(f"Results appended to: {output_tsv}")