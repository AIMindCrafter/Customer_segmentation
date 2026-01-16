from fastapi import FastAPI, HTTPException

import pickle
import pandas as pd
import os


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Customer Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Setup Prometheus Monitoring
# Monitoring disabled due to missing dependency

# --- 1. LOAD THE MODELS ON STARTUP ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

print("Loading models...")
try:
    with open(os.path.join(MODEL_DIR, 'segment_model.pkl'), 'rb') as f:
        df_segments = pickle.load(f)

    with open(os.path.join(MODEL_DIR, 'rules_model.pkl'), 'rb') as f:
        df_rules = pickle.load(f)
except FileNotFoundError as e:
    print(f"Error loading models: {e}")
    # Initialize empty dataframes or handle error widely depending on requirements
    # For now, we'll let it fail later or set None, but raising exception is better for startup
    raise e

# Optimize for speed: Set CustomerID as index for fast lookup
df_segments.set_index('CustomerID', inplace=True)
print("✅ Models loaded successfully!")

# --- 2. DEFINE ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Welcome to the Customer Analytics API. Use /customer/{id} or /recommend/{product}"}

@app.get("/customer/{customer_id}")
def get_customer_segment(customer_id: int):
    """
    Input: Customer ID (e.g., 12345)
    Output: Their Segment (e.g., 'Champions')
    """
    try:
        # Look up the ID in our dataframe
        segment = df_segments.loc[customer_id, 'Segment']
        return {"customer_id": customer_id, "segment": segment}
    except KeyError:
        raise HTTPException(status_code=404, detail="Customer ID not found")

@app.get("/recommend/{product_name}")
def get_recommendations(product_name: str):
    """
    Input: Product Name (e.g., 'HERB MARKER THYME')
    Output: Top recommended bundled products
    """
    # Filter rules where the 'antecedent' matches the input product
    # We use string contains to allow partial matches (e.g., "Thyme" finds "HERB MARKER THYME")
    matches = df_rules[df_rules['antecedents'].str.contains(product_name, case=False, na=False)]
    
    if matches.empty:
        return {"message": "No recommendations found for this product."}
    
    # Sort by Lift and take top 3
    top_recs = matches.sort_values('lift', ascending=False).head(3)
    
    recommendations = []
    for _, row in top_recs.iterrows():
        recommendations.append({
            "product": row['consequents'],
            "confidence_score": round(row['lift'], 2)
        })
        
    return {"input_product": product_name, "recommendations": recommendations}