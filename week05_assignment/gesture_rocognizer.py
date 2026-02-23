import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

model_path = 'E:/mirror_google_drive/rebelway_ML_for_VFX/rebelway_course_repo/WT_week05/week05_assignment/gesture_recognizer.task'

base_options = python.BaseOptions(model_asset_path=model_path)

GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

thumbs_up_count = 0
thumbs_down_count = 0
latest_frame = None
last_gesture = None

# Create a gesture recognizer instance with the live stream mode:
def print_result(result, output_image, timestamp_ms):
    global latest_frame
    global thumbs_up_count, thumbs_down_count, last_gesture

    image = output_image.numpy_view().copy()

    detected_gesture = None

    # Convert the image from BGR to RGB as mediapipe requires RGB input.
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Draw landmarks
    if result.hand_landmarks:
        h, w, _ = image_rgb.shape

        for hand_landmarks in result.hand_landmarks:

            for landmark in hand_landmarks:
                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(image_rgb, (x, y), 4, (0, 255, 0), -1)

    if result.gestures:
        top_gesture = result.gestures[0][0]
        detected_gesture = top_gesture.category_name

        # Count only if new gesture is detected
        if detected_gesture != last_gesture:
            if detected_gesture == 'Thumb_Up':
                thumbs_up_count += 1
            elif detected_gesture == 'Thumb_Down':
                thumbs_down_count += 1

            last_gesture = detected_gesture

        # Display counter
        cv2.putText(image_rgb,
                    f"Thumbs Up: {thumbs_up_count}",
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2)
        
        cv2.putText(image_rgb,
                    f"Thumbs Down: {thumbs_down_count}",
                    (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2)

        cv2.putText(image_rgb,
                    f"Gesture: {detected_gesture}",
                    (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 0, 0),
                    2)

    latest_frame = image_rgb


options = GestureRecognizerOptions(
    base_options=base_options,
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

with GestureRecognizer.create_from_options(options) as recognizer:
    # Continuously capture images from the webcam and feed them into the recognizer:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print('Error: Could not open webcam.')
        exit()

    start_time = time.time()

    last_inference_time = 0
    inference_interval = 80

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640*2)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480*2)

    frame_with = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 24, (frame_with, frame_height))

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print('Error: Could not read frame from webcam.')
            break

        out.write(latest_frame if latest_frame is not None else image)

        # Wrap the image in a MediaPipe Image object.
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

        # Send the image to the recognizer and get the result.
        timestamp_ms = int((time.time() - start_time) * 1000)
        if timestamp_ms > last_inference_time + inference_interval:
            try:
                recognizer.recognize_async(mp_image, timestamp_ms)
            except Exception as e:
                print(f"Error during recognition: {e}")

            last_inference_time = timestamp_ms

        if latest_frame is not None:
            cv2.imshow("MediaPipe Gesture Recognizer", latest_frame)
        else:
            cv2.imshow("MediaPipe Gesture Recognizer", image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    out.release()
    cap.release()
    cv2.destroyAllWindows()