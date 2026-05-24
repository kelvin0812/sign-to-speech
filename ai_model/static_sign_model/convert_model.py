import tensorflow as tf
import numpy as np

print("Converting model to TensorFlow Lite...")

model = tf.keras.models.load_model('static_sign_model.h5')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('static_sign_model.tflite', 'wb') as f:
    f.write(tflite_model)

classes = np.load('classes.npy', allow_pickle=True)
with open('static_sign_model_labels.txt', 'w') as f:
    for label in classes:
        f.write(f"{label}\n")

print("Success! 'static_sign_model.tflite' and 'static_sign_model_labels.txt' are ready for Flutter.")