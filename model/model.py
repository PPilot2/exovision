import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def model(toi_filtered: pd.DataFrame, td_filtered: pd.DataFrame):

    # Features to use
    features = [
        'pl_orbper',      # Orbital period
        'pl_rade',        # Planet radius
        'st_teff',        # Stellar temperature
        'pl_trandep',     # Transit depth
        'pl_trandur',     # Transit duration
        'st_rad',         # Stellar radius
        'st_logg'         # Stellar surface gravity
    ]

    # Prepare positive class (confirmed Kepler planets)
    X_positive = td_filtered[features].values
    y_positive = np.ones(len(X_positive))

    # Synthetic negative class (random noise)
    np.random.seed(42)
    X_negative = X_positive * np.random.uniform(0.5, 1.5, size=X_positive.shape)
    y_negative = np.zeros(len(X_negative))

    # Combine into a single dataset
    X = np.vstack([X_positive, X_negative])
    y = np.hstack([y_positive, y_negative])

    # Split into train/validation sets for accuracy measurement
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)

    # Train Random Forest
    rf_model = RandomForestClassifier(
        n_estimators=1000,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_scaled, y_train)

    # Compute validation accuracy
    y_val_pred = rf_model.predict(X_val_scaled)
    val_accuracy = accuracy_score(y_val, y_val_pred)

    # Predict probabilities for TESS data
    X_test = toi_filtered[features].values
    X_test_scaled = scaler.transform(X_test)
    tess_probs = rf_model.predict_proba(X_test_scaled)[:, 1]

    # Add probabilities to the TESS dataframe
    toi_filtered['rf_probability'] = tess_probs

    return toi_filtered, val_accuracy
