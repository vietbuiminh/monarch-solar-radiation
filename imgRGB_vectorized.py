import os
import pandas as pd
import numpy as np
import cv2
import glob
import os
import time

img_folder = '/Volumes/Extreme SSD/sky/105RECNX'
files = glob.glob(os.path.join(img_folder, '*.JPG'))
print(len(files))
# Initialize an empty list to store data
data_list = []

# Process each image
for file_path in files:
    image = cv2.imread(file_path)

    dimension = image.shape
    height = dimension[0]
    width = dimension[1]
    margin = 100

    info = os.path.getmtime(file_path)
    m_ti = time.localtime(info)  # Convert to time.struct_time
    info_T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", m_ti)
    print(info_T_stamp)

    cropped_image = image[margin:height-margin, margin:width-margin]

    # Calculate the sum of B, G, R channels
    b_sum = np.sum(cropped_image[:, :, 0])
    g_sum = np.sum(cropped_image[:, :, 1])
    r_sum = np.sum(cropped_image[:, :, 2])

    # Calculate the total number of pixels
    total = cropped_image.shape[0] * cropped_image.shape[1]

    # Calculate the average B, G, R values
    avg_b, avg_g, avg_r = b_sum / total, g_sum / total, r_sum / total

    # Append the data to the list
    data_list.append({
        'filename': os.path.basename(file_path)[:-4],
        'time': info_T_stamp,
        'b': avg_b,
        'g': avg_g,
        'r': avg_r
    })

# Convert the list to a DataFrame
df = pd.DataFrame(data_list)

# Save the DataFrame to a CSV file
csv_file_path = 'image_data6.csv'
df.to_csv(csv_file_path, index=False)
print(f'Saved data to CSV: {csv_file_path}')
