import cv2
import os
import numpy as np

img = cv2.imread(r"C:\Users\admin\Desktop\puthon\Games\Sword\graphics\property\line.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
x = 0
y = 0
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        x += 1
        if np.linalg.norm(img[i, j]) == np.linalg.norm([246, 246, 246, 255]):
            y += 1
            img[i, j, 1] = 0
cv2.imwrite(r"C:\Users\admin\Desktop\puthon\Games\Sword\graphics\property\line1.jpg", img)
print(x)
print(y)
