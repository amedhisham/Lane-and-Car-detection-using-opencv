from ultralytics import YOLO
import cv2 as cv
import numpy as np
import math

def find_cars(car_img):
    
    model = YOLO("yolov8n.pt") 

    results = model(car_img)

    results = model(car_img, classes=[2])
    if len(results[0].boxes) != 0:
        x1, y1, x2, y2 = map(int, results[0].boxes[0].xyxy[0])
        box_coordinates = [x1,y1,x2,y2]
        annotated = results[0].plot()
        cv.imshow("cars", annotated)
        cv.waitKey(0)
        return box_coordinates
    else:
        print("no cars found!")

def find_car_lane(box_coordinates,points):


    bottom_center = [math.ceil((box_coordinates[0] + box_coordinates[2])/2) , box_coordinates[3]]
    bottom_right = [box_coordinates[2] , box_coordinates[3]]
    top_left = [box_coordinates[0] , box_coordinates[1]]


    for i in range(len(points)):
        
        corner1_lane = 1000
        corner2_lane = 1000

        lane = points[i].astype(np.int32)
        inside = cv.pointPolygonTest(lane, bottom_center, False)
        if inside == 1:
            lane_num = i + 1
        
        laneSwitching_1 = cv.pointPolygonTest(lane, bottom_right, False)
        laneSwitching_2 = cv.pointPolygonTest(lane, top_left, False)

        if laneSwitching_1 == 1:
            corner1_lane = i + 1
        if laneSwitching_2 == 1:
            corner2_lane = i + 1

    if (corner1_lane != lane_num and corner1_lane != 1000) or (corner2_lane != lane_num and corner2_lane != 1000):
        laneSwitching = 1
    else:
        laneSwitching = 0


    return lane_num , laneSwitching
