'''
Goal: Merge and Flatten Z-Stack Images from a folder and outputting a PGP 9.5 image, DAPI image, and PGP 9.5 DAPI 
overlay image.

Input: Path of file containing images to merge and flatten
Output: Folder containing PGP 9.5 image, DAPI image, and PGP 9.5 DAPI overlay images for each input image. If no folder
exists in directory, a folder will be created.

The code for this algorithm runs under the assumption that the image files have the following properties:
CZI image: 
image array shape: (1, 1, 1, 2, 16, 972, 973, 1)
- 16 slices in z-stack
- 2 channels
- 1 color channel

TIF image: 
image array shape: (16, 2, 973, 974)
- 16 slices in z-stack
- 2 channels

'''

import os
import time
import czifile
import numpy as np
import cv2
from skimage import io
import matplotlib.pyplot as plt


def z_stack_czi(czi_array):
    # extract Z-stack data
    z_stack = czi_array[0, 0, 0, 0, :, :, :, 0]
    
    num_channels = czi_array.shape[3] # get the number of channels
    mip_images = []
    
    for channel in range(num_channels):
        # extract the Z-stack data for the current channel
        z_stack = czi_array[0, 0, 0, channel, :, :, :, 0]
        
        # maximum intensity projection along the z-axis
        flattened_image = np.max(z_stack, axis=0)
        
        mip_images.append(flattened_image)

    # merge channels
    merged = cv2.merge([mip_images[0], 
                        np.zeros_like(mip_images[1], dtype=np.uint8),
                        mip_images[1]])
    pgp = mip_images[1]
    dapi = mip_images[0]
    
    return (merged, pgp, dapi)

def z_stack_tif(tif_array):
    # read the CZI file
    mip_images = []
    stack = tif_array

    num_slices, num_channels, height, width = tif_array.shape
    for i in range(num_channels):
        z_stack = stack[:, i, :, :] # extract z-stack data
        flattened_image = np.max(z_stack, axis=0) # maximum intensity projection along the z-axis
       
        mip_images.append(flattened_image)

    # merge channels
    merged = cv2.merge([mip_images[0], 
                        np.zeros_like(mip_images[0], dtype=np.uint8),
                        mip_images[1]])
    
    pgp = mip_images[1]
    dapi = mip_images[0]
    
    return (merged, pgp, dapi)

# read in images from folder and input into array
images = []
input_dir = input("Enter the path of the directory containing images: ")
output_dir = "Innervation Output"

# if output directory does not exist, create one
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

start_time = time.time() # time how long algorithm takes to run

print("Starting flattening and merging...")
for file in os.listdir(input_dir):
    if '.czi' in file:
        czi_array = czifile.imread(os.path.join(input_dir, file)) # read in file
        img = z_stack_czi(czi_array) # execute flatten and merge algorithm

        filename = file.replace(".czi", "")

        if img is not None:
            images.append((filename, img[0], img[1], img[2])) # add to list
            
    if '.tif' in file:
        tif_array = io.imread(os.path.join(input_dir, file)) # read in file
        img = z_stack_tif(tif_array) # execute flatten and merge algorithm
        
        filename = file.replace(".tif", "")

        if img is not None:
            images.append((filename, img[0], img[1], img[2]))

for n in range(0, len(images)):
    for i in range(1, len(img)+1):
        if i == 1: # save overlay image
            cv2.imwrite(os.path.join(output_dir, f'{images[n][0]}_Overlay.png'), images[n][i])
        elif i == 2: # save PGP image
            cv2.imwrite(os.path.join(output_dir, f'{images[n][0]}_PGP.png'), images[n][i])
        elif i == 3: # save DAPI image
            cv2.imwrite(os.path.join(output_dir, f'{images[n][0]}_DAPI.png'), images[n][i])
    
    
print("Flattening and Merging Complete!")
print("--- %s seconds ---" % (time.time() - start_time))
    