import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

print("Loading AI Brain...")
model = load_model('static_sign_model.h5')
labels = np.load('classes.npy', allow_pickle=True)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
print("Webcam started. Show your signs! Press 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(img_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            coords = []
            for landmark in hand_landmarks.landmark:
                coords.extend([landmark.x, landmark.y, landmark.z])
            
            X_input = np.array([coords]) 
            predictions = model.predict(X_input, verbose=0)
            
            best_guess_index = np.argmax(predictions)
            confidence = np.max(predictions)
            predicted_letter = labels[best_guess_index]
            
            if confidence > 0.60:
                cv2.putText(frame, f'Sign: {predicted_letter} ({confidence*100:.0f}%)', 
                            (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (25, 25, 25), -1) 
    cv2.putText(frame, "GNCIC 2026: SIGN TO SPEECH", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow('ASL Live Translator', frame)
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()