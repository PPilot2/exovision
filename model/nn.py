import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_curve, auc
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import BatchNormalization

def nn(toi_filtered, td_filtered):
    # Prepare data (same as before)
    features = ['pl_orbper', 'st_teff', 'pl_trandep', 'pl_rade']

    # Prepare positive class (confirmed Kepler planets)
    X_positive = td_filtered[features].values
    y_positive = np.ones(len(X_positive))

    # Create synthetic negative class
    np.random.seed(42)
    X_negative = X_positive * np.random.uniform(0.5, 1.5, size=X_positive.shape)
    y_negative = np.zeros(len(X_negative))

    # Combine and scale
    X_train = np.vstack([X_positive, X_negative])
    y_train = np.hstack([y_positive, y_negative])
    X_test = toi_filtered[features].values

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Build enhanced neural network with metrics tracking
    model = Sequential([
        Dense(512, input_shape=(4,)),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(alpha=0.1),
        Dropout(0.4),
        
        Dense(256),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(alpha=0.1),
        Dropout(0.3),
        
        Dense(128),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(alpha=0.1),
        Dropout(0.3),
        
        Dense(64),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(alpha=0.1),
        Dropout(0.2),
        
        Dense(32),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(alpha=0.1),
        Dropout(0.2),
        
        Dense(16),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(alpha=0.1),
        Dropout(0.1),
        
        Dense(8),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(alpha=0.1),
        Dropout(0.1),
        
        Dense(1, activation='sigmoid')
    ])

    # Compile with explicit metrics
    model.compile(
        optimizer=Adam(learning_rate=0.0005),
        loss='binary_crossentropy',
        metrics=['accuracy', 'binary_accuracy', 
                tf.keras.metrics.AUC(),
                tf.keras.metrics.Precision(),
                tf.keras.metrics.Recall()]
    )

    # Custom callback for metrics tracking
    class MetricsCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            if epoch % 10 == 0:
                print(f"\nEpoch {epoch} - accuracy: {logs.get('accuracy'):.4f}")

    # Training with enhanced monitoring
    history = model.fit(
        X_train_scaled, y_train,
        epochs=200,
        batch_size=64,
        validation_split=0.2,
        callbacks=[
            EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True),
            MetricsCallback()
        ],
        verbose=1,
    )
    

    
    # Evaluate model on training and validation sets
    train_metrics = model.evaluate(X_train_scaled, y_train, verbose=0)
    val_metrics = model.evaluate(X_train_scaled[int(0.8*len(X_train_scaled)):], 
                               y_train[int(0.8*len(y_train)):], verbose=0)
    
    print(f"\nTrain Accuracy: {train_metrics[1]:.4f}")
    print(f"Validation Accuracy: {val_metrics[1]:.4f}")

    # Get predictions
    train_preds = (model.predict(X_train_scaled) > 0.5).astype(int)
    train_probs = model.predict(X_train_scaled)

    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_train, train_preds))

    # Plot training history
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')

    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ROC curve
    fpr, tpr, _ = roc_curve(y_train, train_probs)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
            label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.show()

    # Get TESS predictions
    tess_probs = model.predict(X_test_scaled)
    toi_filtered['nn_probability'] = tess_probs

    # Show top candidates
    print("\nTop TESS Candidates (Neural Network):")
    print(toi_filtered.sort_values('nn_probability', ascending=False)[['pl_name', 'nn_probability']].head(10))