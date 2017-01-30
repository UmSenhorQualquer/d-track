import cv2
from numpy import *
from math import *


class BackGroundDetector(object):

	_background = None
	_backgroundSum 		= None
	_backgroundAverage 	= None
	_backgroundCounter 	= None
	_capture = None
	
	_param_bgdetector_threshold = 5
	_param_bgdetector_jump=1000
	_param_bgdetector_compare_jump = 1000

	
	def __init__(self,**kwargs):
		
		
		if "capture" not in kwargs.keys(): 
			print "The variable capture was not set in the object constructer"; exit()
		else: capture = kwargs['capture']

		self._filterFunc = kwargs.get('filterFunction', lambda x: x)

		self._width 	= capture.get( cv2.CAP_PROP_FRAME_WIDTH )
		self._height 	= capture.get( cv2.CAP_PROP_FRAME_HEIGHT )
		self._capture 	= capture
		


	def __initialize__(self):
		z = zeros( (self._height, self._width), float32 )
		self._backgroundSum = z.copy()
		self._backgroundCounter = z.copy()

	def __process(self, frame, jump2Frame=2000, comprate2jumpFrame = 1000, threshold = 5 ):
		current_frame_index = self._capture.get( cv2.CAP_PROP_POS_FRAMES )
		self._capture.set( cv2.CAP_PROP_POS_FRAMES, current_frame_index + comprate2jumpFrame )

		res, next_frame = self._capture.read()
		if res==False: return None

		next_frame  = self._filterFunc(next_frame)
		frame 		= self._filterFunc(frame)

		self._capture.set( cv2.CAP_PROP_POS_FRAMES, current_frame_index + jump2Frame )
		diff = cv2.absdiff( frame, next_frame )
		
		ret , gray = cv2.threshold(diff, threshold , 255, cv2.THRESH_BINARY )

		_, contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		hulls = []
		for contour in contours: hulls.append( cv2.convexHull( contour ) )

		backgroundArea = ones( (self._height, self._width), float32 )
		cv2.drawContours( backgroundArea,  array( hulls ) , -1, (0), -1 )
		
		self._backgroundCounter += backgroundArea

		self._backgroundSum += frame*backgroundArea

		try:
			seterr(all ='ignore')
			self._backgroundAverage = divide(self._backgroundSum , self._backgroundCounter )
		except:
			pass




	def detect(self, jump2Frame=0, comprate2jumpFrame = 1000, threshold = 5 ):
		initial_pos = self._capture.get( cv2.CAP_PROP_POS_FRAMES )

		self.__initialize__()
		old_state = seterr(all ='ignore')
		res = True
		while res:
			res, current_frame = self._capture.read()
			if not res: break
			self.__process(current_frame, jump2Frame, comprate2jumpFrame, threshold)
		self._background = cv2.convertScaleAbs(self._backgroundAverage)


		self._capture.set( cv2.CAP_PROP_POS_FRAMES, initial_pos )
		seterr(**old_state)
		
		return self._background

	def subtract( self, frame, threshold=20, thresholdValue=255 ):
		diff = cv2.absdiff(frame , self._background_color)
		ret , res = cv2.threshold(diff, threshold , 255, cv2.THRESH_BINARY )
		diff = cv2.bitwise_and(frame, res)
		return diff
























if __name__ == "__main__":
	capture = cv2.VideoCapture("/home/ricardo/Downloads/20150220_virgin_1_2015-02-20-104420-0000.avi")
	
	_gaussianBlurMatrixSize = 5
	_gaussianBlursigmaX = 5

	bg = OTPBackGroundDetector(capture=capture, gaussianBlurMatrixSize=_gaussianBlurMatrixSize, gaussianBlursigmaX=_gaussianBlursigmaX)

	#bg.detect( 100, 2000, 50 )
	bg.detect(1000, threshold = 19)
	#bg.quickDetect( )

	exit()
	capture.set( cv2.CAP_PROP_POS_FRAMES, 0 )
	waitingTime = 1

	res = True
	while res:
		res, frame = capture.read()
		image = bg.cleanNoise(frame)
		
		print "image", image
		print "background", bg.background
		diff = cv2.absdiff(image, bg.background)
		ret , gray = cv2.threshold(diff, 20 , 1, cv2.THRESH_BINARY )
		
		_, contours, hierarchy = cv2.findContours(gray.copy() * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		hulls = []
		for contour in contours: 
			if len( contour )>=5:
				ellipse = cv2.fitEllipse(contour)
				
			hull = cv2.convexHull( contour )
			hulls.append(hull)
		
		gray3Channels = cv2.merge( (gray, gray, gray )) 
		cv2.imshow("Capture", frame * gray3Channels)


		key = cv2.waitKey(waitingTime)
		if key == ord('q'): exit()
		if key == ord('w'): waitingTime = 0
		if key == ord('e'): waitingTime = 1