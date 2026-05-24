import cv2
import numpy as np
import os
import mediapipe as mp
from tensorflow.keras.models import load_model

actions = np.array(['hello', 'yes', 'no', 'help', 'thanks', 'idle', 'iloveyou', 'please', 'sorry', 'stop'])
SEQUENCE_LENGTH = 40

model = load_model('dynamic_sign_model.keras')

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, lh, rh])

def live_testing():
    sequence = []
    predictions = [] 
    current_display_word = "" 
    
    threshold = 0.85 
    
    cap = cv2.VideoCapture(0)
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)
            
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-SEQUENCE_LENGTH:]
            
            if len(sequence) == SEQUENCE_LENGTH:
                res = model.predict(np.expand_dims(sequence, axis=0), verbose=0)[0]
                
                best_guess_index = np.argmax(res)
                predictions.append(best_guess_index)
                
                predictions = predictions[-10:]
                

                if np.unique(predictions[-10:])[0] == best_guess_index: 
                    if res[best_guess_index] > threshold:
                        predicted_action = actions[best_guess_index]
                        
                        if predicted_action == 'idle':
                            current_display_word = "" 
                        else:
                            current_display_word = f"{predicted_action.upper()} ({res[best_guess_index]*100:.0f}%)"
            

            cv2.rectangle(image, (0, 0), (image.shape[1], 40), (25, 25, 25), -1) 
            cv2.putText(image, "GNCIC 2026: SIGN TO SPEECH", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)

            if len(sequence) < SEQUENCE_LENGTH:
                cv2.putText(image, "BUFFERING TENSOR SEQUENCE...", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2, cv2.LINE_AA)
            elif current_display_word != "":
                cv2.rectangle(image, (10, 50), (450, 110), (0, 0, 0), -1)
                cv2.putText(image, current_display_word, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Live Sign Language Translation', image)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
                
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    live_testing()