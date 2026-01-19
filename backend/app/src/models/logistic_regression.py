from pathlib import Path

import pandas as pd
from pydantic import BaseModel, field_validator
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ..data.data_model import DataSet


class LogisticRegressionModel(BaseModel):
    file_path: Path = Path()
    drop_columns: list[str] = []
    categorical_features: list[str] = []
    numerical_features: list[str] = []
    target_column: str = ""

    @property
    def dataset(self):
        return DataSet(file_path=self.file_path)

    @field_validator(
        "drop_columns", "categorical_features", "numerical_features", mode="before"
    )
    def package_features(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [v]
        elif isinstance(v, list):
            for item in v:
                if not isinstance(item, str):
                    raise ValueError("List must be a list of strings.")
            return v
        else:
            raise ValueError(f"Value is not a string or list of strings: {v}")

    def BuildModel(self) -> tuple[pd.DataFrame, pd.Series, Pipeline]:
        df = self.dataset.dataframe

        y = df[self.target_column]
        X = df.drop(columns=self.drop_columns + [self.target_column])

        # Preprocessor: One Hot Encode Categorical Features
        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "cat",
                    OneHotEncoder(handle_unknown="ignore"),
                    self.categorical_features,
                ),
                ("num", StandardScaler(), self.numerical_features),
            ],
            remainder="passthrough",
        )

        # Build pipeline: preprocess + train logistic regression
        pipeline = Pipeline(
            [
                ("preprocessor", preprocessor),
                ("classifier", LogisticRegression(solver="liblinear")),
            ]
        )

        return X, y, pipeline

    def TrainTestScoreModel(
        self, X: pd.DataFrame, y: pd.Series, pipeline: Pipeline
    ) -> tuple[float, str | dict]:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        classification = classification_report(y_test, y_pred)
        return accuracy, classification

    def ServeModel(self, pipeline: Pipeline, payload: dict[str, int | float | str]):
        for key, value in payload.items():
            if key not in (self.numerical_features + self.categorical_features):
                raise ValueError(f"Key: {key} not in the categorical features")
        payload_df = pd.DataFrame([payload])
        return pipeline.predict(payload_df)
