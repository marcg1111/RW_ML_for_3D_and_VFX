import cv2
import mediapipe as mp
import numpy as np
import json

source = 'E:\\mirror_google_drive\\rebelway_ML_for_VFX\\rebelway_course_repo\\WT_week05\\face_mesh\\person.mp4'

cap = cv2.VideoCapture(source)

mp_draw = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
#face_mesh = mp_face_mesh.FaceMesh(max_num_faces=2)
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
draw_spec1 = mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
draw_spec2 = mp_draw.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)

landmark_data = []

while cap.isOpened():
    #print('---------------------------------cap is opened---------------------------------')
    ret, frame = cap.read()
    if ret:
        #print('---------------------------------ret == true---------------------------------')    
        scale_val = 1
        x1 = int(frame.shape[1] * scale_val)
        y1 = int(frame.shape[0] * scale_val)
        frame = cv2.resize(frame, (x1, y1))

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_rgb.flags.writeable = False
        detections = face_mesh.process(img_rgb)
        img_rgb.flags.writeable = True

        if detections.multi_face_landmarks:
            #print('---------------------------------multi_face_landmarks detected---------------------------------')
            face_landmark = detections.multi_face_landmarks[0]
            frame_landmarks = []

            for landmark in face_landmark.landmark:
                frame_landmarks.append({
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z
                })

            landmark_data.append(frame_landmarks)

            mp_draw.draw_landmarks(frame, face_landmark, mp_face_mesh.FACEMESH_CONTOURS, draw_spec1, draw_spec2)

        cv2.imshow('Face Mesh', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    else:
        #print('---------------------------------else was triggered---------------------------------')   
        break

cap.release()
cv2.destroyAllWindows() 

output_file = "landmark_data.json"
with open(output_file, 'w') as f:
    json.dump(landmark_data, f, indent=4)

print(f"Landmark data saved to {output_file}")