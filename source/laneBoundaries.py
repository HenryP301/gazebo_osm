import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
import os

class LaneBoundaries:

	def __init__(self, xPoints, yPoints):
		self.xPoints = xPoints
		self.yPoints = yPoints
		# self.lanePoints = []

		self.imgInitialized = False
		self.img = 0
		self.roadWidth = 6 #default 6 meters from left to right lane


	# size of image, scalar for pixel/meter, array containing all left and right road lane segments
	def makeImage(self, boundarySize, scalar, roadLanes, centerLanes, laneSegmentWidths, pngName):

		size = [0,0]

		if scalar <= 0:
			print ('| Cannot scale image < 0 size! Setting to (boundarySize * 1). ')
			scalar = 1
		# [0] = x, and [1] = y
		size[0] = boundarySize[0] * scalar
		size[1] = boundarySize[1] * scalar

		lineWidth = 6 * scalar # 6 pixels in 1 meter

		print ('| Scaled Size = [ ' + str(int(size[1])) + ' x ' + str(int(size[0])) + ' ] pixels')

		if self.imgInitialized == False:
			self.img = np.zeros((size[1], size[0], 3) , np.uint8)

			self.imgInitialized = True

		# drawing and inflating the middle lane.
		for idx, midLane in enumerate(centerLanes):

			xOffset = size[0]//2
			yOffset = size[1]//2

			laneWidth = int(math.ceil(laneSegmentWidths[idx] * 6 *scalar))
			print ("| MidLane Width: ", str(laneWidth))

			if len(midLane[0]) > 2:

				# drawing second lane (A)
				for i in range(len(midLane[0])):

					# No downsample occurs for middle lane as it is thicker
					# and wont cause any rigged edges in the pixels of
					# the lines
					if i == 0:
						startPointX = (int(midLane[0][i]* scalar)) + xOffset
						startPointY = (int(midLane[1][i]* scalar)) + yOffset

						endPointX = (int(midLane[0][(i+1)]* scalar)) + xOffset
						endPointY = (int(midLane[1][(i+1)]* scalar)) + yOffset
					elif i == (len(midLane[0])):
						# dont need to draw backwards
						break	
					else:			

						startPointX = (int(midLane[0][i]* scalar)) + xOffset
						startPointY = (int(midLane[1][i]* scalar)) + yOffset

						endPointX = (int(midLane[0][(i-1)]* scalar)) + xOffset
						endPointY = (int(midLane[1][(i-1)]* scalar)) + yOffset

					# adding a line onto the overall entire image
					# line width as 60 is equal to 4 meters
					cv2.line(self.img, (startPointX,startPointY), (endPointX,endPointY), (255,255,255), laneWidth)
			else:
				# If there is only one point, we can draw anything, so disregard it
				#print ('Road has LESS then four points!')
				# print len(midLane[0])

				if len(midLane[0]) == 2:
					# print len(midLane[0])
					startPointX = (int(midLane[0][0]* scalar) ) + xOffset
					startPointY = (int(midLane[1][0]* scalar) ) + yOffset
					endPointX = (int(midLane[0][1]* scalar) ) + xOffset
					endPointY = (int(midLane[1][1]* scalar)) + yOffset

					cv2.line(self.img, (startPointX,startPointY), (endPointX,endPointY), (255,255,255), laneWidth)

				elif len(midLane[0]) <= 4 and len(midLane[0]) > 1:
					startPointX = (int(midLane[0][0]* scalar) ) + xOffset
					startPointY = (int(midLane[1][0]* scalar) ) + yOffset
					endPointX = (int(midLane[0][1]* scalar) ) + xOffset
					endPointY = (int(midLane[1][1]* scalar)) + yOffset
					cv2.line(self.img, (startPointX,startPointY), (endPointX,endPointY), (255,255,255),laneWidth)

					startPointX = (int(road[0][1]* scalar) ) + xOffset
					startPointY = (int(road[1][1]* scalar) ) + yOffset
					endPointX = (int(road[0][2]* scalar) ) + xOffset
					endPointY = (int(road[1][2]* scalar)) + yOffset
					cv2.line(self.img, (startPointX,startPointY), (endPointX,endPointY), (255,255,255),laneWidth)


		# # Drawing the side lanes
		# for index, road in enumerate(roadLanes):

		# 	# Setting the center of the image as the origin 
		# 	# x = width/2
		# 	# y = height/2
		# 	xOffset = size[0]/2
		# 	yOffset = size[1]/2

		# 	# print ('Road # of points: ' + str(len(road[0])))

		# 	if len(road[0]) > 4:
				
		# 		# print ('Road has more then two points')

		# 		# drawing second lane (A)
		# 		# down sampling to draw every two road points, to not cause zig zags from pixel to pixel
		# 		for i in range(len(road[0])/2):

		# 			# i*2 is just downsampling the amount of lines drawn since you
		# 			# would need really high resolution
		# 			if i == 0:
		# 				LstartPointX = (int(road[0][i*2][0]* scalar) ) + xOffset
		# 				LstartPointY = (int(road[0][i*2][1]* scalar) ) + yOffset

		# 				LendPointX = (int(road[0][(i+1)*2][0]* scalar) ) + xOffset
		# 				LendPointY = (int(road[0][(i+1)*2][1]* scalar)) + yOffset
		# 			elif i == (len(road[0])-1):
		# 				# dont need to draw backwards
		# 				break	
		# 			else:				
		# 				LstartPointX = (int(road[0][i*2][0]* scalar)) + xOffset
		# 				LstartPointY = (int(road[0][i*2][1]* scalar)) + yOffset

		# 				LendPointX = (int(road[0][(i-1)*2][0]* scalar)) + xOffset
		# 				LendPointY = (int(road[0][(i-1)*2][1]* scalar)) + yOffset

		# 			cv2.line(self.img, (LstartPointX,LstartPointY), (LendPointX,LendPointY), (255,255,255))


		# 		# drawing second lane (B)	
		# 		for i in range(len(road[1])/2):

		# 			if i == 0:
		# 				RstartPointX = (int(road[1][i*2][0]* scalar)) + xOffset
		# 				RstartPointY = (int(road[1][i*2][1]* scalar)) + yOffset

		# 				RendPointX = (int(road[1][(i+1)*2][0]* scalar)) + xOffset
		# 				RendPointY = (int(road[1][(i+1)*2][1]* scalar)) + yOffset
		# 			elif i == (len(road[1])-1):
		# 				# dont need to draw backwards
		# 				break	
		# 			else:				
		# 				RstartPointX = (int(road[1][i*2][0]* scalar)) + xOffset
		# 				RstartPointY = (int(road[1][i*2][1]* scalar)) + yOffset

		# 				RendPointX = (int(road[1][(i-1)*2][0]* scalar)) + xOffset
		# 				RendPointY = (int(road[1][(i-1)*2][1]* scalar)) + yOffset

		# 			cv2.line(self.img, (RstartPointX,RstartPointY), (RendPointX,RendPointY), (255,255,255))
		# 	else:
		# 		# If there is only one point, we can draw anything, so disregard it
		# 		# print ('Road has LESS then four points!')
		# 		# print len(road[0])
		# 		# print road[0]

		# 		if len(road[0]) == 2:
		# 			for i in range(len(road[0])):
		# 				LstartPointX = (int(road[0][0][0]* scalar) ) + xOffset
		# 				LstartPointY = (int(road[0][0][1]* scalar) ) + yOffset
		# 				LendPointX = (int(road[0][1][0]* scalar) ) + xOffset
		# 				LendPointY = (int(road[0][1][1]* scalar)) + yOffset

		# 				RstartPointX = (int(road[1][0][0]* scalar) ) + xOffset
		# 				RstartPointY = (int(road[1][0][1]* scalar) ) + yOffset
		# 				RendPointX = (int(road[1][1][0]* scalar) ) + xOffset
		# 				RendPointY = (int(road[1][1][1]* scalar)) + yOffset

		# 				cv2.line(self.img, (LstartPointX,LstartPointY), (LendPointX,LendPointY), (255,255,255))
		# 				cv2.line(self.img, (RstartPointX,RstartPointY), (RendPointX,RendPointY), (255,255,255))
		# 		elif len(road[0]) == 3:
		# 				LstartPointX = (int(road[0][0][0]* scalar) ) + xOffset
		# 				LstartPointY = (int(road[0][0][1]* scalar) ) + yOffset
		# 				LendPointX = (int(road[0][1][0]* scalar) ) + xOffset
		# 				LendPointY = (int(road[0][1][1]* scalar)) + yOffset
		# 				cv2.line(self.img, (LstartPointX,LstartPointY), (LendPointX,LendPointY), (255,255,255))

		# 				LstartPointX = (int(road[0][1][0]* scalar) ) + xOffset
		# 				LstartPointY = (int(road[0][1][1]* scalar) ) + yOffset
		# 				LendPointX = (int(road[0][2][0]* scalar) ) + xOffset
		# 				LendPointY = (int(road[0][2][1]* scalar)) + yOffset
		# 				cv2.line(self.img, (LstartPointX,LstartPointY), (LendPointX,LendPointY), (255,255,255))

		# 				RstartPointX = (int(road[1][1][0]* scalar) ) + xOffset
		# 				RstartPointY = (int(road[1][1][1]* scalar) ) + yOffset
		# 				RendPointX = (int(road[1][2][0]* scalar) ) + xOffset
		# 				RendPointY = (int(road[1][2][1]* scalar)) + yOffset
						
		# 				cv2.line(self.img, (RstartPointX,RstartPointY), (RendPointX,RendPointY), (255,255,255))


		#cv2.imshow('image', self.img)

		imgInverted = np.zeros((size[1], size[0], 3) , np.uint8)
		imgInverted[:,:] = (255,255,255)

		imgGreyScale = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

		imgGreyScale = cv2.GaussianBlur(imgGreyScale,(5,5),0)

		edges = cv2.Canny(imgGreyScale, 100,200)

		ret,thresh = cv2.threshold(edges,25,255,cv2.THRESH_TOZERO)

		imgGreyScale = cv2.bitwise_not( thresh )

		imgGreyScale = cv2.transpose(imgGreyScale)
		imgGreyScale = cv2.flip(imgGreyScale,flipCode=-1)

		cv2.imwrite(pngName,imgGreyScale)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		os.system('xdg-open ' + pngName)
