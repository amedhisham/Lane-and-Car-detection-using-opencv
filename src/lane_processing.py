import typing as tp
import numpy as np
import cv2 as cv
import math

#


#  Function that given the image and the mask of the lines, fill the area between the lines
def fill_lanes(img: np.ndarray, solid_lines: np.ndarray,dashed_lines: np.ndarray, color: tp.List[int] = [255, 0, 0]) -> np.ndarray:
    start = 0
    solid_idx = 1000
    dashed_idx = 1000
    y = math.floor(img.shape[0]*2.0/3.15) #roi
    full_solid_lines = []
    full_dashed_lines = []

    images_withLanes = []
    points = []
    
    
    full_solid_lines = get_full_lines(img, solid_lines)
    full_dashed_lines =  get_full_lines(img, dashed_lines)

    i = 0
    while i < img.shape[1]:
        if np.all(img[y,i] == [0,0,255]):
            solid_idx = int(np.where(full_solid_lines[:,y,i])[0])
            if dashed_idx != 1000:
                points.append(get_lane_vertices(img,full_solid_lines,full_dashed_lines,solid_idx,dashed_idx))
                images_withLanes.append(cv.fillConvexPoly(np.copy(img), points=points[-1], color=color))
                dashed_idx = 1000
                i = i + 5

        elif np.all(img[y,i] == [0,255,0]):  
            dashed_idx = int(np.where(full_dashed_lines[:,y,i])[0][0])               
            points.append(get_lane_vertices(img,full_solid_lines,full_dashed_lines,solid_idx,dashed_idx))
            images_withLanes.append(cv.fillConvexPoly(np.copy(img), points=points[-1], color=color))
            i = i + 5
        i = i + 1
    



    return images_withLanes , points

def get_full_lines(img, lines):

    full_lines = []

    for i in range(len(lines)):
        empty_image = np.zeros(img.shape[:2])
        full_lines.append(cv.line(img=empty_image,pt1=lines[i][0:2],pt2=lines[i][2:4],color=255,thickness=3))
    
    full_lines = np.stack(full_lines)
    
    return full_lines


def get_lane_vertices(img, full_solid_lines,full_dashed_lines,solid_idx,dashed_idx):
    
    y_line , x_line = np.where(full_dashed_lines[dashed_idx,:,:])
    vertex_1_y = max(y_line)

    y_line , x_line = np.where(full_solid_lines[solid_idx,:,:])
    vertex_2_y = max(y_line)

    vertex_1_x = int(np.where(full_dashed_lines[dashed_idx,vertex_1_y,:])[0][0])
    vertex_2_x = int(np.where(full_solid_lines[solid_idx,vertex_2_y,:])[0][0])

    if vertex_1_x > vertex_2_x:
        bottom_left = np.array([vertex_2_x,vertex_2_y])
        bottom_right = np.array([vertex_1_x,vertex_1_y])
    else:
        bottom_left = np.array([vertex_1_x,vertex_1_y])
        bottom_right = np.array([vertex_2_x,vertex_2_y])    
    
    solid_mask = full_solid_lines[solid_idx,:,:] > 0 
    dashed_mask = full_dashed_lines[dashed_idx,:,:] > 0 
    y_intersect , x_intersect = np.where(solid_mask & dashed_mask)
    top_vertex = np.array([x_intersect[0],y_intersect[0]])
    points = np.array([top_vertex, bottom_left,bottom_right])

    return points