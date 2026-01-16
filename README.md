# Customer Segmentation MLOps Project

This project implements a Customer Analytics API using FastAPI, with a focus on MLOps best practices. It includes customer segmentation (KMeans) and product recommendation (Association Rules) capabilities.

## MLOps Features Applied

1. **Project Structure**: Organized into `api/`, `models/`, `data/`, `notebooks/`, and `src/` for better maintainability and separation of concerns.
2. **Reproducibility**: Training logic extracted from notebooks into reusable scripts (`src/train_rules.py`). Dependencies locked in `requirements.txt`.
3. **Containerization**: Fully dockerized application using `Dockerfile` for consistent deployment environments.
4. **Environment Management**: Usage of virtual environments (`venv`) and `.gitignore` to keep the workspace clean.

## Project Structure

```
├── api/
│   └── main.py          # FastAPI application serving the models
├── data/
│   └── Online Retail.xlsx # Raw data (ignored in git)
├── models/
│   ├── segment_model.pkl # Pre-trained segmentation model/lookup
│   └── rules_model.pkl   # Association rules model
├── notebooks/
│   └── ...              # Exploratory data analysis notebooks
├── src/
│   └── train_rules.py   # Script to retrain the association rules model
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Setup & Running

### 1. Local Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Training

To regenerate the association rules model from the raw data:

```bash
python src/train_rules.py
```

### 3. Running the API

Start the FastAPI server:

```bash
uvicorn api.main:app --reload
```

Access the API documentation at `http://127.0.0.1:8000/docs`.

### 4. MLflow Tracking

The training script automatically logs experiments to MLflow. To view the UI:

```bash
mlflow ui
```

Then navigate to `http://127.0.0.1:5000`.

### 5. Prometheus Monitoring

The API exposes Prometheus metrics at `/metrics`. You can scrape this endpoint using a Prometheus server.

After starting the API, view raw metrics at: `http://127.0.0.1:8000/metrics`

### 6. Docker

Build and run the container:

```bash
docker build -t customer-segmentation-api .
docker run -p 8000:8000 customer-segmentation-api
```
# Customer_segmentation
