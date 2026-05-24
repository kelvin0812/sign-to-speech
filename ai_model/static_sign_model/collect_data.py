import cv2
import mediapipe as mp
import numpy as np
import csv
import os

GESTURE_LABEL = "Hello"  
NUM_FRAMES_TO_RECORD = 200 
DATASET_FILE = "sign_language_dataset.csv"

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1, 
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

def create_csv_headers():
    if not os.path.exists(DATASET_FILE):
        with open(DATASET_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            headers = ['label']
            for i in range(21):
                headers.extend([f'x{i}', f'y{i}', f'z{i}'])
            writer.writerow(headers)

def main():
    create_csv_headers()
    cap = cv2.VideoCapture(0)
    
    print(f"--- Ready to record: {GESTURE_LABEL} ---")
    print("Press 'R' to start recording frames.")
    print("Press 'Q' to quit.")

    is_recording = False
    frames_recorded = 0

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        

        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if is_recording and frames_recorded < NUM_FRAMES_TO_RECORD:
                    row_data = [GESTURE_LABEL]
                    for landmark in hand_landmarks.landmark:
                        row_data.extend([landmark.x, landmark.y, landmark.z])
                    
                    with open(DATASET_FILE, mode='a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(row_data)
                    
                    frames_recorded += 1
                    cv2.putText(image, f"Recording: {frames_recorded}/{NUM_FRAMES_TO_RECORD}", 
                                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if not is_recording:
            cv2.putText(image, f"Target: {GESTURE_LABEL} | Press 'R' to record", 
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        elif frames_recorded >= NUM_FRAMES_TO_RECORD:
            cv2.putText(image, "Done! Change label in code.", 
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Sign Language Data Collection', image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') and not is_recording:
            is_recording = True
            frames_recorded = 0

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()