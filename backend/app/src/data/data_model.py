# Pydantic class object to process a dataset

import logging
from pathlib import Path

import openpyxl
import pandas as pd
from pydantic import BaseModel, ConfigDict

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DataSet(BaseModel):
    file_path: Path = Path()
    dataframe: pd.DataFrame = pd.DataFrame()

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def num_rows(self):
        return len(self.dataframe)

    def model_post_init(self, context):
        try:
            self.file_path = self.file_path.resolve()
        except Exception as e:
            logger.error("Error resolving file path: %s", e)
            raise e

        file_extension = self.file_path.suffix.lower().strip(".")
        if file_extension == "csv":
            self.dataframe = pd.read_csv(self.file_path)
            logging.info(f"Converted Input CSV file {self.file_path} into DataFrame.")
        elif file_extension == "json":
            self.dataframe = pd.read_json(self.file_path)
            logging.info(f"Converted Input JSON file {self.file_path} into DataFrame.")
        elif file_extension in ["xlsx", "xls", "xlsm"]:
            self.dataframe = pd.read_excel(self.file_path, engine=openpyxl)
            logging.info(f"Converted Input Excel file {self.file_path} into DataFrame.")
        else:
            logging.error(
                f"Input File {self.file_path} is not a supported format. Please pass a json, csv or excel file."
            )
            raise ValueError("Improper Input File.")
