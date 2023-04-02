import cv2
import numpy as np
import math

debug = True

class Board:
	"""
	keeps track of the squares and updates it
	"""
	def __init__(self, squares):

		self.squares = squares
		self.boardMatrix = []
		self.promotion = 'q'
		self.promo = False
		self.move = "e2e4"

	def draw(self,image):
		"""
draw square
		"""
		for square in self.squares:
			square.draw(image, (0,0,255))
			square.classify(image)

	def assignState(self):
		"""
		Initialize squares
		"""
		black = ['r', 'n', 'b','q','k','b','n','r']
		white = ['R','N','B','Q','K','B','N','R']

		for i in range(8):
			self.squares[8*i + 0].state = black[i]
			self.squares[8*i + 1].state = 'p'
			self.squares[8*i + 2].state = '.'
			self.squares[8*i + 3].state = '.'
			self.squares[8*i + 4].state = '.'
			self.squares[8*i + 5].state = '.'
			self.squares[8*i + 6].state = 'P'
			self.squares[8*i + 7].state = white[i]

		for square in self.squares:
			self.boardMatrix.append(square.state)

	def determineChanges(self,previous, current):
		'''
		Detect changes by difference in color changes from previous and current
		'''

		copy = current.copy()
		
		largestSquare = 0
		secondLargestSquare = 0
		largestDist = 0
		secondLargestDist = 0
		stateChange = []

		for sq in self.squares:
			colorPrevious = sq.roiColor(previous)
			colorCurrent = sq.roiColor(current)

			sum = 0
			for i in range(0,3):
				sum += (colorCurrent[i] - colorPrevious[i])**2

			distance = math.sqrt(sum)

			if distance > 25:
				stateChange.append(sq)
				
			if distance > largestDist:
				secondLargestSquare = largestSquare
				secondLargestDist = largestDist
				largestDist = distance
				largestSquare = sq

			elif distance > secondLargestDist:
				secondLargestDist = distance
				secondLargestSquare = sq


		if  len(stateChange)  == 4:
			
			squareOne = stateChange[0]
			squareTwo = stateChange[1]
			squareThree = stateChange[2]
			squareFour = stateChange[3]

			# check White short side castle
			if squareOne.position == "e1" or squareTwo.position == "e1" or squareThree.position == "e1" or  squareFour.position == "e1":
				if squareOne.position == "f1"  or squareTwo.position == "f1" or squareThree.position == "f1"  or squareFour.position == "f1":
					if squareOne.position == "g1" or squareTwo.position == "g1" or squareThree.position == "g1" or  squareFour.position == "g1":
						if squareOne.position == "h1"  or squareTwo.position == "h1" or squareThree.position == "h1"  or squareFour.position == "h1":
							self.move = "e1g1"
							print(self.move)
							if debug:
								squareOne.draw(copy, (255,0,0), 2)
								squareTwo.draw(copy, (255,0,0), 2)
								squareThree.draw(copy, (255,0,0),2)
								squareFour.draw(copy, (255,0,0), 2)
								cv2.imshow("previous",previous)
								cv2.imshow("identified",copy)
								cv2.waitKey()
								cv2.destroyAllWindows()
							return self.move				
								
				if squareOne.position == "d1"  or squareTwo.position == "d1" or squareThree.position == "d1"  or squareFour.position == "d1":
					if squareOne.position == "c1"  or squareTwo.position == "c1" or squareThree.position == "c1"  or squareFour.position == "c1":
						if squareOne.position == "a1"  or squareTwo.position == "a1" or squareThree.position == "a1"  or squareFour.position == "a1":	
					
							self.move = "e1c1"
							print(self.move)
							if debug:
								squareOne.draw(copy, (255,0,0), 2)
								squareTwo.draw(copy, (255,0,0), 2)
								squareThree.draw(copy, (255,0,0),2)
								squareFour.draw(copy, (255,0,0), 2)
								cv2.imshow("previous",previous)
								cv2.imshow("identified",copy)
								cv2.waitKey()
								cv2.destroyAllWindows()
							return self.move

			if squareOne.position == "e8" or squareTwo.position == "e8" or squareThree.position == "e8" or  squareFour.position == "e8":
				if squareOne.position == "f8"  or squareTwo.position == "f8" or squareThree.position == "f8"  or squareFour.position == "f8":
					if squareOne.position == "g8"  or squareTwo.position == "g8" or squareThree.position == "g8"  or squareFour.position == "g8":
						if squareOne.position == "h8"  or squareTwo.position == "h8" or squareThree.position == "h8"  or squareFour.position == "h8":
							self.move = "e8g8"
							print(self.move)
							if debug:
								squareOne.draw(copy, (255,0,0), 2)
								squareTwo.draw(copy, (255,0,0), 2)
								squareThree.draw(copy, (255,0,0),2)
								squareFour.draw(copy, (255,0,0), 2)
								cv2.imshow("previous",previous)
								cv2.imshow("identified",copy)
								cv2.waitKey()
								cv2.destroyAllWindows()
							return self.move

				
				if squareOne.position == "d8"  or squareTwo.position == "d8" or squareThree.position == "d8"  or squareFour.position == "d8":
					if squareOne.position == "c8"  or squareTwo.position == "c8" or squareThree.position == "c8"  or squareFour.position == "c8":
						if squareOne.position == "a8"  or squareTwo.position == "a8" or squareThree.position == "a8"  or squareFour.position == "a8":
							self.move = "e8c8"
							print(self.move)
							if debug:
								squareOne.draw(copy, (255,0,0), 2)
								squareTwo.draw(copy, (255,0,0), 2)
								squareThree.draw(copy, (255,0,0),2)
								squareFour.draw(copy, (255,0,0), 2)
								cv2.imshow("previous",previous)
								cv2.imshow("identified",copy)
								cv2.waitKey()
								cv2.destroyAllWindows()
							return self.move
				

		squareOne = largestSquare
		squareTwo = secondLargestSquare

		if debug:
			squareOne.draw(copy, (255,0,0), 2)
			squareTwo.draw(copy, (255,0,0), 2)
			cv2.imshow("previous",previous)
			cv2.imshow("identified",copy)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		oneCurr = squareOne.roiColor(current)
		twoCurr = squareTwo.roiColor(current)

		sumCurr1 = 0
		sumCurr2 = 0
		for i in range(0,3):
			sumCurr1 += (oneCurr[i] - squareOne.emptyColor[i])**2
			sumCurr2 += (twoCurr[i] - squareTwo.emptyColor[i])**2

		distCurr1 = math.sqrt(sumCurr1)
		distCurr2 = math.sqrt(sumCurr2)

		if distCurr1 < distCurr2:
			squareTwo.state = squareOne.state
			squareOne.state = '.'
			if squareTwo.state.lower() == 'p':
				if squareOne.position[1:2] == '2' and squareTwo.position[1:2] == '1':
					self.promo = True
				if squareOne.position[1:2] == '7' and squareTwo.position[1:2] == '8':
					self.promo = True

			self.move = squareOne.position + squareTwo.position

		else:
			squareOne.state = squareTwo.state
			squareTwo.state = '.'
			if squareOne.state.lower() == 'p':
				if squareOne.position[1:2] == '1' and squareTwo.position[1:2] == '2':
					self.promo = True
				if squareOne.position[1:2] == '8' and squareTwo.position[1:2] == '7':
					self.promo = True

					
			self.move = squareTwo.position + squareOne.position

		return self.move
