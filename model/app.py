import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plot_data import plot_data
from model import model
from flask import Flask, request, render_template, redirect

# app = Flask(__name__)

# @app.route("/", methods=["GET", "POST"])
# def home():
#     return render_template("index.html")
# Load CSV files
toi_df = pd.read_csv('TOI_2024.12.26_14.04.47.csv', comment='#')
td_df = pd.read_csv('TD_2024.12.26_14.02.59.csv', comment='#')

print("Original TESS shape:", toi_df.shape)
print("Original Kepler shape:", td_df.shape)

# Update column mapping
column_mapping = {
    'toi': 'pl_name',
    'pl_trandurh': 'pl_trandur',
    'st_tmag': 'sy_vmag',
    'st_tmagerr1': 'sy_vmagerr1',
    'st_tmagerr2': 'sy_vmagerr2'
}

# Rename columns in TOI dataset
toi_df = toi_df.rename(columns=column_mapping)

# Get common columns
common_cols = list(set(toi_df.columns).intersection(set(td_df.columns)))
print("\nCommon columns after renaming:", common_cols)

# Filter for common columns
toi_filtered = toi_df[common_cols].copy()
td_filtered = td_df[common_cols].copy()

# Define outlier removal function
def remove_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    return data[((data >= Q1 - 1.5 * IQR) & (data <= Q3 + 1.5 * IQR))]

# Clean parameters
# Expanded parameters list
params = [
    'pl_orbper',      # Orbital period
    'pl_rade',        # Planet radius
    'st_teff',        # Stellar temperature
    'pl_trandep',     # Transit depth
    'pl_trandur',     # Transit duration
    'st_rad',         # Stellar radius
    'st_logg'         # Stellar surface gravity
]


# Clean expanded parameters
for param in params:
    if param in toi_filtered.columns and param in td_filtered.columns:
        toi_filtered[param] = remove_outliers(toi_filtered[param])
        td_filtered[param] = remove_outliers(td_filtered[param])

# Remove NaN values for expanded feature set
toi_filtered = toi_filtered.dropna(subset=params)
td_filtered = td_filtered.dropna(subset=params)

print("\nCleaned TESS size with expanded features:", len(toi_filtered))
print("Cleaned Kepler size with expanded features:", len(td_filtered))

# Plot Kepler and TESS Data

# plot_data(toi_filtered, td_filtered)

model(toi_filtered, td_filtered)
   
# if __name__ == "__main__":
#     app.run(debug=True)