import mediapipe as mp
import numpy as np
import cv2

class FaceDetector:
    def __init__(self, min_detection_confidence=0.5):
        self.minDectCon = min_detection_confidence
        self.draw_mp = mp.solutions.drawing_utils
        self.face_detection = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=self.minDectCon)

    def findFaces(self, img, draw=True):
        img.flags.writeable = False
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.detection_results = self.face_detection.process(image)

        detections = []

        img.flags.writeable = True

        if self.detection_results.detections:
            for id, detection in enumerate(self.detection_results.detections):
                bboxC = detection.location_data.relative_bounding_box
                h, w, c = img.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                
                detections.append([id, bbox, detection.score])

                if draw:
                    image = self.drawShapes(img, bbox)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 2)

        return img, detections
    
    def drawShapes(self, img, bbox):
        x, y, w, h = bbox
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        
        return img
    

def main():
    video_path = 0
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return
    
    detector = FaceDetector()
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            frame, bbx = detector.findFaces(frame)
            cv2.imshow('Face Detection', frame)
            #if cv2.waitKey(1) == ord('q'):
                #break
        else:
            print("No frame captured, exiting...")
            break

if __name__ == "__main__":
    main()


    