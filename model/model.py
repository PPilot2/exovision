import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.model_selection import train_test_split
import seaborn as sns
from scipy.stats import norm
import matplotlib.pyplot as plt


def model(toi_filtered, td_filtered):
    # Updated features list to match available columns
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

    # Create synthetic negative class by perturbing the positive examples
    np.random.seed(42)
    X_negative = X_positive * np.random.uniform(0.5, 1.5, size=X_positive.shape)
    y_negative = np.zeros(len(X_negative))

    # Combine positive and negative examples
    X_train = np.vstack([X_positive, X_negative])
    y_train = np.hstack([y_positive, y_negative])

    # Prepare TESS testing data
    X_test = toi_filtered[features].values

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    # Train Random Forest model
    rf_model = RandomForestClassifier(
        n_estimators=1000,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )



    # Cross-validation scores
    cv_scores = cross_val_score(rf_model, X_train_scaled, y_train, cv=30)
    print("\nCross-validation scores:", cv_scores)
    print(f"Mean CV score: {cv_scores.mean():.4f}")
    print(f"Standard deviation: {cv_scores.std():.4f}")

    # Fill with proportion confidence interval values:)
    std = np.sqrt((cv_scores.mean() * (1 - cv_scores.mean())) / len(cv_scores))
    error = 1.96*std
    min = cv_scores.mean() - error
    max = cv_scores.mean() + error
    print("Confidence Interval (1 proportion z-interval) at 95 percent confidence: ({} , {})".format(min, max))
    # Train final model
    # Split data into train and validation sets
    X_train_split, X_val, y_train_split, y_val = train_test_split(
        X_train_scaled, y_train, test_size=0.2, random_state=42
    )

    # Train model on training set
    rf_model.fit(X_train_split, y_train_split)

    # Calculate accuracies
    train_accuracy = rf_model.score(X_train_split, y_train_split)
    val_accuracy = rf_model.score(X_val, y_val)

    print(f"\nTraining Accuracy: {train_accuracy:.4f}")
    print(f"Validation Accuracy: {val_accuracy:.4f}")

    # Get predictions
    train_preds = rf_model.predict(X_train_scaled)
    train_probs = rf_model.predict_proba(X_train_scaled)[:, 1]

    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_train, train_preds))

    # Confusion Matrix
    cm = confusion_matrix(y_train, train_preds)

    plt.figure(figsize=(10, 8))
    # Set font size to be 3 times larger
    sns.set(font_scale=1.5)
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='d')
    plt.title('Confusion Matrix')

    plt.xticks([0.5, 1.5], ['Not Planet', 'Planet'], rotation=45, ha='center')

    plt.yticks([0.5, 1.5], ['Not Planet', 'Planet' ], rotation=45, va='center')
    # Bold each x and y label
    # Show xlabel

    plt.xlabel('Predicted Label', fontweight='bold')
    plt.ylabel('True Label', fontweight='bold')

    
    plt.show()
    
    # Create figure with a standard normal distribution
    plt.figure(figsize=(10, 6))
    # Only go from 0.8 to 1
    x = np.linspace(0.8, 1, 1000)
    plt.plot(x, norm.pdf(x, cv_scores.mean(), std), label='Normal Distribution', color='black')

    # Plot normal curve and shade the confidence interval
    # Add the number 90% into the fill between

    plt.fill_between(x, norm.pdf(x, cv_scores.mean(), std), where=(x > min) & (x < max), color='red')

    plt.title('Normal Curve of the Confidence Interval (95% confidence)')
    plt.show()

   # Get TESS predictions (probabilities)
    tess_probs = rf_model.predict_proba(X_test_scaled)[:, 1]  # Get probability of class 1
    toi_filtered['rf_probability'] = tess_probs
    print("\nPrediction statistics:")
    print(f"Shape: {tess_probs.shape}")
    print(f"Min: {tess_probs.min()}, Max: {tess_probs.max()}")
    print(f"Mean: {tess_probs.mean()}, Std: {tess_probs.std()}")
    # Show top candidates
    print("\nTop TESS Candidates (Random Forest):")
    predictions = toi_filtered.sort_values('rf_probability', ascending=False)[['pl_name', 'rf_probability']]
    print(predictions.head(20))
    # Create a histogram of the frequency of probabilities from the predictions of the TESS dataset
    plt.figure(figsize=(10, 6))
    sns.histplot(toi_filtered['rf_probability'], kde=True)
    plt.title('Random Forest Predictions')
    plt.xlabel('Probability')
    plt.ylabel('Frequency')
    plt.show()

