import cv2
from ultralytics import YOLO

import util
from sort.sort import *

from util import get_car,read_license_plate

mot_tracker = Sort()



#load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('./model/license_plate_detector.pt')

vehicles = [2,3,5,7]
cap =  cv2.VideoCapture('./sample.mp4 ')

frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret,frame = cap.read()

    if ret and frame_nmr < 10:

        #detect vehicles
        detections = coco_model(frame)[0]
        detections_ = []

        # print(detections)
        for detection in detections.boxes.data.tolist():
            print(detection)
            x1, y1, x2,y2,score, class_id = detection
            if int(class_id) in vehicles:
                detections_.append([x1,y1,x2,y2,score])


        #track vehicles
        track_ids = mot_tracker.update(np.asarray(detections_))


        #detect license plates
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # assign a car to license plate
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

            #crop license plate
            license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), : ]


            #process license plate
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray,64,255,cv2.THRESH_BINARY_INV)

            cv2.imshow('original_crop',license_plate_crop)
            cv2.imshow('threshold',license_plate_crop_thresh)


            cv2.waitKey(0)






            #read license plate number

            license_plate_text, license_plate_text_score = util.read_license_plate(license_plate_crop_thresh)

            # write results



























#load video




#read frames

#detect vehicles