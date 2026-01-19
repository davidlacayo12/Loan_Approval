# Serves the model. User has the option to train it, test it, deploy it, or serve it.
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .src import LogisticRegressionModel

__author__ = "David Lacayo"

BASE_PATH = Path(__file__).parent
MODEL_PATH = BASE_PATH / "src" / "data" / "outputs" / "trained_model.pkl"
DATA_PATH = BASE_PATH / "src" / "data" / "inputs" / "loan_approval.csv"


class Payload(BaseModel):
    city: str = Field(default="")
    income: int | float = Field(default=0.0, ge=0.0)
    credit_score: int = Field(default=300, ge=300, le=850)
    loan_amount: int | float = Field(default=0.0, ge=0.0, lt=1_000_000)
    years_employed: int = Field(default=1, ge=1, lt=50)


class ModelResponse(BaseModel):
    loan_approved: bool = Field(default=False)


# --- Initialize Model Instance and Load or Train Once ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing model...")

    logistic_regression_model = LogisticRegressionModel(
        file_path=DATA_PATH,
        drop_columns=["name", "points"],
        categorical_features=["city"],
        numerical_features=[
            "income",
            "credit_score",
            "loan_amount",
            "years_employed",
        ],
        target_column="loan_approved",
    )

    # Train or load
    if MODEL_PATH.exists():
        print("Loading saved model...")
        model = joblib.load(MODEL_PATH)
    else:
        print("Training model...")
        X, y, pipeline = logistic_regression_model.BuildModel()
        accuracy, classification = logistic_regression_model.TrainTestScoreModel(
            X, y, pipeline
        )
        print(f"Model training complete. Accuracy: {accuracy:.2f}")
        print("Classification Report:\n")
        print(classification)
        joblib.dump(pipeline, MODEL_PATH)
        model = pipeline

    # Store in app state for reuse
    app.state.logistic_regression_model = logistic_regression_model
    app.state.log_reg_pipeline = model

    yield  # FastAPI serves requests after this point

    print("Shutting down app... (cleanup if needed)")


# -------- Execution Begins Here -------- #

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=ModelResponse)
async def predict(payload: Payload):
    log_reg_pipeline = app.state.log_reg_pipeline
    logistic_regression_model = app.state.logistic_regression_model
    result = logistic_regression_model.ServeModel(
        log_reg_pipeline, payload.model_dump()
    )
    return ModelResponse(loan_approved=bool(*result))
