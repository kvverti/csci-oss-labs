from PIL import Image
import numpy as np

def convertImage(filename):
    with Image.open(filename) as img:
        img2 = img.convert(mode='L').resize((28, 28))
        return 255 - np.array(img2)
