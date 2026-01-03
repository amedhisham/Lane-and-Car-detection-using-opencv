import typing as tp
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from pathlib import Path

from src.utils import show_img , draw_lines
from src.loader import load_images
from src.line_processing import rm_lines, check_solid
from src.lane_processing import fill_lanes
from src.car_processing import find_cars , find_car_lane


images, image_names = load_images('data/roads/raw') 

for i in range(len(images)): 

    edge_img = cv.Canny(images[i],800,100)
    show_img(edge_img)
    
    lines = cv.HoughLinesP(edge_img, rho = 1,theta = 0.01,threshold = 50,minLineLength=20,maxLineGap=20)


    # hls = cv.cvtColor(images[i], cv.COLOR_BGR2HLS)
    # lower_white = np.array([0, 180, 0])
    # upper_white = np.array([255, 255, 180])
    # white_mask = cv.inRange(hls, lower_white, upper_white)
    # lane_mask = cv.bitwise_and(edge_img, white_mask)

    # lines_2 = cv.HoughLinesP(edge_img, rho = 7,theta = 0.1,threshold = 120,minLineLength=20,maxLineGap=20)
    # if lines is not None:
    #     lines = lines.squeeze(1)
    #     print(lines)
    #     if lines_2 is not None:
    #         lines_2 = lines_2.squeeze(1)
    #         breakpoint()
    #         # lines = np.concatenate((lines, lines_2), axis=0)
    #     image_with_lines, mask = draw_lines(images[i], lines, color=[0, 0, 255], thickness=2)
    # else:
    #         image_with_lines = images[i]

    if lines is not None:
        lines = lines.squeeze(1)
        lines = rm_lines(images[i],lines)
        
            

        solid_lines = check_solid(lines)
        
        lines_set = set(map(tuple, lines))
        solid_set = set(map(tuple, solid_lines))
        dashed_lines = lines_set - solid_set
        dashed_lines = np.array(list(dashed_lines), dtype=int).reshape(-1, 4)


        print(len(lines))
        if len(lines) != 0:
            image_with_lines, mask, solid_lines = draw_lines(images[i], solid_lines, color=[0, 0, 255], thickness=2, solid_flag= 1)
            image_with_lines, mask, dashed_lines = draw_lines(image_with_lines, dashed_lines, color=[0, 255, 0], thickness=2)

        else:
            image_with_lines = images[i]
    else:
            print("No lines found!")
            print("Lighting failure. Attempting to fix by equalizing image histogram")
            gray = cv.cvtColor(images[i], cv.COLOR_BGR2GRAY)
            gray = cv.equalizeHist(gray)
            edge_img = cv.Canny(images[i],800,100)
            lines = cv.HoughLinesP(edge_img, rho = 1,theta = 0.01,threshold = 50,minLineLength=20,maxLineGap=20)
            if lines is not None:
                lines = lines.squeeze(1)
                lines = rm_lines(images[i],lines)
                print("Found lines after equalizing!")
                print(len(lines))
                image_with_lines, mask, solid_lines = draw_lines(images[i], lines, color=[0, 0, 255], thickness=2, solid_flag= 1)
                show_img(image_with_lines, title = "lines")
                continue
            else: 
                print("Lighting failure. No lines found even after equalizing histogram")
                continue

    show_img(image_with_lines, title = "lines")
    images_withLanes, points = fill_lanes(image_with_lines,solid_lines,dashed_lines)
    for j in range(len(images_withLanes)):
        show_img(images_withLanes[j],title = "lanes")
    
    folder_path = Path("data/roads/raw") / f"{image_names[i]}_cars"
    
    if folder_path.is_dir():
        car_imgs, car_imgNames = load_images(folder_path)

        for j in range(len(car_imgs)):
            box_coordinates = find_cars(car_imgs[j])
            print("Car box found at:")
            print(box_coordinates)
            lane_num , laneSwitching = find_car_lane(box_coordinates,points)
            print(f"Car in lane: {lane_num} , Lanes Numbered from left to right")
            if laneSwitching:
                 print("Car is changing lanes")
            else:
                 print("Car not changing lanes")




  