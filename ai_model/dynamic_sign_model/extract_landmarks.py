import cv2
import numpy as np
import os
import mediapipe as mp

actions = ['hello', 'yes', 'no', 'help', 'thanks', 'idle','iloveyou', 'please', 'sorry', 'stop'] 
VIDEO_PATH = 'custom_sign_data'
SAVE_PATH = 'extracted_landmarks'

mp_holistic = mp.solutions.holistic

def extract_keypoints(results):
    """
    Extracts x, y, z coordinates from MediaPipe results and flattens them.
    Fills with zeros if a hand/body part isn't visible to maintain exact shapes.
    """
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    
    return np.concatenate([pose, lh, rh])

def process_dataset():
    os.makedirs(SAVE_PATH, exist_ok=True)
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        for action in actions:
            action_path = os.path.join(VIDEO_PATH, action)
            save_action_path = os.path.join(SAVE_PATH, action)
            os.makedirs(save_action_path, exist_ok=True)
            
            if not os.path.exists(action_path):
                print(f"Warning: Folder {action_path} not found. Skipping.")
                continue
                
            videos = [f for f in os.listdir(action_path) if f.endswith('.mp4')]
            print(f"\nScanning {len(videos)} videos for sign: '{action}'")
            
            for video_file in videos:
                video_name_without_ext = video_file.split('.')[0]
                save_file_path = os.path.join(save_action_path, f"{video_name_without_ext}.npy")
                
                if os.path.exists(save_file_path):
                    print(f"  ⏩ Skipping {video_file} - already extracted.")
                    continue
                
                video_full_path = os.path.join(action_path, video_file)
                cap = cv2.VideoCapture(video_full_path)
                video_sequence_data = []
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    
                    results = holistic.process(image)
                    
                    keypoints = extract_keypoints(results)
                    video_sequence_data.append(keypoints)
                    
                cap.release()
                
                npy_data = np.array(video_sequence_data)
                np.save(save_file_path, npy_data)
                
                print(f"  -> Extracted & Saved {save_file_path} | Shape: {npy_data.shape}")

    print("\n✅ Landmark extraction complete! Your datasets are ready for training.")

if __name__ == '__main__':
    process_dataset()