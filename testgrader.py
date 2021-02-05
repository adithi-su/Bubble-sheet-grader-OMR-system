from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True)
args = vars(ap.parse_args())

ANSWER_KEY = {0:1, 1:4, 2:0, 3:3, 4:1}

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(blur, 75, 200)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
docCnt = None

if len(cnts)>0:
    #sorting in descending order
    cnts = sorted(cnts, key=cv2.contourArea, reverse = True)
    for c in cnts:
        p = cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,0.02*p, True)
        # four contours - check
        if len(approx) == 4:
            docCnt=approx
            break

paper = four_point_transform(image, docCnt.reshape(4,2))
warped = four_point_transform(gray, docCnt.reshape(4,2))

# applying Otsu's thresholding method to binarize the warped piece of paper
T = cv2.threshold(warped,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# background => black, foreground=>white
# finding contours in the thresholded image
cnts = cv2.findContours(T.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
questions_contour = []

for c in cnts:
    # computing the binding box
    (x, y, w, h)=cv2.boundingRect(c)
    aspect_ratio = w/float(h)

    if w>=20 and h>=20 and aspect_ratio>=0.9 and aspect_ratio<=1.1:
        questions_contour.append(c)

#sorting the questions from top to bottom
questions_contour = contours.sort_contours(questions_contour, method='top-to-bottom')[0]
correct = 0

# each q has 5 possible answers, looping over qs in batches of 5
for (q,i) in enumerate(np.arange(0, len(questions_contour),5)):
    # sorting contours for current q from L->R
    cnts = contours.sort_contours(questions_contour[i:i+5])[0]
    bubbled = None
    # to determine which bubble is filled, use threshold - T image and count the number of non-zero pixels in each bubble area
    for (j,c) in enumerate(cnts):
        # construct mask that only reveals current bubble
        mask = np.zeros(T.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        #apply mask to T image + count no of non zero pixels in the bubble area
        mask = cv2.bitwise_and(T, T, mask=mask)
        total = cv2.countNonZero(mask)

        if bubbled is None or total>bubbled[0]:
            bubbled=(total, j)

        # initialize contour color and index of current ans
        color = (0,0,255)
        k = ANSWER_KEY[q]

        if k==bubbled[1]:
            color = (0,255,0)
            correct += 1

        #draw the outline of correct ans
        cv2.drawContours(paper, [cnts[k]], -1, color, 3)

score = (correct / 5.0) * 100.0
print("[INFO] score: {:.2f}%".format(score))
#cv2.putText(paper, "{:.2f}%".format(score), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
cv2.waitKey(0)
