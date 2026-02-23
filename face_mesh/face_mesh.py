import cv2
import mediapipe as mp
import numpy as np

source = 0

cap = cv2.VideoCapture(source)

mp_draw = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=2)
draw_spec1 = mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
draw_spec2 = mp_draw.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        scale_val = 2
        x1 = int(frame.shape[1] * scale_val)
        y1 = int(frame.shape[0] * scale_val)
        frame = cv2.resize(frame, (x1, y1))

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = face_mesh.process(img_rgb)

        if detections.multi_face_landmarks:
            for face_landmarks in detections.multi_face_landmarks:
                mp_draw.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS, draw_spec1, draw_spec2)

        cv2.imshow('Face Mesh', frame)

        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()  