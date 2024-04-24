# Z-Stack-Image-Processing-Algorithm
Python algorithm to flatten and merge .czi and .tif images.

## Purpose
Merge and Flatten Z-Stack Images from a folder and outputting a PGP 9.5 image, DAPI image, and PGP 9.5 DAPI 
overlay image.

## Input
Path of file containing .czi and .tif images to merge and flatten

## Output
Folder containing PGP 9.5 image, DAPI image, and PGP 9.5 DAPI overlay images for each input image. If no folder 
exists in directory, a folder will be created.

## Additional Information
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

Link to Gomez Lab Github: https://github.com/Gomez-Lab
