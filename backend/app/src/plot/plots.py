import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pydantic import BaseModel, ConfigDict


class ModelPlots(BaseModel):
    dataframe: pd.DataFrame

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def pair_plot(self, target):
        sns.pairplot(self.dataframe, hue=target)
        plt.show()
