import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import os
import time
import joblib

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

class GeneAutoencoder(nn.Module):
    def __init__(self, input_dim):
        super(GeneAutoencoder, self).__init__()
        
        # Encoder - Simplified architecture
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, 32)  # Latent space
        )
        
        # Decoder - Simplified architecture
        self.decoder = nn.Sequential(
            nn.Linear(32, 64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, input_dim),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded
    
    def predict(self, x):
        """Method for analysis that returns only the reconstruction."""
        _, decoded = self(x)
        return decoded

def preprocess_list_column(df, column):
    """Convert list-type column to numeric features."""
    # Convert column to string type and handle NaN values
    df[column] = df[column].astype(str)
    df[column] = df[column].replace('nan', '')
    
    # Count the number of items in the list
    df[f'{column}_count'] = df[column].apply(lambda x: len(str(x).split('|')) if x != '' else 0)
    
    # If the column is empty, set count to 0
    df[f'{column}_count'] = df[f'{column}_count'].replace(0, 1)
    
    return df

def load_and_preprocess_data(sample_size=None):
    """Load and preprocess the training and testing data."""
    print("Loading data...")
    
    # Load training data (normal genes)
    train_data = pd.read_csv('dataProcessing/finalDataset/train_data.csv', low_memory=False)
    test_data = pd.read_csv('dataProcessing/finalDataset/test_data.csv', low_memory=False)
    
    # Store original columns
    original_columns = train_data.columns.tolist()
    
    # If sample_size is specified, use only that many samples
    if sample_size is not None:
        print(f"Using {sample_size} samples for training")
        train_data = train_data.sample(n=sample_size, random_state=42)
    
    # Define non-feature columns
    non_feature_cols = ['GeneID', 'Symbol', 'description']
    
    # List-type columns that need special handling
    list_columns = ['MIM_numbers_list', 'MedGenCUIs_list', 'go_terms_list', 'sources_list']
    
    # Preprocess list columns
    for col in list_columns:
        if col in train_data.columns:
            print(f"Preprocessing list column: {col}")
            train_data = preprocess_list_column(train_data, col)
            test_data = preprocess_list_column(test_data, col)
    
    # Get all columns
    all_cols = train_data.columns.tolist()
    
    # Identify numeric columns (excluding non-feature columns and list columns)
    numeric_cols = []
    for col in all_cols:
        if col not in non_feature_cols and col not in list_columns:
            try:
                # Try to convert to numeric
                pd.to_numeric(train_data[col], errors='raise')
                numeric_cols.append(col)
            except:
                continue
    
    # Add the count columns from list preprocessing
    numeric_cols.extend([f'{col}_count' for col in list_columns if col in train_data.columns])
    
    # All remaining columns (excluding non-feature columns and list columns) are categorical
    categorical_cols = [col for col in all_cols 
                       if col not in non_feature_cols 
                       and col not in list_columns 
                       and col not in numeric_cols]
    
    print(f"\nNumber of numeric features: {len(numeric_cols)}")
    print(f"Number of categorical features: {len(categorical_cols)}")
    
    print("\nNumeric features:", numeric_cols)
    print("\nCategorical features:", categorical_cols)
    
    # Create preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
        ])
    
    # Fit and transform training data
    print("\nPreprocessing training data...")
    X_train = preprocessor.fit_transform(train_data)
    
    # Transform test data
    print("Preprocessing test data...")
    X_test = preprocessor.transform(test_data)
    
    print(f"Final feature dimension after preprocessing: {X_train.shape[1]}")
    
    # Get feature names after preprocessing
    feature_names = numeric_cols.copy()
    for col in categorical_cols:
        # Get unique values for each categorical column
        unique_values = pd.get_dummies(train_data[col]).columns
        feature_names.extend([f"{col}_{val}" for val in unique_values])
    
    # Convert to PyTorch tensors
    train_tensor = torch.FloatTensor(X_train).to(device)
    test_tensor = torch.FloatTensor(X_test).to(device)
    
    return train_tensor, test_tensor, feature_names, original_columns

def train_autoencoder(model, train_data, epochs=50, batch_size=64, lr=0.0005):
    """Train the autoencoder."""
    print("Training autoencoder...")
    start_time = time.time()
    
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, betas=(0.9, 0.999))
    
    # Create data loader
    train_dataset = torch.utils.data.TensorDataset(train_data)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    losses = []
    best_loss = float('inf')
    patience = 10
    patience_counter = 0
    
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        valid_batches = 0
        
        for batch in train_loader:
            data = batch[0]
            
            # Forward pass
            encoded, decoded = model(data)
            loss = criterion(decoded, data)
            
            # Skip if loss is NaN
            if torch.isnan(loss):
                continue
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            
            epoch_loss += loss.item()
            valid_batches += 1
        
        if valid_batches > 0:
            avg_loss = epoch_loss / valid_batches
            losses.append(avg_loss)
            
            # Early stopping
            if avg_loss < best_loss:
                best_loss = avg_loss
                patience_counter = 0
                # Save best model
                torch.save(model.state_dict(), 'results/best_model.pth')
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    print(f"Early stopping at epoch {epoch+1}")
                    break
            
            if (epoch + 1) % 2 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}')
    
    training_time = time.time() - start_time
    print(f"Training completed in {training_time/60:.2f} minutes")
    return losses

def detect_anomalies(model, test_data, threshold_percentile=95):
    """Detect anomalies in the test data."""
    print("Detecting anomalies...")
    
    model.eval()
    with torch.no_grad():
        # Get reconstruction errors for all test data
        encoded, decoded = model(test_data)
        reconstruction_errors = torch.mean((decoded - test_data) ** 2, dim=1)
        
        # Handle NaN values
        if torch.isnan(reconstruction_errors).any():
            print("Warning: NaN values detected in reconstruction errors")
            # Replace NaN values with the maximum non-NaN value
            valid_errors = reconstruction_errors[~torch.isnan(reconstruction_errors)]
            if len(valid_errors) > 0:
                max_valid_error = torch.max(valid_errors)
                reconstruction_errors = torch.where(torch.isnan(reconstruction_errors), 
                                                 max_valid_error, 
                                                 reconstruction_errors)
            else:
                print("Error: All reconstruction errors are NaN")
                return None, None, None
        
        # Calculate threshold
        threshold = np.percentile(reconstruction_errors.cpu().numpy(), threshold_percentile)
        
        # Identify anomalies
        anomalies = reconstruction_errors > threshold
    
    return reconstruction_errors, anomalies, threshold

def plot_results(losses, reconstruction_errors, threshold):
    """Plot training losses and reconstruction errors."""
    plt.figure(figsize=(12, 5))
    
    # Plot training losses
    plt.subplot(1, 2, 1)
    plt.plot(losses)
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    
    # Plot reconstruction errors
    plt.subplot(1, 2, 2)
    errors = reconstruction_errors.cpu().numpy()
    
    # Handle NaN values in plotting
    if np.isnan(errors).any():
        print("Warning: NaN values detected in reconstruction errors for plotting")
        errors = np.nan_to_num(errors, nan=np.nanmax(errors[~np.isnan(errors)]))
    
    plt.hist(errors, bins=50)
    plt.axvline(x=threshold, color='r', linestyle='--', label=f'Threshold ({threshold:.4f})')
    plt.title('Reconstruction Error Distribution')
    plt.xlabel('Reconstruction Error')
    plt.ylabel('Count')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('results/autoencoder_results.png')
    plt.close()

def save_autoencoder_results(model, train_data, test_data, reconstruction_errors, anomalies, threshold, losses, feature_names, original_columns):
    """Save comprehensive autoencoder results."""
    print("Saving detailed autoencoder results...")
    
    # Convert losses to regular Python list if it's not already
    losses_list = [float(loss) for loss in losses] if losses else []
    
    # Save model architecture and parameters
    model_info = {
        'architecture': {
            'input_dim': int(train_data.shape[1]),
            'encoder_layers': [256, 64, 32],
            'decoder_layers': [64, 256, int(train_data.shape[1])]
        },
        'training': {
            'losses': losses_list,
            'final_loss': float(losses[-1]) if losses else None,
            'training_samples': int(train_data.shape[0])
        },
        'anomaly_detection': {
            'threshold': float(threshold),
            'anomaly_count': int(anomalies.sum().item()),
            'total_samples': int(len(anomalies)),
            'anomaly_percentage': float((anomalies.sum().item() / len(anomalies)) * 100)
        }
    }
    
    # Save reconstruction errors distribution
    error_stats = {
        'mean': float(reconstruction_errors.mean().item()),
        'std': float(reconstruction_errors.std().item()),
        'min': float(reconstruction_errors.min().item()),
        'max': float(reconstruction_errors.max().item()),
        'percentiles': {
            '25': float(np.percentile(reconstruction_errors.cpu().numpy(), 25)),
            '50': float(np.percentile(reconstruction_errors.cpu().numpy(), 50)),
            '75': float(np.percentile(reconstruction_errors.cpu().numpy(), 75)),
            '95': float(np.percentile(reconstruction_errors.cpu().numpy(), 95))
        }
    }
    
    # Save all results
    results = {
        'model_info': model_info,
        'error_stats': error_stats,
        'reconstruction_errors': reconstruction_errors.cpu().numpy(),
        'anomalies': anomalies.cpu().numpy()
    }
    
    # Save in multiple formats
    np.save('results/autoencoder_results.npy', results)
    
    # Save as JSON for better readability
    import json
    with open('results/autoencoder_results.json', 'w') as f:
        json.dump({
            'model_info': model_info,
            'error_stats': error_stats
        }, f, indent=4)
    
    try:
        # Load original test data to get the original columns
        test_data_original = pd.read_csv('dataProcessing/finalDataset/test_data.csv')
        
        # Create DataFrame with original features
        anomaly_details = test_data_original.copy()
        anomaly_details['reconstruction_error'] = reconstruction_errors.cpu().numpy()
        anomaly_details['is_anomaly'] = anomalies.cpu().numpy()
        
        # Save full details with original features
        anomaly_details.to_csv('results/anomaly_details_full.csv', index=False)
        
        # Save summary (just the most important columns)
        summary_cols = ['GeneID', 'Symbol', 'description', 'reconstruction_error', 'is_anomaly']
        anomaly_details[summary_cols].to_csv('results/anomaly_details_summary.csv', index=False)
        
        print("✓ Anomaly details saved successfully")
        
    except Exception as e:
        print(f"Warning: Error saving anomaly details: {str(e)}")
        print("Saving basic anomaly information only...")
        
        # Save basic anomaly information
        basic_details = pd.DataFrame({
            'reconstruction_error': reconstruction_errors.cpu().numpy(),
            'is_anomaly': anomalies.cpu().numpy()
        })
        basic_details.to_csv('results/anomaly_details_basic.csv', index=False)
    
    print("✓ Detailed results saved in multiple formats")

def train_and_save_model(train_data, input_dim, epochs=50, batch_size=128, lr=0.001):
    """Train the model and save it along with necessary metadata."""
    print("\nTraining new model...")
    model = GeneAutoencoder(input_dim).to(device)
    losses = train_autoencoder(model, train_data, epochs, batch_size, lr)
    
    # Save model and metadata
    torch.save({
        'model_state_dict': model.state_dict(),
        'input_dim': input_dim,
        'architecture': '256-64-32-64-256',
        'losses': losses
    }, 'results/model_checkpoint.pth')
    
    print("✓ Model saved to 'results/model_checkpoint.pth'")
    return model, losses

def save_preprocessor(preprocessor, feature_names):
    """Save the preprocessor and feature names."""
    preprocessor_data = {
        'preprocessor': preprocessor,
        'feature_names': feature_names
    }
    joblib.dump(preprocessor_data, 'results/preprocessor.joblib')
    print("✓ Preprocessor saved to 'results/preprocessor.joblib'")

def load_preprocessor():
    """Load the saved preprocessor and feature names."""
    try:
        preprocessor_data = joblib.load('results/preprocessor.joblib')
        return preprocessor_data['preprocessor'], preprocessor_data['feature_names']
    except Exception as e:
        print(f"Error loading preprocessor: {str(e)}")
        return None, None

def test_model(model_path, test_data_path):
    """Test a pre-trained model on new data."""
    print("\nTesting pre-trained model...")
    
    try:
        # Load the model
        checkpoint = torch.load(model_path)
        model = GeneAutoencoder(checkpoint['input_dim']).to(device)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        
        # Load preprocessor
        preprocessor, feature_names = load_preprocessor()
        if preprocessor is None:
            print("Error: Preprocessor not found. Please train the model first.")
            return None
        
        # Load test data
        test_data = pd.read_csv(test_data_path)
        
        # Preprocess test data using saved preprocessor
        test_tensor, _, _ = preprocess_data(test_data, preprocessor=preprocessor, is_training=False)
        
        # Detect anomalies
        reconstruction_errors, anomalies, threshold = detect_anomalies(model, test_tensor)
        
        # Save test results
        test_results = {
            'reconstruction_errors': reconstruction_errors.cpu().numpy(),
            'anomalies': anomalies.cpu().numpy(),
            'threshold': threshold
        }
        
        # Create results directory if it doesn't exist
        os.makedirs('test_results', exist_ok=True)
        
        # Save results
        np.save('test_results/test_results.npy', test_results)
        
        # Save detailed results
        test_data['reconstruction_error'] = reconstruction_errors.cpu().numpy()
        test_data['is_anomaly'] = anomalies.cpu().numpy()
        
        # Save full results
        test_data.to_csv('test_results/test_results_full.csv', index=False)
        
        # Save summary results
        summary_cols = ['GeneID', 'Symbol', 'description', 'reconstruction_error', 'is_anomaly']
        test_data[summary_cols].to_csv('test_results/test_results_summary.csv', index=False)
        
        print(f"\nTest Results:")
        print(f"Total samples: {len(anomalies)}")
        print(f"Anomalies detected: {anomalies.sum().item()}")
        print(f"Anomaly percentage: {(anomalies.sum().item() / len(anomalies)) * 100:.2f}%")
        print("\nResults saved in 'test_results' directory:")
        print("- test_results.npy: Raw results")
        print("- test_results_full.csv: Complete results with all features")
        print("- test_results_summary.csv: Summary with key information")
        
        return test_results
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        return None

def preprocess_data(data, preprocessor=None, is_training=False):
    """Preprocess data for model input."""
    # Define non-feature columns
    non_feature_cols = ['GeneID', 'Symbol', 'description']
    
    # List-type columns that need special handling
    list_columns = ['MIM_numbers_list', 'MedGenCUIs_list', 'go_terms_list', 'sources_list']
    
    # Preprocess list columns
    for col in list_columns:
        if col in data.columns:
            data = preprocess_list_column(data, col)
    
    # Get all columns
    all_cols = data.columns.tolist()
    
    # Identify numeric columns
    numeric_cols = []
    for col in all_cols:
        if col not in non_feature_cols and col not in list_columns:
            try:
                pd.to_numeric(data[col], errors='raise')
                numeric_cols.append(col)
            except:
                continue
    
    # Add count columns from list preprocessing
    numeric_cols.extend([f'{col}_count' for col in list_columns if col in data.columns])
    
    # Identify categorical columns
    categorical_cols = [col for col in all_cols 
                       if col not in non_feature_cols 
                       and col not in list_columns 
                       and col not in numeric_cols]
    
    # Create preprocessing pipeline if not provided
    if preprocessor is None:
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
            ])
    
    # Transform data
    if is_training:
        X = preprocessor.fit_transform(data)
    else:
        X = preprocessor.transform(data)
    
    # Get feature names
    feature_names = numeric_cols.copy()
    for col in categorical_cols:
        unique_values = pd.get_dummies(data[col]).columns
        feature_names.extend([f"{col}_{val}" for val in unique_values])
    
    # Convert to PyTorch tensor
    tensor = torch.FloatTensor(X).to(device)
    
    return tensor, preprocessor, feature_names

def main(skip_training=False, sample_size=None):
    print("\n" + "="*50)
    print("GENE ANOMALY DETECTION PIPELINE")
    print("="*50)
    
    # Create output directory
    print("\n1. Setting up directories...")
    os.makedirs('results', exist_ok=True)
    os.makedirs('results/plots', exist_ok=True)
    os.makedirs('results/analysis', exist_ok=True)
    print("✓ Directories created")
    
    # Load and preprocess data
    print("\n2. Loading and preprocessing data...")
    train_data, test_data, feature_names, original_columns = load_and_preprocess_data(sample_size)
    print(f"✓ Data loaded: {train_data.shape[0]} training samples, {test_data.shape[0]} test samples")
    
    # Save preprocessor
    print("\n3. Saving preprocessor...")
    train_data_df = pd.read_csv('dataProcessing/finalDataset/train_data.csv')
    if sample_size is not None:
        train_data_df = train_data_df.sample(n=sample_size, random_state=42)
    _, preprocessor, _ = preprocess_data(train_data_df, is_training=True)
    save_preprocessor(preprocessor, feature_names)
    
    # Initialize or load model
    print("\n4. Model initialization...")
    input_dim = train_data.shape[1]
    
    if skip_training:
        try:
            model, losses = load_model()
            print("✓ Using pre-trained model")
        except FileNotFoundError:
            print("Error: No pre-trained model found. Please train the model first.")
            return
    else:
        model, losses = train_and_save_model(train_data, input_dim)
        print("✓ Model trained and saved")
    
    # Detect anomalies
    print("\n5. Detecting anomalies...")
    result = detect_anomalies(model, test_data)
    if result is None:
        print("Error: Anomaly detection failed due to NaN values")
        return
    
    reconstruction_errors, anomalies, threshold = result
    print(f"  - Threshold: {threshold:.4f}")
    print(f"  - Anomalies detected: {anomalies.sum().item()} out of {len(anomalies)}")
    print("✓ Anomaly detection completed")
    
    # Save detailed autoencoder results
    save_autoencoder_results(model, train_data, test_data, reconstruction_errors, anomalies, threshold, losses, feature_names, original_columns)
    
    # Plot results
    print("\n6. Generating visualizations...")
    plot_results(losses, reconstruction_errors, threshold)
    print("✓ Plots saved to 'results/plots/'")
    
    print("\n" + "="*50)
    print("Pipeline completed successfully!")
    print("="*50 + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Gene Anomaly Detection Pipeline')
    parser.add_argument('--skip-training', action='store_true', help='Skip training and use pre-trained model')
    parser.add_argument('--sample-size', type=int, help='Number of samples to use for training')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    parser.add_argument('--model-path', type=str, default='results/model_checkpoint.pth', help='Path to pre-trained model')
    parser.add_argument('--test-data', type=str, default='dataProcessing/finalDataset/test_data.csv', help='Path to test data')
    args = parser.parse_args()
    
    if args.test:
        test_model(args.model_path, args.test_data)
    else:
        main(skip_training=args.skip_training, sample_size=args.sample_size)