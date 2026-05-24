import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.losses import CategoricalCrossentropy 
from tensorflow.keras import regularizers

actions = np.array(['hello', 'yes', 'no', 'help', 'thanks', 'idle', 'iloveyou', 'please', 'sorry', 'stop'])
DATA_PATH = 'extracted_landmarks'
SEQUENCE_LENGTH = 40

def add_noise(data, noise_factor=0.005):
    """Injects tiny mathematical tremors into the skeleton to prevent memorization."""
    noise = np.random.normal(loc=0.0, scale=noise_factor, size=data.shape)
    return data + noise

def train_model():
    sequences, labels = [], []
    label_map = {label:num for num, label in enumerate(actions)}
    
    for action in actions:
        action_path = os.path.join(DATA_PATH, action)
        if not os.path.exists(action_path):
            print(f"Warning: {action_path} missing. Skipping.")
            continue
            
        for file in os.listdir(action_path):
            if file.endswith('.npy'):
                res = np.load(os.path.join(action_path, file))
                if res.shape == (SEQUENCE_LENGTH, 258):
                    sequences.append(res)
                    labels.append(label_map[action])

    X = np.array(sequences)
    y = to_categorical(labels).astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    
    X_train_noisy = add_noise(X_train)
    X_train_augmented = np.concatenate((X_train, X_train_noisy))
    y_train_augmented = np.concatenate((y_train, y_train))
    print(f"Data Augmented! Training samples increased from {len(X_train)} to {len(X_train_augmented)}")
    
    model = Sequential()
    
    model.add(LSTM(64, return_sequences=True, activation='relu', 
                   kernel_regularizer=regularizers.l2(0.001), 
                   input_shape=(SEQUENCE_LENGTH, 258)))
    model.add(Dropout(0.5)) 
    
    model.add(LSTM(64, return_sequences=True, activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(LSTM(32, return_sequences=False, activation='relu'))
    model.add(BatchNormalization())
    
    model.add(Dense(32, activation='relu'))
    model.add(Dense(actions.shape[0], activation='softmax'))
    
    model.compile(optimizer='Adam', 
                  loss=CategoricalCrossentropy(label_smoothing=0.1), 
                  metrics=['categorical_accuracy'])
    
    early_stop = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=0.00001, verbose=1)
    
    print("\n--- Starting Strict Neural Network Training ---")
    model.fit(X_train_augmented, y_train_augmented, 
              epochs=150, 
              validation_data=(X_test, y_test),
              callbacks=[early_stop, reduce_lr])
    
    print("\n--- Generating Classification Report ---")
    predictions = np.argmax(model.predict(X_test), axis=1)
    true_labels = np.argmax(y_test, axis=1)
    print(classification_report(true_labels, predictions, target_names=actions))
    
    model.save('dynamic_sign_model.keras')
    print("\n✅ Training complete! Highly regulated model saved as 'dynamic_sign_model.keras'.")

if __name__ == '__main__':
    train_model()