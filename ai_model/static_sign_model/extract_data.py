import os
import cv2
import mediapipe as mp
import csv

DATASET_DIR = r"C:\Users\User\Downloads\ASL_Alphabet_Dataset\asl_alphabet_train"
CSV_OUTPUT = "sign_language_dataset.csv"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True, 
    max_num_hands=1,
    min_detection_confidence=0.5
)

def main():
    print(f"Starting data extraction from {DATASET_DIR}...")
    
    if not os.path.exists(DATASET_DIR):
        print(f"Error: The folder '{DATASET_DIR}' does not exist.")
        print("Please check line 9 and make sure your path is correct!")
        return

    with open(CSV_OUTPUT, mode='w', newline='') as f:
        writer = csv.writer(f)
        headers = ['label']
        for i in range(21):
            headers.extend([f'x{i}', f'y{i}', f'z{i}'])
        writer.writerow(headers)

        for label in os.listdir(DATASET_DIR):
            label_dir = os.path.join(DATASET_DIR, label)
            
            if not os.path.isdir(label_dir):
                continue
            
            print(f"Processing images for gesture: [{label}]...")
            images_processed = 0
            
            for image_name in os.listdir(label_dir):
                image_path = os.path.join(label_dir, image_name)
                
                img = cv2.imread(image_path)
                if img is None:
                    continue 
                
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                results = hands.process(img_rgb)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        row_data = [label]
                        for landmark in hand_landmarks.landmark:
                            row_data.extend([landmark.x, landmark.y, landmark.z])
                        
                        writer.writerow(row_data)
                        images_processed += 1
                        
            print(f"  -> Extracted {images_processed} successful hand landmarks for '{label}'.")

    print(f"\nDone! All data has been saved to {CSV_OUTPUT}")
    hands.close()

if __name__ == "__main__":
    main()