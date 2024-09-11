import cv2
import matplotlib.pyplot as plt
import pytesseract
import numpy as np
import pandas as pd
import glob
import os
import time

df = pd.DataFrame(columns=['filename', 'time', 'b', 'g', 'r'])
img_folder = '/Volumes/Extreme SSD/sky/103RECNX'
files = glob.glob(os.path.join(img_folder, '*.JPG'))
print(len(files))
for file_path in files:
    image = cv2.imread(file_path)

    dimension = image.shape
    height = dimension[0]
    width = dimension[1]
    margin = 100  # this will ignore the margin inside the boundary of the image
    info_image = image[:32, 28:647]
    # plt.imshow(info_image[:, :, [2, 1, 0]])
    # plt.show()

    # Get the file modification time
    info = os.path.getmtime(file_path)
    m_ti = time.localtime(info)  # Convert to time.struct_time
    info_T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", m_ti)
    print(info_T_stamp)
    # info = pytesseract.image_to_string(
    #     info_image, config="--psm 13 --oem 1 -c tessedit_char_white= 0123456789:-")
    cropped_image = image[margin:height-margin, margin:width-margin]
    dimension = cropped_image.shape

    height = dimension[0]
    width = dimension[1]
    b, g, r = 0, 0, 0
    for y in range(height):
        for x in range(width):
            b += cropped_image[y, x, 0]
            g += cropped_image[y, x, 1]
            r += cropped_image[y, x, 2]
    # if image type is b g r, then b g r value will be displayed.
    # if image is gray then color intensity will be displayed.
    total = height * width
    avg_b, avg_g, avg_r = b/total, g/total, r/total
    data = {
        'filename': os.path.basename(file_path)[:-4],
        'time': info_T_stamp,
        'b': avg_b,
        'g': avg_g,
        'r': avg_r
    }
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    # plt.imshow(cropped_image[:, :, [2, 1, 0]])
    # plt.show()

csv_file_path = 'image_data4.csv'
df.to_csv(csv_file_path, index=False)
print(f'Saved data to CSV: {csv_file_path}')
