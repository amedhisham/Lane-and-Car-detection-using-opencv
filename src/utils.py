import typing as tp
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# Function to plot images inline in the notebook
def show_img(img, title=None):
    # Check if the image is in BGR format and convert it to RGB
    if len(img.shape) == 3 and img.shape[2] == 3:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # Plot the image
    plt.figure() 
    plt.imshow(img)
    if title:
        plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    plt.close()


# Funtion to add lines to an image
def draw_lines(img: np.ndarray, lines: np.ndarray, color: tp.List[int] = [0, 0, 255], thickness: int = 1, solid_flag: int = 0) -> tp.Tuple[np.ndarray]:
    new_image = np.copy(img)
    empty_image = np.zeros(img.shape[:2])

    if len(lines.shape) == 1:
        lines = lines[None, ...]

    angles = []
    # Draw found lines
    if solid_flag == 0:
        linesToDelete = []
        for i in range(len(lines)):
            pt1 = lines[i][0:2]
            pt2 = lines[i][2:4]
            angles.append(np.arctan2(pt2[1] - pt1[1], pt2[0] - pt1[0]))  

        indices = sorted(range(len(angles)), key=lambda i: angles[i])

        # Apply the same reordering to both lists
        angles = [angles[i] for i in indices]
        lines = [lines[i] for i in indices]       

        for i in range(len(lines)):
            pt1 = lines[i][0:2]
            pt2 = lines[i][2:4]            
            if i == 0:
                direction = pt1- pt2
                pt1 = np.round(pt1 + 10*direction).astype(int)
                pt2 = np.round(pt2 - 10*direction).astype(int)
                lines[i][0:2] = pt1
                lines[i][2:4] = pt2
                empty_image = cv.line(img=empty_image,pt1=pt1, pt2=pt2, color=255, thickness=thickness)
            elif abs(angles[i] - angles[i-1]) > 0.1 :
                direction = pt1- pt2
                pt1 = np.round(pt1 + 10*direction).astype(int)
                pt2 = np.round(pt2 - 10*direction).astype(int)
                lines[i][0:2] = pt1
                lines[i][2:4] = pt2
                empty_image = cv.line(img=empty_image,pt1=pt1, pt2=pt2, color=255, thickness=thickness)
            else:
                linesToDelete.append(i)

        linesList = lines
        pops = 0
        for i in range(len(linesToDelete)):
            linesList.pop(linesToDelete[i]-pops)
            pops = pops + 1
        
        lines = np.array(linesList)

    else:
        for i in range(len(lines)):
            direction = lines[i][0:2] - lines[i][2:4]
            pt1 = np.round(lines[i][0:2] + 10*direction).astype(int)
            pt2 = np.round(lines[i][2:4] - 10*direction).astype(int)
            lines[i][0:2] = pt1
            lines[i][2:4] = pt2
            empty_image = cv.line(img=empty_image,pt1=pt1, pt2=pt2, color=255, thickness=thickness)

    # Keep lower part of each line until intersection
    mask_lines = empty_image != 0
    max_line = 0
    valid = flag = False # check that we found 2 lines at least once before 
    for i, line in enumerate(mask_lines): # iterate each line and search for a batch of contiguous idxs
        indices = np.argwhere(line)
        if len(indices) > 1:
            flag = True
            for ii in range(len(indices)-1):
                flag = flag and indices[ii+1] == indices[ii] + 1
                if not flag:
                    valid = True 
                    break    
                if valid:
                    max_line = i
        elif len(indices) == 1 and valid:
            max_line = i
        if flag and valid:
            break

    mask_boundaries = np.zeros_like(empty_image)
    mask_boundaries[max_line:] = 1
    mask = (mask_lines * mask_boundaries).astype(bool)

    new_image[mask_lines] = np.array(color)
    
    return new_image, mask,lines
