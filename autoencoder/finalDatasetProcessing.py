import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def prepare_final_dataset():
    """
    Combine all processed datasets and prepare final feature set for anomaly detection.
    """
    print("Loading processed datasets...")
    
    # Load all datasets with correct file names and paths
    try:
        gene_info = pd.read_csv('dataProcessing/finalDataset/human_genes_info.tsv', sep='\t', low_memory=False)
        print("Loaded gene_info successfully")
        
        gene_neighbors = pd.read_csv('dataProcessing/finalDataset/human_gene_neighbours.tsv', sep='\t', low_memory=False)
        print("Loaded gene_neighbors successfully")
        
        gene2go = pd.read_csv('dataProcessing/finalDataset/gene2go.tsv', sep='\t', low_memory=False)
        print("Loaded gene2go successfully")
        
        mim2gene = pd.read_csv('dataProcessing/finalDataset/mim2gene.tsv', sep='\t', low_memory=False)
        print("Loaded mim2gene successfully")
        
    except FileNotFoundError as e:
        print(f"Error loading files: {str(e)}")
        print("Please check if the following files exist:")
        print("1. dataProcessing/finalDataset/human_genes_info.tsv")
        print("2. dataProcessing/finalDataset/human_gene_neighbours.tsv")
        print("3. dataProcessing/finalDataset/gene2go.tsv")
        print("4. dataProcessing/finalDataset/gene_disease_features.tsv")
        return
    
    print("\nMerging datasets...")
    
    # Merge all datasets on GeneID
    try:
        final_dataset = gene_info.merge(
            gene_neighbors, on='GeneID', how='left'
        ).merge(
            gene2go, on='GeneID', how='left'
        ).merge(
            mim2gene, on='GeneID', how='left'
        )
        print("Datasets merged successfully")
        print("\nAvailable columns after merge:")
        print(final_dataset.columns.tolist())
        
        final_dataset.to_csv('dataProcessing/finalDataset/final_merged_raw.csv', index=False)
        
    except Exception as e:
        print(f"Error merging datasets: {str(e)}")
        return
    
    # Fill missing values
    final_dataset = final_dataset.fillna({
        'total_go_terms': 0,
        'Function_terms': 0,
        'Process_terms': 0,
        'Component_terms': 0,
        'unique_evidence_codes': 0,
        'total_MIM_numbers': 0,
        'phenotype_count': 0,
        'gene_count': 0,
        'nondisease_count': 0,
        'susceptibility_count': 0,
        'questionable_count': 0,
        'somatic_count': 0,
        'total_MedGenCUIs': 0
    })
    
    # Prepare feature sets
    print("\nPreparing feature sets...")
    
    # 1. Basic Gene Features
    basic_features = [
        'gene_length'
    ]
    
    # 2. Spatial Features
    spatial_features = [
        'left_neighbors_count',
        'right_neighbors_count',
        'overlapping_genes_count',
        'distance_to_left',
        'distance_to_right'
    ]
    
    # 3. Functional Features
    functional_features = [
        'total_go_terms',
        'Function_terms',
        'Process_terms',
        'Component_terms',
        'unique_evidence_codes'
    ]
    
    # 4. Disease Features
    disease_features = [
        'total_MIM_numbers',
        'phenotype_count',
        'gene_count',
        'nondisease_count',
        'susceptibility_count',
        'questionable_count',
        'somatic_count',
        'total_MedGenCUIs'
    ]
    
    # 5. Categorical Features
    categorical_features = [
        'chromosome_x',
        'type_of_gene'
    ]
    
    # Create feature preprocessing pipeline
    print("Creating preprocessing pipeline...")
    
    # Numerical features preprocessing
    numerical_features = basic_features + spatial_features + functional_features + disease_features
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    # Categorical features preprocessing
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # Apply preprocessing
    print("Applying preprocessing...")
    X = preprocessor.fit_transform(final_dataset)
    
    # Save preprocessed data
    print("Saving preprocessed data...")
    np.save('dataProcessing/finalDataset/preprocessed_features.npy', X)
    
    # Save feature names
    feature_names = (
        numerical_features +
        [f"{col}_{val}" for col, vals in 
         zip(categorical_features, 
             preprocessor.named_transformers_['cat'].named_steps['onehot'].categories_)
         for val in vals]
    )
    
    with open('dataProcessing/finalDataset/feature_names.txt', 'w') as f:
        f.write('\n'.join(feature_names))
    
    # Save metadata
    metadata = {
        'total_genes': len(final_dataset),
        'total_features': X.shape[1],
        'numerical_features': len(numerical_features),
        'categorical_features': len(categorical_features),
        'feature_categories': {
            'basic_features': len(basic_features),
            'spatial_features': len(spatial_features),
            'functional_features': len(functional_features),
            'disease_features': len(disease_features),
            'categorical_features': len(categorical_features)
        }
    }
    
    import json
    with open('dataProcessing/finalDataset/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)
    
    print("\nFinal dataset preparation complete!")
    print(f"Total genes: {metadata['total_genes']}")
    print(f"Total features: {metadata['total_features']}")
    print("\nFeature categories:")
    for category, count in metadata['feature_categories'].items():
        print(f"- {category}: {count} features")

if __name__ == "__main__":
    prepare_final_dataset()