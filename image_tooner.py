#step 1
#Use bilateral filter for edge-aware smoothing.
import cv2

num_down = 2 # number of downsampling steps
num_bilateral = 7 # number of bilateral filtering steps

img_rgb = cv2.imread("girl.jpg")

#convert the image into a square image of 800x800
width1 = 720
height1 = 720
dim1 = (width1,height1)
img_rgb = cv2.resize(img_rgb,dim1,interpolation = cv2.INTER_AREA)


# downsample image using Gaussian pyramid
img_color = img_rgb
for _ in range(num_down):
   img_color = cv2.pyrDown(img_color)

# repeatedly apply small bilateral filter instead of
# applying one large filter
for _ in range(num_bilateral):
   img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=9, sigmaSpace=7)

# upsample image to original size
for _ in range(num_down):
   img_color = cv2.pyrUp(img_color)

#STEP 2 & 3
#Use median filter to reduce noise
# convert to grayscale and apply median blur
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
img_blur = cv2.medianBlur(img_gray, 7)

#STEP 4
#Use adaptive thresholding to create an edge mask
# detect and enhance edges
img_edge = cv2.adaptiveThreshold(img_blur, 255,
   cv2.ADAPTIVE_THRESH_MEAN_C,
   cv2.THRESH_BINARY,
   blockSize=9,
   C=2)

# Step 5
# Combine color image with edge mask & display picture

img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)


#Step 6
#determine size of both images
#resize edge image to the size of color image

col = img_color.shape
print('size of color', col)
edge = img_edge.shape
print('size of edge',edge)
if img_color.shape[0] == img_edge.shape[0] and img_color.shape[1] == img_edge.shape[1]:
   img_edge_resized = img_edge
else:
   width = img_color.shape[1]
   height = img_color.shape[0]
   dim =(width,height)
   img_edge_resized = cv2.resize(img_edge,dim,interpolation = cv2.INTER_AREA)

#Step 7
# convert back to color, bit-AND with color image
img_cartoon = cv2.bitwise_and(img_color,img_edge_resized)

#display
cv2.imshow("ThE_cartoon", img_cartoon)
