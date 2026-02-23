import cv2
import mediapipe as mp
import numpy as np

mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_style = mp.solutions.drawing_styles

source = 'E:\\mirror_google_drive\\rebelway_ML_for_VFX\\rebelway_course_repo\\WT_week05\\pose_detection\\yoga.mp4'

cap = cv2.VideoCapture(source)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            scale_val = 0.75
            x1 = int(frame.shape[1] * scale_val)
            y1 = int(frame.shape[0] * scale_val)
            frame = cv2.resize(frame, (x1, y1))

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_rgb.flags.writeable = False
            detections = pose.process(img_rgb)
            img_rgb.flags.writeable = True

            if detections.pose_landmarks:
                mp_draw.draw_landmarks(frame, detections.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_style.get_default_pose_landmarks_style())
            else:
                print('No pose landmarks detected')

            cv2.imshow('Pose Detection', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        else:
            print('No frame captured, ending video processing')
            break

    cap.release()
    cv2.destroyAllWindows()