# import the necessary packages
from cv2 import ROTATE_90_CLOCKWISE
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import imutils
import numpy as np

class Camera:

	def __init__(self):
		self.cam = PiCamera()
		self.cam.resolution=(1920,1088)
		# self.cam.rotation = 90
		# self.cam.start_preview()
		# time.sleep(20)

	# def imageResize(self,orgImage, resizeFact):
	# 	return cv2.resize(orgImage, (int(orgImage.shape[1]*resizeFact),int(orgImage.shape[0]*resizeFact)), cv2.INTER_AREA)
	# def click_event(self,event,x,y,flags,params):
	# 	print(x,' ',y) 
	def takePicture(self):
		# _,img=cv2.VideoCapture(0)
		# cv2.imshow("Img",img)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
		# self.cam.capture("image.jpg",format="bgr")
		# # initialize the camera and grab a reference to the raw camera capture
		rawCapture = PiRGBArray(self.cam)

		# # allow the camera to warmup
		# time.sleep(1)

		# grab an image from the camera
		self.cam.capture(rawCapture, format="bgr")
		rawCapture.truncate(0)
		# self.cam.close()
		image = rawCapture.array	
		cv2.imwrite("Image.jpg",image)
		# image=cv2.imread("image.jpg")
		# cv2.imshow("Image",image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
		pts = np.float32([[440, 10], [1420, 80], [190, 1080], [1670, 1079]]) # coordinates for warp perspective
		pts2=np.float32([[0,0],[400,0],[0,400],[400,400]])
		transform=cv2.getPerspectiveTransform(pts,pts2)
		res=cv2.warpPerspective(image,transform,(400,400))
		res=cv2.rotate(res,rotateCode=ROTATE_90_CLOCKWISE)
		cv2.imwrite("warped.jpg",res)
		# cv2.imshow("warped",res)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
		return res
