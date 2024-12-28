import numpy as np
import pandas as pd
from Levenshtein import distance


class TitanicHelper:
    def __init__(self, parquet_path):
        self.passengers_df = pd.read_parquet(parquet_path)
        self.passenger_names = self.passengers_df["name"].dropna().astype(str).tolist()

    def did_they_survive(self, name):
        # look up the person in the passenger data
        passenger = self.passengers_df[self.passengers_df["name"] == name]

        if len(passenger) == 0:
            return np.nan

        survival = passenger["Survivor (S) or Victim (†)"].values[0]

        return survival == "S"

    def get_closest_match(self, name):
        """Get the passenger with the closest match to a given name"""

        # Calculate distances for all strings
        distances = [(s, distance(name, s)) for s in self.passenger_names]

        # Find the string with minimum distance
        closest_match = min(distances, key=lambda x: x[1])[0]

        return closest_match
