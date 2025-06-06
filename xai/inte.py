# Integration script to run XAI analysis with your autoencoder
# Add this to your main script after the autoencoder training

def main_xai_analysis():
    """
    Main function to run the complete XAI analysis pipeline.
    """
    print("=" * 60)
    print("STARTING XAI ANALYSIS PIPELINE")
    print("=" * 60)
    
    # 1. Load and preprocess data (using your existing function)
    print("\n1. Loading and preprocessing data...")
    train_tensor, test_tensor, feature_names, original_columns = load_and_preprocess_data(sample_size=1000)
    
    # 2. Initialize and train autoencoder (using your existing code)
    print("\n2. Initializing autoencoder...")
    input_dim = train_tensor.shape[1]
    model = GeneAutoencoder(input_dim).to(device)
    
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Train the autoencoder
    print("\n3. Training autoencoder...")
    losses = train_autoencoder(model, train_tensor, epochs=20, batch_size=64)
    
    # Load best model
    if os.path.exists('results/best_model.pth'):
        model.load_state_dict(torch.load('results/best_model.pth'))
        print("Loaded best model from training")
    
    # 3. Detect anomalies (using your existing function)
    print("\n4. Detecting anomalies...")
    reconstruction_errors, anomalies, threshold = detect_anomalies(model, test_tensor)
    
    if reconstruction_errors is None:
        print("Error: Could not detect anomalies. Exiting.")
        return
    
    print(f"Detected {torch.sum(anomalies).item()} anomalies out of {len(test_tensor)} samples")
    print(f"Anomaly threshold: {threshold:.4f}")
    
    # 4. Create XAI pipeline
    print("\n5. Creating XAI pipeline...")
    xai_model = create_xai_pipeline(
        autoencoder_model=model,
        train_data=train_tensor,
        test_data=test_tensor,
        feature_names=feature_names,
        reconstruction_errors=reconstruction_errors,
        anomalies=anomalies,
        threshold=threshold
    )
    
    # 5. Analyze anomalous samples
    print("\n6. Analyzing anomalous samples...")
    explanations_list = analyze_anomalous_samples(
        xai_model=xai_model,
        test_data=test_tensor,
        anomaly_mask=anomalies,
        feature_names=feature_names,
        max_samples=3,  # Analyze top 3 anomalous samples
        save_plots=True
    )
    
    # 6. Generate comprehensive report
    print("\n7. Generating comprehensive analysis report...")
    generate_comprehensive_report(explanations_list, reconstruction_errors, anomalies, threshold)
    
    # 7. Plot overall results
    print("\n8. Creating summary visualizations...")
    plot_results(losses, reconstruction_errors, threshold)
    create_xai_summary_plots(explanations_list, reconstruction_errors, anomalies)
    
    print("\n" + "=" * 60)
    print("XAI ANALYSIS PIPELINE COMPLETED")
    print("=" * 60)
    print(f"Results saved in 'results/' directory")
    print(f"- Individual sample analyses: xai_explanation_sample_*.png")
    print(f"- Comprehensive report: xai_comprehensive_report.txt")
    print(f"- Summary plots: xai_summary_analysis.png")

def generate_comprehensive_report(explanations_list, reconstruction_errors, anomalies, threshold):
    """
    Generate a comprehensive text report of the XAI analysis.
    """
    report_path = 'results/xai_comprehensive_report.txt'
    
    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("COMPREHENSIVE XAI ANALYSIS REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated on: {pd.Timestamp.now()}\n\n")
        
        # Overall statistics
        f.write("OVERALL STATISTICS:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total samples analyzed: {len(reconstruction_errors)}\n")
        f.write(f"Anomalies detected: {torch.sum(anomalies).item()}\n")
        f.write(f"Anomaly rate: {(torch.sum(anomalies).item() / len(reconstruction_errors) * 100):.2f}%\n")
        f.write(f"Anomaly threshold: {threshold:.6f}\n")
        f.write(f"Mean reconstruction error: {torch.mean(reconstruction_errors).item():.6f}\n")
        f.write(f"Max reconstruction error: {torch.max(reconstruction_errors).item():.6f}\n\n")
        
        # Individual sample analyses
        f.write("INDIVIDUAL SAMPLE ANALYSES:\n")
        f.write("-" * 40 + "\n")
        
        for i, explanations in enumerate(explanations_list):
            sample_id = explanations.get('mutation_analysis', {}).get('sample_id', f'Sample_{i}')
            f.write(f"\n{sample_id}:\n")
            f.write("." * 20 + "\n")
            
            # SHAP analysis summary
            if explanations.get('shap'):
                f.write("Top SHAP contributors:\n")
                for j, feature_data in enumerate(explanations['shap']['top_features'][:5]):
                    f.write(f"  {j+1}. {feature_data['feature']}: {feature_data['shap_value']:.4f}\n")
                f.write("\n")
            
            # Mutation analysis
            if explanations.get('mutation_analysis'):
                mutations = explanations['mutation_analysis']['potential_mutations']
                f.write(f"Potential mutations detected: {len(mutations)}\n")
                
                if mutations:
                    high_sig_mutations = [m for m in mutations if m['significance'] == 'High significance']
                    f.write(f"High significance mutations: {len(high_sig_mutations)}\n")
                    
                    for mut in high_sig_mutations:
                        f.write(f"  - {mut['feature']}: {mut['type']} ({mut['significance']})\n")
                f.write("\n")
            
            # Summary report
            if explanations.get('summary_report'):
                report = explanations['summary_report']
                f.write("Key findings:\n")
                for finding in report['key_findings']:
                    f.write(f"  - {finding['type']}: {finding['finding']}\n")
                f.write("\n")
        
        # Recommendations
        f.write("OVERALL RECOMMENDATIONS:\n")
        f.write("-" * 40 + "\n")
        recommendations = [
            "1. Validate computational findings with laboratory testing",
            "2. Consider population stratification in genetic analysis",
            "3. Cross-reference findings with clinical databases (ClinVar, OMIM)",
            "4. Implement quality control measures for genetic data",
            "5. Consider functional impact of identified variants",
            "6. Evaluate inheritance patterns where applicable"
        ]
        
        for rec in recommendations:
            f.write(f"{rec}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")
    
    print(f"Comprehensive report saved to: {report_path}")

def create_xai_summary_plots(explanations_list, reconstruction_errors, anomalies):
    """
    Create summary plots for the XAI analysis.
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('XAI Analysis Summary', fontsize=16)
    
    # 1. Reconstruction error distribution with anomalies highlighted
    ax1 = axes[0, 0]
    errors_np = reconstruction_errors.cpu().numpy()
    normal_errors = errors_np[~anomalies.cpu().numpy()]
    anomaly_errors = errors_np[anomalies.cpu().numpy()]
    
    ax1.hist(normal_errors, bins=50, alpha=0.7, label='Normal', color='blue')
    ax1.hist(anomaly_errors, bins=20, alpha=0.7, label='Anomalies', color='red')
    ax1.set_xlabel('Reconstruction Error')
    ax1.set_ylabel('Count')
    ax1.set_title('Error Distribution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Top contributing features across all anomalies
    ax2 = axes[0, 1]
    if explanations_list and explanations_list[0].get('shap'):
        # Aggregate SHAP values across all samples
        feature_importance = {}
        for explanations in explanations_list:
            if explanations.get('shap'):
                for feature_data in explanations['shap']['top_features'][:10]:
                    feature = feature_data['feature']
                    importance = abs(feature_data['shap_value'])
                    if feature in feature_importance:
                        feature_importance[feature] += importance
                    else:
                        feature_importance[feature] = importance

