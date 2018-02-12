import cv2, numpy as np
from dolphintracker.singlecam_tracker.camera_filter.FindDolphin import SearchBlobs
from dolphintracker.singlecam_tracker.camera_filter.BackGroundDetector import BackGroundDetector
import datetime

class PoolCamera(object):

	def __init__(self, videofile, name, scene, maskObjectsNames, filters, frames_range=None):
		
		self.name 	      = name
		self.videoCap     = cv2.VideoCapture(videofile)
		self.scene 	      = scene
		self.filters      = filters
		self.mask 	  	  = self.create_mask(maskObjectsNames)
		self.frames_range = frames_range

		self._searchblobs = SearchBlobs()

		self._backgrounds 	 = []
		self._last_centroid = None

		if self.frames_range is not None:
			self.videoCap.set(cv2.CAP_PROP_POS_FRAMES, self.frames_range[0])
			print('set first frame', self.frames_range)

		self._total_frames = self.videoCap.get(7)

		self._colors = [(255,0,0),(0,255,0),(0,0,255)]

	def create_mask(self, objectsNames):
		mask = np.zeros((self.img_height,self.img_width), np.uint8)
		for objname in objectsNames:
			obj = self.scene.getObject(objname)
			ptsProjection = self.points_projection( [p for p in obj.points if p[2]<0.2] )
			hull = cv2.convexHull(np.int32(ptsProjection))
			cv2.fillPoly(mask, np.int32([hull]), 255)
		return mask

	def read(self):
		res, self.frame = self.videoCap.read()
		if res:
			self.originalFrame = self.frame.copy()
		else:
			self.originalFrame = None
		return res


	def process(self):
		if len(self._backgrounds)==0:
			for i, colorFilter in enumerate(self.filters):
				firstFrame = self.frame_index
				bgDetector = BackGroundDetector(capture=self.videoCap, filterFunction=colorFilter.process)
				
				print('Background detection parameters', self._total_frames*0.04, self._total_frames*0.03)
				last_frame = self.frames_range[1] if self.frames_range is not None else None
				
				bg = bgDetector.detect(int(self._total_frames*0.04), int(self._total_frames*0.03), 180, last_frame)
				bg = cv2.dilate( bg, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (5,5) ), iterations=2 )
				bg = 255-bg
				bg[bg<255]=0
				self._backgrounds.append( cv2.bitwise_and(bg, self.mask) )

			self.frame_index = firstFrame

		result = []
		for i, colorFilter in enumerate(self.filters):

			filterResult = colorFilter.filter(self.frame, self._backgrounds[i])
			blobs        = self._searchblobs.process(filterResult)
			res = blobs[0] if len(blobs)>=1 else None
			result.append(res)
			
			
		return result



	def create_empty_mask(self): return np.zeros( (self.img_height, self.img_width), np.uint8 )

	def points_projection(self, points): cam = self.scene_camera; return [cam.calcPixel(*p) for p in points]

	@property
	def scene_camera(self): return self.scene.getCamera(self.name)

	@property
	def img_width(self):  return int( self.videoCap.get(cv2.CAP_PROP_FRAME_WIDTH)  )

	@property
	def img_height(self): return int( self.videoCap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
	
	@property
	def fps(self): return int( self.videoCap.get(cv2.CAP_PROP_FPS) )

	@property 
	def frame_index(self): return int( self.videoCap.get(cv2.CAP_PROP_POS_FRAMES)  )
	@frame_index.setter
	def frame_index(self, value): self.videoCap.set(cv2.CAP_PROP_POS_FRAMES, value)
	
	@property 
	def currentTime(self): 
		milli =  self.videoCap.get(cv2.CAP_PROP_POS_MSEC)
		return datetime.timedelta(milliseconds=milli)
	
	
	@property
	def totalFrames(self): return self.videoCap.get(cv2.CAP_PROP_FRAME_COUNT)