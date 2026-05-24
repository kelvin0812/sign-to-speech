import tensorflow as tf

model = tf.keras.models.load_model('action_model.keras')

converter = tf.lite.TFLiteConverter.from_keras_model(model)

converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS, 
    tf.lite.OpsSet.SELECT_TF_OPS
]

converter._experimental_lower_tensor_list_ops = False


converter.optimizations = [tf.lite.Optimize.DEFAULT]

print("Converting model... This might take a few seconds.")
tflite_model = converter.convert()

with open('action_model.tflite', 'wb') as f:
    f.write(tflite_model)
    
print("✅ Converted to action_model.tflite successfully!")