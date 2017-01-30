import pyforms
from pyforms			import BaseWidget
from pyforms.Controls	import ControlText
from pyforms.Controls	import ControlProgress
from pyforms.Controls	import ControlSlider
from pyforms.Controls	import ControlButton
from pyforms.Controls	import ControlPlayer
from pyforms.Controls	import ControlFile
from pyforms.utils 		import tools
import os, cv2, shutil, numpy as np, csv

from dolphintracker.singlecam_tracker.camera_filter.FindDolphin import FilterAllPool
from dolphintracker.singlecam_tracker.pool_camera import PoolCamera

from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.Scene import Scene



class SingleCamTracker(BaseWidget):
		
	def __init__(self):
		super(SingleCamTracker,self).__init__('Dolphin tracker')

		self._sceneFile 	= ControlFile('Scene file')

		self._video 		= ControlFile('Video')
		
		self._outputfile 	= ControlText('Output zip file')
		self._camera 	 	= ControlText('Camera')
		self._player 		= ControlPlayer('Image')
		self._start 	 	= ControlText('Start on frame', '0')

		self._blockSize1 	= ControlSlider('Thresh block size', 193, 1, 1001)
		self._cValue1 		= ControlSlider('Thresh C value',	 284, 0, 500)

		self._blockSize2 	= ControlSlider('Thresh block size', 463, 1, 1001)
		self._cValue2 		= ControlSlider('Thresh C value', 	 289, 0, 500)
		
		self._blockSize3 	= ControlSlider('Thresh block size', 910, 1, 1001)
		self._cValue3 		= ControlSlider('Thresh C value', 	 288, 0, 500)
	
		self._exc_btn 		= ControlButton('Run')		

		self.formset = [ 	'_sceneFile'	,
							('_video', '_start'),
							('_camera', '_outputfile'),
							('_blockSize1', '_cValue1'),
							('_blockSize2', '_cValue2'),
							('_blockSize3', '_cValue3'),
							'_player','_exc_btn']

		self.has_progress = True
		self._video.changed_event 			= self.__video_changed
		self._player.process_frame_event 	= self.__processFrame

		self._blockSize1.changed_event 		= self._player.refresh
		self._blockSize2.changed_event 		= self._player.refresh
		self._blockSize3.changed_event 		= self._player.refresh
		self._cValue1.changed_event 		= self._player.refresh
		self._cValue2.changed_event 		= self._player.refresh
		self._cValue3.changed_event 		= self._player.refresh
		self._exc_btn.value 				= self.execute
		
		self._sceneFile.value = '/home/ricardo/Desktop/01Apollo201403210900/2013.11.23_10.59/2013.11.23_10.59_scene.obj'
		self._video.value = '/home/ricardo/Desktop/01Apollo201403210900/2013.11.23_10.59/2013.11.23_10.59_Entrada.MP4'
		self._camera.value = 'Camera1'
		self._start.value = '19977'
		
		

	def __processFrame(self, frame): 
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

	def __video_changed(self):  
		self._player.value = self._video.value
		head, 		tail 	  	 = os.path.split(self._video.value)
		filename, 	extention 	 = os.path.splitext(tail)
		self._outputfile.value   = "{0}_out.zip".format(filename)
		
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
		if not os.path.exists('output'): os.makedirs('output')

		VIDEO_FILE		= self._video.value
		VIDEO_OUT_FILE 	= self.output_videofile
		FIRST_FRAME 	= eval(self._start.value)
		SCENE_FILE		= self._sceneFile.value

		world 				= WavefrontOBJReader(SCENE_FILE)
		scene 				= Scene()
		scene.objects 		= world.objects
		scene.cameras 		= world.cameras
		
		filterCamera1 =  FilterAllPool()

		filterCamera1._param_tb_block_size       = self._blockSize1.value if (self._blockSize1.value % 2)!=0 else (self._blockSize1.value+1)
		filterCamera1._param_tb_c                = self._cValue1.value
		
		filterCamera2 =  FilterAllPool()
		filterCamera2._param_tb_block_size       = self._blockSize2.value if (self._blockSize2.value % 2)!=0 else (self._blockSize2.value+1)
		filterCamera2._param_tb_c                = self._cValue2.value

		filterCamera3 =  FilterAllPool()
		filterCamera3._param_tb_block_size       = self._blockSize3.value if (self._blockSize3.value % 2)!=0 else (self._blockSize3.value+1)
		filterCamera3._param_tb_c                = self._cValue3.value
		
		
		camera = PoolCamera( VIDEO_FILE, self._camera.value, scene, ['Pool'], [filterCamera1, filterCamera2, filterCamera3] )

		camera.frame_index = FIRST_FRAME
		self.max_progress = camera.totalFrames-FIRST_FRAME
		
		OUT_IMG_WIDTH  = camera.img_width  // 3
		OUT_IMG_HEIGHT = camera.img_height // 3
		fourcc    	   = cv2.VideoWriter_fourcc('M','J','P','G')
		outvideofile   = os.path.join('output',VIDEO_OUT_FILE)
		outVideo 	   = cv2.VideoWriter( outvideofile,fourcc, camera.fps, (OUT_IMG_WIDTH,OUT_IMG_HEIGHT) )
		csvfile = open( os.path.join( 'output', self.output_csvfile ), 'w')
		spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|',quoting=csv.QUOTE_MINIMAL)

		count = 0
		point = None
		while True:
			frameIndex = camera.frame_index
			res = camera.read()
			
			if not res: break

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
			self.progress = count
			count +=1
			
		csvfile.close()
		outVideo.release()

		tools.zipdir('output', os.path.join('output', self._outputfile.value) )
		for filename in os.listdir("output"):
			path2file = os.path.join('output', filename)
			if os.path.isdir(path2file): shutil.rmtree( path2file )
			elif os.path.splitext(filename)[1].lower()!='.zip': os.remove( path2file )


##################################################################################################################
##################################################################################################################
##################################################################################################################

def main(): pyforms.start_app( SingleCamTracker )

if __name__ == "__main__":	main()
	

