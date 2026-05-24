import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

df = pd.read_csv("sign_language_dataset.csv")

X = df.iloc[:, 1:].values 
y = df.iloc[:, 0].values   


encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
np.save('classes.npy', encoder.classes_) 

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2)

model = Sequential([
    Dense(128, activation='relu', input_shape=(63,)),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dense(len(encoder.classes_), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

print("Training the AI brain...")
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

model.save('static_sign_model.h5')
print("Success! Your model 'static_sign_model.h5' is ready for your Flutter app.")