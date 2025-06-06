import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import lime
import lime.tabular
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class GeneticXAIModel:
    """
    Explainable AI model for genetic anomaly detection and mutation analysis.
    """
    
    def _init_(self, autoencoder_model, feature_names, device='cpu'):
        self.autoencoder = autoencoder_model
        self.feature_names = feature_names
        self.device = device
        self.shap_explainer = None
        self.lime_explainer = None
        self.anomaly_classifier = None
        self.feature_importance_scores = None
        
    def setup_explainers(self, background_data, anomaly_labels=None):
        """
        Setup SHAP and LIME explainers for the autoencoder.
        
        Args:
            background_data: Background dataset for SHAP (torch.Tensor)
            anomaly_labels: Binary labels indicating anomalies (numpy array)
        """
        print("Setting up XAI explainers...")
        
        # Convert background data to numpy for explainers
        if isinstance(background_data, torch.Tensor):
            background_np = background_data.cpu().numpy()
        else:
            background_np = background_data
            
        # Setup SHAP explainer for autoencoder
        self.autoencoder.eval()  # Ensure model is in evaluation mode
        
        # Create a wrapper function for SHAP that returns reconstruction error
        def reconstruction_error_func(X):
            """Function that returns reconstruction error for SHAP analysis."""
            if not isinstance(X, torch.Tensor):
                X_tensor = torch.FloatTensor(X).to(self.device)
            else:
                X_tensor = X
                
            with torch.no_grad():
                _, decoded = self.autoencoder(X_tensor)
                # Calculate reconstruction error per sample
                reconstruction_errors = torch.mean((decoded - X_tensor) ** 2, dim=1)
                return reconstruction_errors.cpu().numpy()
        
        # Initialize SHAP explainer
        print("Initializing SHAP explainer...")
        # Use a subset of background data for efficiency
        background_subset = background_np[:min(100, len(background_np))]
        self.shap_explainer = shap.KernelExplainer(reconstruction_error_func, background_subset)
        
        # Setup LIME explainer
        print("Initializing LIME explainer...")
        self.lime_explainer = lime.tabular.LimeTabularExplainer(
            training_data=background_np,
            feature_names=self.feature_names,
            mode='regression',  # We're explaining reconstruction error
            discretize_continuous=True
        )
        
        # If anomaly labels are provided, train a classifier for better interpretability
        if anomaly_labels is not None:
            print("Training anomaly classifier for enhanced interpretation...")
            self.anomaly_classifier = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            self.anomaly_classifier.fit(background_np, anomaly_labels)
            
            # Get feature importance from the classifier
            self.feature_importance_scores = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.anomaly_classifier.feature_importances_
            }).sort_values('importance', ascending=False)
    
    def explain_anomaly(self, anomalous_sample, sample_id=None, top_k_features=20):
        """
        Explain why a specific sample is considered anomalous.
        
        Args:
            anomalous_sample: Single sample to explain (torch.Tensor or numpy array)
            sample_id: Identifier for the sample
            top_k_features: Number of top contributing features to show
            
        Returns:
            Dictionary containing explanation results
        """
        print(f"Explaining anomaly for sample {sample_id if sample_id else 'Unknown'}...")
        
        # Convert to numpy if needed
        if isinstance(anomalous_sample, torch.Tensor):
            sample_np = anomalous_sample.cpu().numpy().reshape(1, -1)
        else:
            sample_np = anomalous_sample.reshape(1, -1)
        
        explanations = {}
        
        # 1. SHAP Explanation
        print("Generating SHAP explanation...")
        try:
            shap_values = self.shap_explainer.shap_values(sample_np, nsamples=100)
            
            # Get top contributing features
            feature_contributions = []
            for i, (feature, shap_val) in enumerate(zip(self.feature_names, shap_values[0])):
                feature_contributions.append({
                    'feature': feature,
                    'shap_value': shap_val,
                    'feature_value': sample_np[0][i],
                    'abs_shap_value': abs(shap_val)
                })
            
            # Sort by absolute SHAP value
            feature_contributions.sort(key=lambda x: x['abs_shap_value'], reverse=True)
            explanations['shap'] = {
                'values': shap_values[0],
                'top_features': feature_contributions[:top_k_features]
            }
            
        except Exception as e:
            print(f"SHAP explanation failed: {e}")
            explanations['shap'] = None
        
        # 2. LIME Explanation
        print("Generating LIME explanation...")
        try:
            # Create prediction function for LIME
            def predict_fn(X):
                X_tensor = torch.FloatTensor(X).to(self.device)
                with torch.no_grad():
                    _, decoded = self.autoencoder(X_tensor)
                    errors = torch.mean((decoded - X_tensor) ** 2, dim=1)
                    return errors.cpu().numpy()
            
            lime_explanation = self.lime_explainer.explain_instance(
                sample_np[0], 
                predict_fn, 
                num_features=top_k_features
            )
            
            explanations['lime'] = {
                'explanation': lime_explanation,
                'top_features': lime_explanation.as_list()
            }
            
        except Exception as e:
            print(f"LIME explanation failed: {e}")
            explanations['lime'] = None
        
        # 3. Feature Deviation Analysis
        print("Analyzing feature deviations...")
        explanations['deviation_analysis'] = self._analyze_feature_deviations(
            sample_np[0], top_k_features
        )
        
        # 4. Mutation Pattern Analysis
        print("Analyzing potential mutation patterns...")
        explanations['mutation_analysis'] = self._analyze_mutation_patterns(
            sample_np[0], sample_id
        )
        
        return explanations
    
    def _analyze_feature_deviations(self, sample, top_k_features):
        """
        Analyze how much each feature deviates from normal patterns.
        """
        # This would typically require access to the training statistics
        # For now, we'll provide a framework for deviation analysis
        
        deviations = []
        
        # Calculate z-scores for each feature (assuming we have training statistics)
        for i, (feature_name, feature_value) in enumerate(zip(self.feature_names, sample)):
            # In a real implementation, you'd use actual training statistics
            # For demonstration, we'll use placeholder calculations
            
            deviation_info = {
                'feature': feature_name,
                'value': feature_value,
                'deviation_score': abs(feature_value),  # Placeholder
                'interpretation': self._interpret_genetic_feature(feature_name, feature_value)
            }
            deviations.append(deviation_info)
        
        # Sort by deviation score
        deviations.sort(key=lambda x: x['deviation_score'], reverse=True)
        
        return deviations[:top_k_features]
    
    def _analyze_mutation_patterns(self, sample, sample_id):
        """
        Analyze potential mutation patterns in the anomalous sample.
        """
        mutation_analysis = {
            'sample_id': sample_id,
            'potential_mutations': [],
            'affected_pathways': [],
            'risk_assessment': 'Unknown'
        }
        
        # Identify features that might represent mutations
        for i, (feature_name, feature_value) in enumerate(zip(self.feature_names, sample)):
            
            # Look for features that might indicate mutations
            if any(keyword in feature_name.lower() for keyword in 
                   ['mutation', 'variant', 'snp', 'deletion', 'insertion', 'substitution']):
                
                if feature_value > 0:  # Assuming non-zero indicates presence
                    mutation_analysis['potential_mutations'].append({
                        'feature': feature_name,
                        'value': feature_value,
                        'type': self._classify_mutation_type(feature_name),
                        'significance': self._assess_mutation_significance(feature_name, feature_value)
                    })
            
            # Look for pathway-related features
            if any(keyword in feature_name.lower() for keyword in 
                   ['pathway', 'go_', 'kegg', 'reactome']):
                
                if feature_value > 0:
                    mutation_analysis['affected_pathways'].append({
                        'pathway': feature_name,
                        'activity_level': feature_value
                    })
        
        return mutation_analysis
    
    def _interpret_genetic_feature(self, feature_name, feature_value):
        """
        Provide biological interpretation of genetic features.
        """
        interpretations = []
        
        # Gene expression patterns
        if 'expression' in feature_name.lower():
            if feature_value > 2:
                interpretations.append("High expression level detected")
            elif feature_value < -2:
                interpretations.append("Low expression level detected")
        
        # Pathway analysis
        if 'pathway' in feature_name.lower():
            if feature_value > 0:
                interpretations.append(f"Pathway activity: {feature_value:.3f}")
        
        # GO terms
        if 'go_' in feature_name.lower():
            interpretations.append(f"Gene ontology annotation present")
        
        # Default interpretation
        if not interpretations:
            interpretations.append(f"Feature value: {feature_value:.3f}")
        
        return "; ".join(interpretations)
    
    def _classify_mutation_type(self, feature_name):
        """
        Classify the type of mutation based on feature name.
        """
        feature_lower = feature_name.lower()
        
        if 'snp' in feature_lower:
            return 'Single Nucleotide Polymorphism'
        elif 'deletion' in feature_lower:
            return 'Deletion'
        elif 'insertion' in feature_lower:
            return 'Insertion'
        elif 'substitution' in feature_lower:
            return 'Substitution'
        elif 'copy' in feature_lower:
            return 'Copy Number Variation'
        else:
            return 'Unknown Mutation Type'
    
    def _assess_mutation_significance(self, feature_name, feature_value):
        """
        Assess the clinical significance of a mutation.
        """
        # This is a simplified assessment - in practice, you'd use databases like ClinVar
        
        if feature_value > 0.8:
            return 'High significance'
        elif feature_value > 0.5:
            return 'Moderate significance'
        elif feature_value > 0.2:
            return 'Low significance'
        else:
            return 'Uncertain significance'
    
    def generate_summary_report(self, explanations, sample_id=None):
        """
        Generate a comprehensive summary report for the anomaly explanation.
        """
        report = {
            'sample_id': sample_id,
            'analysis_summary': {},
            'key_findings': [],
            'recommendations': []
        }
        
        # Summarize SHAP findings
        if explanations.get('shap'):
            top_shap_features = explanations['shap']['top_features'][:5]
            report['key_findings'].append({
                'type': 'SHAP Analysis',
                'finding': f"Top contributing features: {', '.join([f['feature'] for f in top_shap_features])}"
            })
        
        # Summarize mutation analysis
        if explanations.get('mutation_analysis'):
            mutations = explanations['mutation_analysis']['potential_mutations']
            if mutations:
                high_sig_mutations = [m for m in mutations if m['significance'] == 'High significance']
                if high_sig_mutations:
                    report['key_findings'].append({
                        'type': 'Mutation Analysis',
                        'finding': f"High significance mutations detected: {len(high_sig_mutations)}"
                    })
        
        # Generate recommendations
        report['recommendations'] = [
            "Validate findings with clinical genetic testing",
            "Consult with genetic counselor for interpretation",
            "Consider functional studies for novel variants",
            "Review family history for inherited patterns"
        ]
        
        return report
    
    def plot_explanations(self, explanations, sample_id=None, save_path=None):
        """
        Create visualizations for the explanations.
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'XAI Analysis for Sample {sample_id if sample_id else "Unknown"}', fontsize=16)
        
        # 1. SHAP feature importance
        if explanations.get('shap'):
            ax1 = axes[0, 0]
            shap_data = explanations['shap']['top_features'][:10]
            features = [item['feature'][:20] for item in shap_data]  # Truncate long names
            values = [item['shap_value'] for item in shap_data]
            
            colors = ['red' if v > 0 else 'blue' for v in values]
            ax1.barh(features, values, color=colors)
            ax1.set_xlabel('SHAP Value')
            ax1.set_title('Top SHAP Feature Contributions')
            ax1.grid(True, alpha=0.3)
        
        # 2. Feature deviation heatmap
        if explanations.get('deviation_analysis'):
            ax2 = axes[0, 1]
            dev_data = explanations['deviation_analysis'][:10]
            feature_names = [item['feature'][:15] for item in dev_data]
            deviation_scores = [item['deviation_score'] for item in dev_data]
            
            # Create a simple heatmap
            heatmap_data = np.array(deviation_scores).reshape(-1, 1)
            im = ax2.imshow(heatmap_data, cmap='Reds', aspect='auto')
            ax2.set_yticks(range(len(feature_names)))
            ax2.set_yticklabels(feature_names)
            ax2.set_title('Feature Deviations')
            ax2.set_xticks([])
        
        # 3. Mutation significance pie chart
        if explanations.get('mutation_analysis'):
            ax3 = axes[1, 0]
            mutations = explanations['mutation_analysis']['potential_mutations']
            if mutations:
                significance_counts = {}
                for mut in mutations:
                    sig = mut['significance']
                    significance_counts[sig] = significance_counts.get(sig, 0) + 1
                
                if significance_counts:
                    ax3.pie(significance_counts.values(), labels=significance_counts.keys(), autopct='%1.1f%%')
                    ax3.set_title('Mutation Significance Distribution')
                else:
                    ax3.text(0.5, 0.5, 'No mutations detected', ha='center', va='center')
                    ax3.set_title('Mutation Analysis')
            else:
                ax3.text(0.5, 0.5, 'No mutations detected', ha='center', va='center')
                ax3.set_title('Mutation Analysis')
        
        # 4. Summary statistics
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        # Create summary text
        summary_text = "Analysis Summary:\n\n"
        
        if explanations.get('shap'):
            top_feature = explanations['shap']['top_features'][0]
            summary_text += f"Top contributing feature:\n{top_feature['feature'][:30]}\n"
            summary_text += f"SHAP value: {top_feature['shap_value']:.3f}\n\n"
        
        if explanations.get('mutation_analysis'):
            num_mutations = len(explanations['mutation_analysis']['potential_mutations'])
            summary_text += f"Potential mutations: {num_mutations}\n"
            
            if num_mutations > 0:
                high_sig = sum(1 for m in explanations['mutation_analysis']['potential_mutations'] 
                             if m['significance'] == 'High significance')
                summary_text += f"High significance: {high_sig}\n"
        
        ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=10, 
                verticalalignment='top', fontfamily='monospace')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Explanation plot saved to {save_path}")
        
        plt.show()
        
        return fig

# Integration function with your existing autoencoder
def create_xai_pipeline(autoencoder_model, train_data, test_data, feature_names, 
                       reconstruction_errors, anomalies, threshold):
    """
    Create and setup the complete XAI pipeline.
    
    Args:
        autoencoder_model: Trained autoencoder model
        train_data: Training data tensor
        test_data: Test data tensor  
        feature_names: List of feature names
        reconstruction_errors: Reconstruction errors from autoencoder
        anomalies: Boolean mask of anomalies
        threshold: Anomaly threshold
    
    Returns:
        Configured XAI model
    """
    print("Creating XAI pipeline...")
    
    # Initialize XAI model
    xai_model = GeneticXAIModel(
        autoencoder_model=autoencoder_model,
        feature_names=feature_names,
        device=train_data.device
    )
    
    # Convert anomaly mask to labels
    anomaly_labels = anomalies.cpu().numpy().astype(int)
    
    # Setup explainers using training data as background
    xai_model.setup_explainers(
        background_data=train_data,
        anomaly_labels=np.zeros(len(train_data))  # Training data assumed normal
    )
    
    print("XAI pipeline created successfully!")
    return xai_model

# Example usage function
def analyze_anomalous_samples(xai_model, test_data, anomaly_mask, feature_names, 
                             max_samples=5, save_plots=True):
    """
    Analyze multiple anomalous samples and generate explanations.
    
    Returns:
        List of explanation dictionaries
    """
    # Get indices of anomalous samples
    anomaly_indices = torch.where(anomaly_mask)[0].cpu().numpy()
    
    print(f"Found {len(anomaly_indices)} anomalous samples")
    print(f"Analyzing top {min(max_samples, len(anomaly_indices))} samples...")
    
    explanations_list = []
    
    for i, idx in enumerate(anomaly_indices[:max_samples]):
        print(f"\n--- Analyzing Sample {idx} ({i+1}/{min(max_samples, len(anomaly_indices))}) ---")
        
        # Get the anomalous sample
        sample = test_data[idx]
        
        # Generate explanation
        explanations = xai_model.explain_anomaly(
            anomalous_sample=sample,
            sample_id=f"Sample_{idx}",
            top_k_features=20
        )
        
        # Generate summary report
        report = xai_model.generate_summary_report(explanations, sample_id=f"Sample_{idx}")
        explanations['summary_report'] = report
        
        # Create visualizations
        if save_plots:
            plot_path = f'results/xai_explanation_sample_{idx}.png'
            xai_model.plot_explanations(explanations, sample_id=f"Sample_{idx}", save_path=plot_path)
        
        explanations_list.append(explanations)
        
        print(f"Analysis complete for Sample {idx}")
    
    return explanations_list