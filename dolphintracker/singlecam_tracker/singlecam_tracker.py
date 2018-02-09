import pyforms
from pyforms			import BaseWidget
from pyforms.controls	import ControlText
from pyforms.controls	import ControlProgress
from pyforms.controls	import ControlSlider
from pyforms.controls	import ControlButton
from pyforms.controls	import ControlPlayer
from pyforms.controls	import ControlFile
from pyforms.controls	import ControlCombo
from pyforms.controls	import ControlBoundingSlider
from pyforms.utils 		import tools
import os, cv2, shutil, numpy as np, csv

from dolphintracker.singlecam_tracker.camera_filter.FindDolphin import FilterAllPool
from dolphintracker.singlecam_tracker.pool_camera import PoolCamera

from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.Scene import Scene



class SingleCamTracker(BaseWidget):
		
	def __init__(self):
		super(SingleCamTracker,self).__init__('Dolphin tracker')

		self.set_margin(5)

		self._sceneFile 	= ControlFile('Scene file')

		self._video 		= ControlFile('Video')
		
		self._camera 	 	= ControlCombo('Camera', enabled=False)
		self._player 		= ControlPlayer('Image')
		self._range 	 	= ControlBoundingSlider('Frames to analyse', default=[0, 100], enabled=False)

		self._blockSize1 	= ControlSlider('Thresh block size', default=193, minimum=2, maximum=1001)
		self._cValue1 		= ControlSlider('Thresh C value',	 default=284, minimum=0, maximum=500)

		self._blockSize2 	= ControlSlider('Thresh block size', default=463, minimum=2, maximum=1001)
		self._cValue2 		= ControlSlider('Thresh C value', 	 default=289, minimum=0, maximum=500)
		
		self._blockSize3 	= ControlSlider('Thresh block size', default=910, minimum=2, maximum=1001)
		self._cValue3 		= ControlSlider('Thresh C value', 	 default=288, minimum=0, maximum=500)
	
		self._exc_btn 		= ControlButton('Run')

		self._progress 		= ControlProgress('Progress', visible=False)

		self.formset 		= [ 	
			'_video',
			'_range',
			('_sceneFile', '_camera'),
			('_blockSize1', '_cValue1'),
			('_blockSize2', '_cValue2'),
			('_blockSize3', '_cValue3'),
			'_player','_exc_btn',
			'_progress'
		]

		self.has_progress = True
		self._video.changed_event 			= self.__video_changed_evt
		self._player.process_frame_event 	= self.__process_frame_evt
		self._sceneFile.changed_event 		= self.__scene_changed_evt

		self._blockSize1.changed_event 		= self._player.refresh
		self._blockSize2.changed_event 		= self._player.refresh
		self._blockSize3.changed_event 		= self._player.refresh
		self._cValue1.changed_event 		= self._player.refresh
		self._cValue2.changed_event 		= self._player.refresh
		self._cValue3.changed_event 		= self._player.refresh
		self._exc_btn.value 				= self.execute
		
		"""
		self._sceneFile.value = '/home/ricardo/Downloads/golfinhos/2013.11.23_10.59_scene.obj'
		self._video.value 	  = '/home/ricardo/Downloads/golfinhos/2013.11.23_10.59_Entrada.MP4'
		self._range.value     = [9000, self._range.max]
		"""
		
	def __scene_changed_evt(self):
		if self._sceneFile.value:
			self._camera.enabled = True
			world 				= WavefrontOBJReader(self._sceneFile.value)
			scene 				= Scene()
			scene.objects 		= world.objects
			scene.cameras 		= world.cameras

			self._camera.clear()
			for cam in scene.cameras:
				self._camera.add_item(cam.name)
		else:
			self._camera.enabled = False
		
	def __video_changed_evt(self):
		self._player.value 	   = self._video.value
		head, 		tail 	   = os.path.split(self._video.value)
		filename, 	extention  = os.path.splitext(tail)

		if self._video.value:
			self._range.enabled = True
			self._range.max 	= self._player.max
			self._range.value 	= self._range.value[0], self._player.max
		else:
			self._range.enabled = False



	def __process_frame_evt(self, frame): 
		b, g, r = cv2.split(frame)
		thresh = g
		
		blockSize = self._blockSize1.value
		if (blockSize % 2)==0: blockSize+=1

		res1 = cv2.adaptiveThreshold(thresh,255,
			cv2.ADAPTIVE_THRESH_MEAN_C,
			cv2.THRESH_BINARY_INV, blockSize, self._cValue1.value-255)
		#res1 = cv2.bitwise_and(thresh, res1)
		#res1[res1>140] = 0; 
		#res1[res1>0] = 255
		#res1 = cv2.erode(  res1, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (3,3) ), iterations=1 )
		#res1 = cv2.dilate( res1, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (5,5) ), iterations=2 )


		blockSize = self._blockSize2.value
		if (blockSize % 2)==0: blockSize+=1

		res2 = cv2.adaptiveThreshold(thresh,255,
			cv2.ADAPTIVE_THRESH_MEAN_C,
			cv2.THRESH_BINARY_INV, blockSize, self._cValue2.value-255)
		#res2 = cv2.bitwise_and(thresh, res2)
		#res2[res2>160] = 0; 
		#res2[res2>0] = 255
		#res2 = cv2.erode(  res2, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (3,3) ), iterations=1 )
		#res2 = cv2.dilate( res2, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (5,5) ), iterations=2 )


		blockSize = self._blockSize3.value
		if (blockSize % 2)==0: blockSize+=1

		res3 = cv2.adaptiveThreshold(thresh,255,
			cv2.ADAPTIVE_THRESH_MEAN_C,
			cv2.THRESH_BINARY_INV, blockSize, self._cValue3.value-255)
		#res3 = cv2.bitwise_and(thresh, res3)
		#res3[res3>100] = 0; 
		#res3[res3>0] = 255
		#res3 = cv2.erode(  res3, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (3,3) ), iterations=1 )
		#res3 = cv2.dilate( res3, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (5,5) ), iterations=2 )
		resImg = cv2.merge((res1, res2, res3))
		#resImg[resImg==0] = 255
		#res = np.zeros_like(resImg) + 255
		#resImg = cv2.bitwise_and(res, resImg)
		return [frame, resImg]


	@property
	def output_videofile(self):
		head, 		tail 	  	 = os.path.split(self._video.value)
		filename, 	extention 	 = os.path.splitext(tail)
		return "{0}_out.avi".format(filename)

	@property
	def output_csvfile(self):
		head, 		tail 	  	 = os.path.split(self._video.value)
		filename, 	extention 	 = os.path.splitext(tail)
		return "{0}_out.csv".format(filename)









	def execute(self):
		self._exc_btn.enabled = False
		self._blockSize1.enabled = False
		self._blockSize2.enabled = False
		self._blockSize3.enabled = False
		self._cValue1.enabled = False
		self._cValue2.enabled = False
		self._cValue3.enabled = False
		self._sceneFile.enabled  = False
		self._video.enabled = False
		self._range.enabled = False
		self._camera.enabled = False

		if not os.path.exists('output'): os.makedirs('output')

		VIDEO_FILE				= self._video.value
		VIDEO_OUT_FILE 			= self.output_videofile
		SCENE_FILE				= self._sceneFile.value
		FIRST_FRAME, LAST_FRAME = self._range.value
		
		world 				= WavefrontOBJReader(SCENE_FILE)
		scene 				= Scene()
		scene.objects 		= world.objects
		scene.cameras 		= world.cameras
		
		filterCamera1 =  FilterAllPool()

		filterCamera1._param_tb_block_size = self._blockSize1.value if (self._blockSize1.value % 2)!=0 else (self._blockSize1.value+1)
		filterCamera1._param_tb_c          = self._cValue1.value
		
		filterCamera2 =  FilterAllPool()
		filterCamera2._param_tb_block_size = self._blockSize2.value if (self._blockSize2.value % 2)!=0 else (self._blockSize2.value+1)
		filterCamera2._param_tb_c          = self._cValue2.value

		filterCamera3 =  FilterAllPool()
		filterCamera3._param_tb_block_size = self._blockSize3.value if (self._blockSize3.value % 2)!=0 else (self._blockSize3.value+1)
		filterCamera3._param_tb_c          = self._cValue3.value

		self._progress.show()
		self._progress.max = LAST_FRAME-FIRST_FRAME
		self._progress.min = 0
		
		
		camera = PoolCamera( VIDEO_FILE, self._camera.value, scene, ['Pool'], [filterCamera1, filterCamera2, filterCamera3] )

		camera.frame_index = FIRST_FRAME
		self.max_progress = camera.totalFrames-FIRST_FRAME
		
		OUT_IMG_WIDTH  = camera.img_width  // 3
		OUT_IMG_HEIGHT = camera.img_height // 3
		fourcc    	   = cv2.VideoWriter_fourcc('M','J','P','G')
		outvideofile   = os.path.join('output',VIDEO_OUT_FILE)
		outVideo 	   = cv2.VideoWriter( outvideofile,fourcc, camera.fps, (OUT_IMG_WIDTH,OUT_IMG_HEIGHT) )
		csvfile 	   = open( os.path.join( 'output', self.output_csvfile ), 'w')
		spamwriter     = csv.writer(csvfile, delimiter=';',quotechar='|',quoting=csv.QUOTE_MINIMAL)

		count = 0
		point = None

		

		while True:
			frameIndex = camera.frame_index
			res = camera.read()

			
			
			if not res: break
			if frameIndex>LAST_FRAME: break

			blobs = camera.process()

		
			"""
			frame = camera.originalFrame.copy()
			f, axarr = plt.subplots(len(blobs), sharex=True)
			plt.xlim([0,256])
			for i, blob in enumerate(blobs):
				if blob==None: continue
				p1, p2 = blob._bounding
				cut_x, cut_y, cut_xx, cut_yy = p1[0]-30, p1[1]-30, p2[0]+30, p2[1]+30
				if cut_x<0: cut_x=0
				if cut_y<0: cut_y=0
				if cut_xx>frame.shape[1]: cut_xx=frame.shape[1]
				if cut_yy>frame.shape[0]: cut_yy=frame.shape[0]

				img = frame[cut_y:cut_yy, cut_x:cut_xx]
				cv2.imshow('camera'+str(i), img)

				color = ('b','g','r')
				for j,col in enumerate(color):
					histr = cv2.calcHist([img],[j],None,[256],[0,256])
					axarr[i].plot(histr,color = col)
			"""	
				
			for i, b in enumerate(blobs): 
				if b!=None: b.draw(camera.originalFrame, color=camera._colors[i] )

			row2save = [frameIndex]
			for blob in blobs:
				row2save += (list(blob._centroid)+[blob._area]) if blob!=None else [None, None,None]
			
			spamwriter.writerow(row2save)
		
			img = cv2.resize(camera.originalFrame, (OUT_IMG_WIDTH,OUT_IMG_HEIGHT))
			cv2.putText(img, str(frameIndex), (20, 50), cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255), thickness=2, lineType=cv2.LINE_AA)
			cv2.putText(img, str(frameIndex), (20, 50), cv2.FONT_HERSHEY_PLAIN, 1.0, (0,0,0), thickness=1, lineType=cv2.LINE_AA)


			outVideo.write(img)
			self._player.image = img
			count +=1

			self._progress.value = count


		csvfile.close()
		outVideo.release()

		self._progress.hide()
		self._exc_btn.enabled = True
		self._blockSize1.enabled = True
		self._blockSize2.enabled = True
		self._blockSize3.enabled = True
		self._cValue1.enabled = True
		self._cValue2.enabled = True
		self._cValue3.enabled = True
		self._sceneFile.enabled  = True
		self._video.enabled = True
		self._range.enabled = True
		self._camera.enabled = True

##################################################################################################################
##################################################################################################################
##################################################################################################################

def main(): pyforms.start_app( SingleCamTracker, geometry=(100,100, 800, 700) )

if __name__ == "__main__":	main()
	

