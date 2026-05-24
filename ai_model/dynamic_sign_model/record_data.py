import cv2
import os
import time

actions = ['hello', 'yes', 'no', 'help', 'thanks','idle','iloveyou', 'please', 'sorry', 'stop']
samples_per_action = 30
frames_per_sequence = 40  
data_path = 'custom_sign_data'

cap = cv2.VideoCapture(0) 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

for action in actions:
    action_folder = os.path.join(data_path, action)
    os.makedirs(action_folder, exist_ok=True)
    
    existing_videos = [f for f in os.listdir(action_folder) if f.endswith('.mp4')]
    
    if len(existing_videos) >= samples_per_action:
        print(f"⏩ Skipping '{action}' - already has {len(existing_videos)} samples.")
        continue
        
    print(f"\n--- Get ready to record '{action}' ---")
    
    start_time = time.time()
    while time.time() - start_time < 3:
        ret, frame = cap.read()
        cv2.imshow('Data Collection', frame)
        cv2.waitKey(1)
    
    for sample in range(samples_per_action):
        start_time = time.time()
        while time.time() - start_time < 2:
            ret, frame = cap.read()
            time_left = 2 - int(time.time() - start_time)
            cv2.putText(frame, f"Get ready for '{action}' - Sample {sample+1} in {time_left}", 
                        (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow('Data Collection', frame)
            cv2.waitKey(1)
            
        video_path = os.path.join(action_folder, f"{action}_{sample}.mp4")
        out = cv2.VideoWriter(video_path, fourcc, 30.0, (width, height))
        
        for frame_num in range(frames_per_sequence):
            ret, frame = cap.read()
            if not ret: break
            
            out.write(frame)
            
            display_frame = frame.copy()
            cv2.putText(display_frame, f"RECORDING: {action} ({frame_num+1}/{frames_per_sequence})", 
                        (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imshow('Data Collection', display_frame)
            cv2.waitKey(1)
            
        out.release()
        
        pause_time = time.time()
        while time.time() - pause_time < 0.5:
            ret, frame = cap.read()
            cv2.putText(frame, "Reset Hands...", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 165, 0), 2)
            cv2.imshow('Data Collection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break 

cap.release()
cv2.destroyAllWindows()
print("\nData collection complete!")