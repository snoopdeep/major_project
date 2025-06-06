import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

def prepare_training_data():
    """
    Prepare training and testing data for autoencoder using only final_merged_raw.csv.
    """
    print("Loading processed dataset...")
    
    # Load the preprocessed data
    final_dataset = pd.read_csv('dataProcessing/finalDataset/final_merged_raw.csv', low_memory=False)
    
    # Print initial dataset size
    print(f"\nTotal number of genes: {len(final_dataset)}")
    
    # Print value counts for debugging
    print("\nValue distributions:")
    print("\nPhenotype count distribution:")
    print(final_dataset['phenotype_count'].value_counts().head())
    print("\nGene count distribution:")
    print(final_dataset['gene_count'].value_counts().head())
    print("\nMIM numbers distribution:")
    print(final_dataset['total_MIM_numbers'].value_counts().head())
    
    # Define normal genes based on absolute thresholds
    normal_genes = final_dataset[
        (final_dataset['phenotype_count'] <= 1) &
        (final_dataset['gene_count'] <= 1) &
        (final_dataset['total_MIM_numbers'] <= 1)
    ]
    
    print(f"\nNumber of normal genes: {len(normal_genes)}")
    
    # Define potential anomalies
    potential_anomalies = final_dataset[
        (final_dataset['phenotype_count'] > 1) |
        (final_dataset['gene_count'] > 1) |
        (final_dataset['total_MIM_numbers'] > 1)
    ]
    
    print(f"Number of potential anomalies: {len(potential_anomalies)}")
    
    # Split normal genes into training and testing
    train_normal, test_normal = train_test_split(
        normal_genes, 
        test_size=0.2, 
        random_state=42
    )
    
    # Combine test_normal with potential_anomalies for testing
    test_data = pd.concat([test_normal, potential_anomalies])
    
    # Create output directory if it doesn't exist
    os.makedirs('dataProcessing/finalDataset', exist_ok=True)
    
    # Save the datasets
    print("\nSaving datasets...")
    train_normal.to_csv('dataProcessing/finalDataset/train_data.csv', index=False)
    test_data.to_csv('dataProcessing/finalDataset/test_data.csv', index=False)
    
    # Print statistics
    print("\nDataset Statistics:")
    print(f"Training data size: {len(train_normal)} genes")
    print(f"Testing data size: {len(test_data)} genes")
    print(f"Number of potential anomalies: {len(potential_anomalies)} genes")
    
    # Save metadata
    metadata = {
        'train_size': len(train_normal),
        'test_size': len(test_data),
        'anomalies_size': len(potential_anomalies),
        'normal_genes_in_test': len(test_normal),
        'features_used': list(final_dataset.columns)
    }
    
    import json
    with open('dataProcessing/finalDataset/training_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)

if __name__ == "__main__":
    prepare_training_data() 