import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import cv2
from pathlib import Path

bits = 8
K = 2**(bits) - 1 

# reading image location and brightness factor
if len(sys.argv) > 1:
    ImageName = sys.argv[1]
    pImg = Path(ImageName)
    if not pImg.is_file():
        print("\nERROR: Image file not found on path," + 
              "make sure to include full path and extension!\n")
        quit()

    BrightnessFactor = sys.argv[2]
    try:
        BrightnessFactor = float(BrightnessFactor)
    except Exception as err:
        print(err)
        print("\nERROR: Brightness factor is not in valid format!" +
              " Suggestion to keep it within the range (0,5)\n")
        quit()
else:
    print("\nERROR: Image path and Brightness factor not provided via command line.\n")
    quit()

# make sure whether brightness factor is in range
if BrightnessFactor < 0 or BrightnessFactor > 100:
    print("\nERROR: Brightness factor out of range!\n")
    quit()

# reading image
img = cv2.imread(ImageName)
if len(img.shape) <= 2:
    print("\nERROR:Provide Color Images only!\n")
    quit() 

print("\nProcessing image...\n")

greyImgBrightness = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
greyImg = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)

# creating both grayscale as well as brightened grayscale image
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        val = (int(img[i][j][0]) + int(img[i][j][1]) + int(img[i][j][2])) // 3
        greyImg[i][j] = val
        if BrightnessFactor*val > K: greyImgBrightness[i][j] = K
        else: greyImgBrightness[i][j] = BrightnessFactor*val

# displaying the results for comparision
f, axarr = plt.subplots(1, 2, figsize=(10, 5))
axarr[0].imshow(greyImg, cmap='grey')
axarr[0].set_title('Gray Image without Brightness')
axarr[0].axis('off')

axarr[1].imshow(greyImgBrightness, cmap='grey')
axarr[1].set_title(str("Gray Image with Brightness=" + str(BrightnessFactor) + "x"))
axarr[1].axis('off')

plt.tight_layout()
plt.show()

# saving the images in the same folder as original image
root, extension = os.path.splitext(ImageName)
if cv2.imwrite(str(pImg.stem + "_Grayscale"+ extension), greyImg):
    print("Grayscale Image was saved successfully!")
else:
    print("Error saving image.")

if cv2.imwrite(str(pImg.stem + "_Grayscale_Brightness_" + str(BrightnessFactor) +"x" + extension), greyImgBrightness):
    print("Grayscale Image with brightness was saved successfully!")
else:
    print("Error saving image.")
