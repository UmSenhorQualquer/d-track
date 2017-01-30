
import csv, cv2, numpy as np, os

import pyforms
from pyforms import BaseWidget
from pyforms.Controls import ControlText
from pyforms.Controls import ControlProgress
from pyforms.Controls import ControlSlider
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlImage
from pyforms.Controls import ControlPlayer
from pyforms.Controls import ControlFile

from dolphinrender.render_positions import RenderPositions


class DolphinRender(BaseWidget):
	
	def __init__(self):
		super(DolphinRender,self).__init__('Dolphin render')

		self._sceneFile 	= ControlFile('Scene file')

		self._video0 		= ControlFile('Video 0')
		self._video1 		= ControlFile('Video 1')
		self._data 			= ControlFile('Data')
		
		self._outputfile 	= ControlText('Output movie')
		
		self._exc_btn 		= ControlButton('Run')		
		
		self.formset = [
			'_sceneFile',
			('_video0', '_video1'),
			('_data', '_outputfile'),
			'_exc_btn',
			' '
		]

		self._data.changed_changed = self.__data_changed
		self._exc_btn.value 				= self.execute


		#self._start.value = '85300'
		#self._start.value = '10500'
		#self._start.value = '11500'
		
		self._sceneFile.value 	= '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2012.12.01_13.48/2012.12.01_13.48_scene.obj'
		self._video0.value 		= '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2012.12.01_13.48/2012.12.01_13.48_Entrada (1).MP4'
		self._video1.value 		= '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2012.12.01_13.48/2012.12.01_13.48_Cascata (1).MP4'
		self._data.value		= '/home/ricardo/subversion/opencsp/applications/dolphintracker/output/2012.12.01_13.48_version_13.05.2015.csv'
		"""
		self._sceneFile.value  	= '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2013.03.16_12.18/2013.03.16_12.18_scene.obj'
		self._video0.value 		= '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2013.03.16_12.18/2013 03 16 12 18_Entrada.MP4'
		self._video1.value 		= '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2013.03.16_12.18/2013 03 16 12 18_Cascata.MP4'
		self._data.value		= '/home/ricardo/subversion/opencsp/applications/dolphintracker/output/2013 03 16 12 18.csv'
		"""

		

	def __data_changed(self):  
		head, 		tail 	  	 = os.path.split(self._data.value)
		filename, 	extention 	 = os.path.splitext(tail)
		self._outputfile.value   = "{0}_resume.avi".format(filename)


	def execute(self):
		SCENE_FILE 	= self._sceneFile.value
		VIDEO0 		= self._video0.value
		VIDEO1 		= self._video1.value

		if not os.path.exists('output'): os.makedirs('output')
		
		outVideoFilename = os.path.join('output', self._outputfile.value)
		outvideo = cv2.VideoWriter(outVideoFilename, cv2.cv.CV_FOURCC('M','J','P','G'), 30, (1920, 480))
		run = RenderPositions(SCENE_FILE, self._data.value,VIDEO0, VIDEO1, videowriter = outvideo)
		run.startScene()


def main(): pyforms.start_app( DolphinRender, geometry=(100,100,900, 180) )

if __name__ == "__main__": main()

"""
	SCENE_FILE = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2012.12.01_13.48/2012.12.01_13.48_scene.obj'
	VIDEO0 = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2012.12.01_13.48/2012.12.01_13.48_Entrada (1).MP4'
	VIDEO1 = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2012.12.01_13.48/2012.12.01_13.48_Cascata (1).MP4'

	SCENE_FILE = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2013.03.16_12.18/2013.03.16_12.18_scene.obj'
	VIDEO0 = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2013.03.16_12.18/2013 03 16 12 18_Entrada.MP4'
	VIDEO1 = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2013.03.16_12.18/2013 03 16 12 18_Cascata.MP4'
	
	if not os.path.isfile(VIDEO0): 		print 'file does not exists \n',VIDEO0
	if not os.path.isfile(VIDEO1): 		print 'file does not exists \n',VIDEO1
	if not os.path.isfile(SCENE_FILE): 	print 'file does not exists \n',SCENE_FILE

	#SCENE_FILE = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2013.03.16_12.18/2013.03.16_12.18_scene2render.obj'
	#VIDEO0 = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2013.03.16_12.18/2013 03 16 12 18_Entrada.MP4'
	#VIDEO1 = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2013.03.16_12.18/2013 03 16 12 18_Cascata.MP4'
	outvideo = cv2.VideoWriter('3dscene.avi', cv2.cv.CV_FOURCC('M','J','P','G'), 30, (1920, 480))
	run = RenderPositions(SCENE_FILE,'output/2013 03 16 12 18.csv',VIDEO0, VIDEO1,videowriter = outvideo)
	run.startScene()

	#run.loadData()
	#while True: run.process()
"""