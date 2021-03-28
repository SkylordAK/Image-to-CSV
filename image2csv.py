import pytesseract as pt
import cv2
import os
import numpy as np
import csv
import argparse
import webbrowser as wb
parser = argparse.ArgumentParser()
parser.add_argument("img", help = "path to image")
parser.add_argument("cells", type = int, help = "number of cells in one row")
args = parser.parse_args()

try:
    im_path = args.img
except:
    im_path = "abcd.jpeg"
text = ''
r = []


img = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
icon = cv2.imread(im_path)
(thresh, imgg) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
imgg = 255-imgg
kernel_length = np.array(img).shape[1] // 20
verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
img_temp1 = cv2.erode(imgg, verticle_kernel, iterations=2)
verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=2)
img_temp2 = cv2.erode(imgg, hori_kernel, iterations=2)
horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=2)
alpha = 0.5
beta = 1.0 - alpha
img__bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
img__bin = cv2.erode(~img__bin, kernel, iterations=2)
(thresh, img__bin) = cv2.threshold(img__bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(img__bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

idx = 0
for c in contours[::-1]:
    x, y, w, h = cv2.boundingRect(c)
    area = w*h
    if area > 3000 and area < 100000:
        idx += 1
        temp = img[y:y+h, x:x+w]
        #temp = cv2.resize(temp, (temp.shape[1], temp.shape[0]))
        #temp = temp[20:, 20:]
        te = pt.image_to_string(temp, config='--psm 6')
        if '\n' in te:
            te = te.replace('\n', ' ')
    try:
        r.append(te)
    except:
        r.append(' ')
try:
    tot = args.cells
except:
    tot = 8
with open ("fetched.csv", "w", newline = "") as f:
    wri = csv.writer(f)
    for i in range(0, len(r), tot):
        wri.writerow(r[i:i+tot])
wb.open("fetched.csv")
