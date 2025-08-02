import csv
import os
import pandas as pd
from collections import defaultdict

def process_mim2gene(input_file, output_file):
    """
    Process mim2gene_medgen file to extract disease associations for human genes.
    
    Args:
        input_file (str): Path to input mim2gene_medgen file
        output_file (str): Path to output file
    Returns:
        tuple: (total_rows_processed, processed_rows) for the file
    """
    print(f"Processing file: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist.")
        return 0, 0
    
    # Dictionary to store disease associations per gene
    gene_diseases = defaultdict(lambda: {
        'tax_id': '9606',  # Since this is human-specific
        'MIM_numbers': set(),
        'phenotype_count': 0,
        'gene_count': 0,
        'nondisease_count': 0,
        'susceptibility_count': 0,
        'questionable_count': 0,
        'somatic_count': 0,
        'MedGenCUIs': set(),
        'sources': set()
    })
    
    row_count = 0
    processed_count = 0
    
    try:
        with open(input_file, 'r', newline='') as infile:
            reader = csv.reader(infile, delimiter='\t')
            
            # Skip header if it exists
            next(reader, None)
            
            for row in reader:
                row_count += 1
                
                # Skip empty rows or rows without enough columns
                if not row or len(row) < 6:
                    continue
                
                mim_number, gene_id, type_, source, medgen_cui, comment = row
                
                # Skip rows without GeneID
                if gene_id == '-':
                    continue
                
                # Process the row
                gene_diseases[gene_id]['MIM_numbers'].add(mim_number)
                
                # Count by type
                if type_ == 'phenotype':
                    gene_diseases[gene_id]['phenotype_count'] += 1
                elif type_ == 'gene':
                    gene_diseases[gene_id]['gene_count'] += 1
                
                # Count by comment
                if comment == 'nondisease':
                    gene_diseases[gene_id]['nondisease_count'] += 1
                elif comment == 'susceptibility':
                    gene_diseases[gene_id]['susceptibility_count'] += 1
                elif comment == 'question':
                    gene_diseases[gene_id]['questionable_count'] += 1
                elif comment == 'somatic':
                    gene_diseases[gene_id]['somatic_count'] += 1
                
                # Add MedGenCUI if present
                if medgen_cui != '-':
                    gene_diseases[gene_id]['MedGenCUIs'].add(medgen_cui)
                
                # Add source if present
                if source != '-':
                    gene_diseases[gene_id]['sources'].add(source)
                
                processed_count += 1
                
                if processed_count % 1000 == 0:
                    print(f"Processed {processed_count} rows...")
        
        # Write processed data to output file
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter='\t', lineterminator='\n')
            
            # Write header
            writer.writerow([
                'tax_id',
                'GeneID',
                'total_MIM_numbers',
                'phenotype_count',
                'gene_count',
                'nondisease_count',
                'susceptibility_count',
                'questionable_count',
                'somatic_count',
                'total_MedGenCUIs',
                'MIM_numbers_list',
                'MedGenCUIs_list',
                'sources_list'
            ])
            
            # Write gene disease associations
            for gene_id, data in gene_diseases.items():
                writer.writerow([
                    data['tax_id'],
                    gene_id,
                    len(data['MIM_numbers']),
                    data['phenotype_count'],
                    data['gene_count'],
                    data['nondisease_count'],
                    data['susceptibility_count'],
                    data['questionable_count'],
                    data['somatic_count'],
                    len(data['MedGenCUIs']),
                    '|'.join(sorted(data['MIM_numbers'])),
                    '|'.join(sorted(data['MedGenCUIs'])),
                    '|'.join(sorted(data['sources']))
                ])
        
        print(f"Completed processing. Total rows: {row_count}, Processed rows: {processed_count}")
        return row_count, processed_count
            
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return row_count, processed_count

if __name__ == "__main__":
    # File paths
    input_file = r"C:\Users\Deepak Singh\Desktop\majorPBackend\dataProcessing\mim2gene_medgen"
    output_file = r"C:\Users\Deepak Singh\Desktop\majorPBackend\dataProcessing\finalDataset\gene_disease_features.tsv"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Process the file
    total_rows, processed_rows = process_mim2gene(input_file, output_file)
    
    print(f"\nProcessing complete:")
    print(f"Total rows in input file: {total_rows}")
    print(f"Rows processed and saved: {processed_rows}")
    print(f"Output saved to: {output_file}")