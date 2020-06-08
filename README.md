# Basic_Image_Processing_with_Python_Tkinter
### Perform Edge Detection, Hough Transforms, Low and High Pass Filtering on Images with Tkinter Package

### (NOTE: Use main.ipynb and main.py)

### GUI
<img src="git1/1.png" width= "400" height="400">

### Select files from the explorer

<img src="git1/2.png" width= "800" height="400">

###  Detect edges using a 3x3 horizontal and vertical kernel

<img src="git1/3.png" width= "800" height="400">

###  Detect and label round objects in an image 
#### The object size might vary for  images so you should tweak in the appropriate values in the variable **circles** (as shown below).
```javascript
circles	= cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10,param1=50,param2=12,minRadius=0,maxRadius=20)
```
<img src="git1/4.png" width= "800" height="400">

###  High pass Fourier filtering 
#### Filters out low and filter in high spatial frequencies.

<img src="git1/5.png" width= "800" height="600">

###  Low pass Fourier filtering 
#### Filters out high and filter in low spatial frequencies.

<img src="git1/6.png" width= "800" height="600">
