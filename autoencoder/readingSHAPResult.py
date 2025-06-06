# Load SHAP results
shap_results = np.load('results/shap_analysis_results.npy', allow_pickle=True).item()

# Load feature importance
feature_importance = pd.read_csv('results/feature_importance.csv')

# Access SHAP values
shap_values = shap_results['shap_values']
feature_names = shap_results['feature_names']

# Get top important features
top_features = feature_importance.head(10)