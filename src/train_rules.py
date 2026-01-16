import pandas as pd
import pickle
import os
from mlxtend.frequent_patterns import fpgrowth, association_rules

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'Online Retail.xlsx')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'rules_model.pkl')

def train_rules_model():
    print(f"Loading data from {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}")
        return

    # Use openpyxl engine
    df_trans = pd.read_excel(DATA_PATH, engine='openpyxl')
    
    # Ensure InvoiceNo is treated as string for the contains check
    df_trans['InvoiceNo'] = df_trans['InvoiceNo'].astype(str)

    print("Preparing basket...")
    # Filter out cancellations
    df_clean = df_trans[~df_trans['InvoiceNo'].str.contains('C', na=False, case=False)]
    
    # Create the basket
    print("Grouping data (this may take a moment)...")
    basket = (df_clean.groupby(['InvoiceNo', 'Description'])['Quantity']
              .sum().unstack().reset_index().fillna(0)
              .set_index('InvoiceNo'))

    # Convert to boolean
    basket_sets = (basket > 0).astype(bool)

    if 'POSTAGE' in basket_sets.columns:
        basket_sets.drop('POSTAGE', inplace=True, axis=1)

    print(f"Basket Shape: {basket_sets.shape}")
    
    # MLflow Tracking
    import mlflow
    mlflow.set_experiment("Market Basket Analysis")

    with mlflow.start_run():
        # Parameters
        min_support = 0.01
        metric = "lift"
        min_threshold = 1.0
        
        mlflow.log_param("min_support", min_support)
        mlflow.log_param("metric", metric)
        mlflow.log_param("min_threshold", min_threshold)

        print("Running FP-Growth...")
        frequent_itemsets = fpgrowth(basket_sets, min_support=min_support, use_colnames=True)

        if frequent_itemsets.empty:
            print("Warning: No patterns found at 1%.")
            mlflow.log_metric("num_rules", 0)
            return

        print("Generating rules...")
        rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
        
        num_rules = len(rules)
        print(f"Found {num_rules} rules.")
        mlflow.log_metric("num_rules", num_rules)

        # Prepare for deployment (simplify frozen sets to strings)
        deployment_rules = rules.copy()
        deployment_rules['antecedents'] = deployment_rules['antecedents'].apply(lambda x: list(x)[0])
        deployment_rules['consequents'] = deployment_rules['consequents'].apply(lambda x: list(x)[0])
        deployment_rules = deployment_rules[['antecedents', 'consequents', 'lift']]

        print(f"Saving model to {MODEL_PATH}...")
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(deployment_rules, f)
        
        # Log the model artifact
        mlflow.log_artifact(MODEL_PATH)
        
        print("✅ Rules model generated, saved, and logged to MLflow successfully!")

if __name__ == "__main__":
    train_rules_model()
