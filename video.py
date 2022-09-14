#Author: A. N. M. Sajedul Alam
#Title: Extracting faces from cctv-footage using Multi-Task Cascaded Convolutional Neural Networks and OpenCV

#Before importing OpenCV and MTCNN, you need to install OpenCV and MTCNN
#For intalling OpenCV, use "pip install opencv-python"
#For installing MTCNN, use "pip install mtcnn"

import cv2
import mtcnn
import os

face_detector = mtcnn.MTCNN()
vc = cv2.VideoCapture('./video.mp4')
conf_t = 0.99

try:
    if not os.path.exists('Extracted Faces'):
        os.makedirs('Extracted Faces')
except OSError:
    print("Error: Creating directory of ", 'Extracted Faces')
    
current_frame = 0
while vc.isOpened():
    ret, frame = vc.read()

    if not ret:
        break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detector.detect_faces(frame_rgb)

    for res in results:
        x1, y1, width, height = res['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        
        confidence = res['confidence']
        if confidence < conf_t:
            continue
        key_points = res['keypoints'].values()
        orig_frame = frame.copy()
        
        cut_face = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=1)
        ore_face = orig_frame[y1:y2, x1:x2]
        

        folderName = 'Extracted Faces'
        if ret:
            name = folderName+'/face-'+ str(current_frame)+ '.jpg'
            print('Generating - '+ name)

            cv2.imwrite(name, ore_face)
            current_frame += 1
        else:
            break


    cv2.imshow('Processing', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break