import numpy as np
import cv2
import imutils
import sys
import pytesseract
import pandas as pd
import time


pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Read input image
img = cv2.imread(r"number plates\4.png")

# convert input image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# read haarcascade for number plate detection
cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# Detect license number plates
plates = cascade.detectMultiScale(gray, 1.2, 5)
print('Number of detected license plates:', len(plates))

# loop over all plates
for (x, y, w, h) in plates:
    # draw bounding rectangle around the license number plate
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    gray_plates = gray[y:y + h, x:x + w]
    color_plates = img[y:y + h, x:x + w]

    # save number plate detected
    cv2.imwrite('Numberplate.jpg', gray_plates)
    cv2.imshow('Number Plate', gray_plates)
    cv2.imshow('Number Plate Image', img)
    cv2.waitKey(0)


# Configuration for tesseract
config = ('-l eng --oem 1 --psm 3')

# Run tesseract OCR on image
text = pytesseract.image_to_string(img, config=config)

#Data is stored in CSV file
raw_data = {'date': [time.asctime( time.localtime(time.time()) )], 
        'v_number': [text]}

#cv2.destroyAllWindows()

df = pd.DataFrame(raw_data, columns = ['date', 'v_number'])
df.to_csv('data.csv')

# Print recognized text
print(text)

cv2.waitKey(0)
