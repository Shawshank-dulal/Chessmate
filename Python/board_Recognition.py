import math
import cv2
import numpy as np
import imutils
from Line import Line
from Square import Square
from Board import Board
from Camera import Camera
import time

debug =  True
calibration=False

class board_Recognition:
	'''
	works with camera class to identify board, squares and so on.
	'''

	def __init__(self, camera):

		self.cam = camera

	# def click_event(self,event,x,y,flags,params):
	# 	if event == cv2.EVENT_LBUTTONDOWN:
	# 		cv2.circle(image,(x,y),5,(0,0,255),-1)
	# 		print(x,' ',y) 
	# 		return x,y
	# 	cv2.imshow("image",image)

	def initialize_Board(self):

		corners = []

		# retake picture until board is initialized properly
		while len(corners) < 81:

			image = self.cam.takePicture()

			if calibration:#for helping in calibration step
				cv2.namedWindow("image")
				cv2.setMouseCallback("image",self.click_event)

				cv2.waitKey(0)
				cv2.destroyAllWindows()
			adaptiveThresh,img = self.clean_Image(image)

			mask = self.initialize_mask(adaptiveThresh,img)
			# if debug:
			# 	cv2.imshow("Masked",mask)
			# 	cv2.waitKey(0)
			# 	cv2.destroyAllWindows()
			# Find edges
			edges,colorEdges = self.findEdges(mask)

			# Find lines
			horizontal, vertical = self.findLines(edges,colorEdges)

			# Find corners
			corners = self.findCorners(horizontal, vertical, colorEdges)

		# Find squares
		squares = self.findSquares(corners, img)

		# create Board
		board = Board(squares)

		return board

	def clean_Image(self,image):
		'''
		clean and resize image
		'''
		# resize image
		img = imutils.resize(image, width=400, height = 400)
		
		# Convert to grayscale
		gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

		# Setting all pixels above the threshold value to white and those below to black
		# Adaptive thresholding is used to combat differences of illumination in the picture
		# adaptiveThresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 10)
		adaptiveThresh=cv2.adaptiveThreshold(cv2.GaussianBlur(gray,(7,7),0),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,10)
		if debug:
			# Show thresholded image
			cv2.imshow("Adaptive Thresholding", adaptiveThresh)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		return adaptiveThresh,img

	def initialize_mask(self, adaptiveThresh,img):
		'''
		border detection
		'''

		# Find contours (closed polygons)
		contours, hierarchy = cv2.findContours(adaptiveThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE	)

		# Create copy of original image
		imgContours = img.copy()

		for c in range(len(contours)):
			area = cv2.contourArea(contours[c])
			perimeter = cv2.arcLength(contours[c], True)
			if c ==0:
				Lratio = 0
			if perimeter > 0:
				ratio = area / perimeter
				if ratio > Lratio:
					largest=contours[c]
					Lratio = ratio
					Lperimeter=perimeter
					Larea = area
			else:
					pass

		# Draw
		cv2.drawContours(imgContours, [largest], -1, (0,0,0), 1)
		if debug:
			# Show image with contours
			cv2.imshow("Chess Boarder",imgContours)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		epsilon = 0.1 * Lperimeter
		chessboardEdge = cv2.approxPolyDP(largest, epsilon, True)

		mask = np.zeros((img.shape[0], img.shape[1]), 'uint8')*125
		cv2.fillConvexPoly(mask, chessboardEdge, 255, 1)
		extracted = np.zeros_like(img)
		extracted[mask == 255] = img[mask == 255]
		extracted[np.where((extracted == [125, 125, 125]).all(axis=2))] = [0, 0, 20]

		if debug:
			# Show image
			cv2.imshow("mask",extracted)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		return extracted

	def findEdges(self, image):
		'''
		Edge detection
		'''
	
		# Find edges
		edges = cv2.Canny(image, 100, 200, None, 3)
		if debug:
			cv2.imshow("Canny", edges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		colorEdges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

		return edges,colorEdges

	def findLines (self, edges, colorEdges):
		'''
		Line detection and finding if those lines are vertical or horizontal
		'''
		
		# Infer lines based on edges
		lines = cv2.HoughLinesP(edges, 1,  np.pi / 180, 100,np.array([]), 100, 80)

		# Draw lines
		a,b,c = lines.shape
		for i in range(a):
			cv2.line(colorEdges, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0,255,0),2,cv2.LINE_AA)

		if  debug:
			# Show image with lines
			cv2.imshow("Lines",colorEdges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		# Sort the lines by orientation
		horizontal = []
		vertical = []
		for l in range(a):
			[[x1,y1,x2,y2]] = lines[l]
			newLine = Line(x1,x2,y1,y2)
			if newLine.orientation == 'horizontal':
				horizontal.append(newLine)
			else:
				vertical.append(newLine)

		return horizontal, vertical

	def findCorners (self, horizontal, vertical, colorEdges):
		'''
		Detect corners
		'''

		corners = []
		for v in vertical:
			for h in horizontal:
				s1,s2 = v.find_intersection(h)
				corners.append([s1,s2])

		# remove duplicate corners
		dedupeCorners = []
		for c in corners:
			matchingFlag = False
			for d in dedupeCorners:
				if math.sqrt((d[0]-c[0])*(d[0]-c[0]) + (d[1]-c[1])*(d[1]-c[1])) < 20:
					matchingFlag = True
					break
			if not matchingFlag:
				dedupeCorners.append(c)

		for d in dedupeCorners:
			cv2.circle(colorEdges, (d[0],d[1]), 10, (0,0,255))


		if debug:
			cv2.imshow("Corners",colorEdges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		return dedupeCorners

	def findSquares(self, corners, colorEdges):
		'''
		Finds the squares of the chessboard 
		'''

		# sort corners by row
		corners.sort(key=lambda x: x[0])
		rows = [[],[],[],[],[],[],[],[],[]]
		r = 0
		for c in range(0, 81):
			if c > 0 and c % 9 == 0:
				r = r + 1

			rows[r].append(corners[c])

		letters = ['a','b','c','d','e','f','g','h']
		numbers = ['1','2','3','4','5','6','7','8']
		Squares = []
		
		for r in rows:
			r.sort(key=lambda y: y[1])
		
		for r in range(0,8):
			for c in range (0,8):
				c1 = rows[r][c]
				c2 = rows[r][c + 1]
				c3 = rows[r + 1][c]
				c4 = rows[r + 1][c + 1]

				position = letters[r] + numbers[7-c]
				newSquare = Square(colorEdges,c1,c2,c3,c4,position)
				newSquare.draw(colorEdges,(0,0,255),2)
				newSquare.drawROI(colorEdges,(255,0,0),2)
				newSquare.classify(colorEdges)
				Squares.append(newSquare)



		if debug:
			#Show image with squares
			cv2.imshow("Squares", colorEdges)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		return Squares
app=board_Recognition(Camera);