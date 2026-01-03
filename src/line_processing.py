import numpy as np
import cv2 as cv
from itertools import zip_longest


def rm_lines(img: np.ndarray,lines: np.ndarray) -> np.ndarray:
    
    #remove horizontal lines

    linesList = lines.tolist()
    fake_count = 0
    pops = 0
    pt1 = []
    pt2 = []
    fake_lines = []
    for i in range(len(lines)):
        pt1.append(lines[i][0:2])
        pt2.append(lines[i][2:4])
        pt3 =  np.array([lines[i][2],lines[i][1]])

        hyp = np.linalg.norm(pt2[-1] - pt1[-1])
        opp = np.linalg.norm(pt2[-1] - pt3)
        angle = np.sin(opp/hyp)

        # hls = cv.cvtColor(img, cv.COLOR_BGR2HLS)
        # lower_white = np.array([0, 180, 0])
        # upper_white = np.array([255, 255, 180])
        # white_mask = cv.inRange(hls, lower_white, upper_white)

        # print(white_mask[pt1[1],pt1[0]])
        # breakpoint()
        if angle < 0.3:
            linesList.pop(i-pops)
            pops = pops + 1
            pt1.pop()
            pt2.pop()
    
    lines = np.array(linesList)


    #remove duplicate lines


    for i in range(len(linesList)):
        for j in range(len(linesList)):
            if i == j:
                continue
            else:

                #get all points lying on line j
                empty_image = np.zeros(img.shape[:2])
                empty_image = cv.line(img=empty_image,pt1=lines[j][0:2], pt2=lines[j][2:4], color=255, thickness=1)
                line_coords = np.where(empty_image == 255)
                rows = line_coords[0] 
                cols = line_coords[1] 

                points = list(zip(cols, rows))

                #calculate line lenghts
                line_i_length = np.linalg.norm(lines[i][0:2] - lines[i][2:4])
                line_j_length = np.linalg.norm(lines[j][0:2] - lines[j][2:4])
                max_lineLength = max(line_i_length,line_j_length)
                
                #loop over all points in line to check overlapping lines
                for k in range(len(points)):
                    
                    #if line is very long and intersection happens in the upper part of image
                    if (lines[i][1] < 200 or lines[i][3] < 200 or points[k][1] < 200) and max_lineLength > 350:
                        continue

                    dist_1 = np.linalg.norm(lines[i][0:2] - points[k])
                    dist_2 = np.linalg.norm(lines[i][2:4] - points[k])

                    if min([dist_1,dist_2]) < 15:

                        if fake_count == 0:
                            fake_lines.append([i,j])
                        else:
                            temp_array = np.array(list(zip_longest(*fake_lines, fillvalue=10000))).T
                            target = i
                            result = np.where(temp_array == target)
                            row = result[0]
                            if len(row) == 0:
                                target = j
                                result = np.where(temp_array == target)
                                row = result[0]
                                if len(row) == 0:
                                    fake_lines.append([i,j])
                                else:
                                    fake_lines[row[0]].append(i)
                            else:
                                try:
                                    fake_lines[row[0]].append(j)
                                except:
                                    breakpoint()
                        fake_count = fake_count + 1
                        break
                    # print(fake_count)
    
    lines_toDelete=[]
    for i in range(len(fake_lines)):
        fake_lines[i] = list(set(fake_lines[i]))
        fake_lines[i].sort()
        lines_toDelete.append(fake_lines[i][1:])

    lines_toDelete = sum(lines_toDelete,[])
    lines_toDelete = list(set(lines_toDelete))    
    lines_toDelete.sort()

    pops = 0

    for i in range(len(lines_toDelete)):
        linesList.pop(lines_toDelete[i]-pops)
        pops = pops + 1
    
    lines = np.array(linesList)
    return lines

def check_solid(lines: np.ndarray) -> np.ndarray:


    linesList = lines.tolist()
    pops = 0
    for i in range(len(lines)):
        pt1 = lines[i][0:2]
        pt2 = lines[i][2:4]

        line_length = np.linalg.norm(pt1 - pt2)

        if line_length < 150:
            linesList.pop(i-pops)
            pops = pops + 1  
    
    solid_lines = np.array(linesList)

    return solid_lines