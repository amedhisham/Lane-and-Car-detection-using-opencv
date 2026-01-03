from pathlib import Path
import cv2 as cv

def load_images(folder, extensions=(".png", ".jpg", ".jpeg")):
    images = []
    image_names = []

    for path in sorted(Path(folder).iterdir()):
        if path.suffix.lower() in extensions:
            img = cv.imread(str(path))
            image_names.append(path.stem)
            images.append(img)

    return images , image_names
