import csv, os
from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from dolphintracker.smooth_path.pool_camera import PoolCamera
from py3dengine.scenes.SceneClient 	import SceneClient
from py3dengine.scenes.Scene 		import Scene
from py3dengine.cameras.Ray 		import Ray, lin3d_distance

import pyforms
from pyforms			import BaseWidget
from pyforms.Controls	import ControlText
from pyforms.Controls	import ControlFile
from pyforms.Controls	import ControlButton

class SmoothPath(BaseWidget):

	def __init__(self):
		super(SmoothPath,self).__init__('Smooth path')

		self._scenefile			= ControlFile('Scene file')
		self._trackfile0 		= ControlFile('Tracking from camera 0')
		self._trackfile1 		= ControlFile('Tracking from camera 1')
		self._videofile0		= ControlFile('Camera 0 video')
		self._videofile1		= ControlFile('Camera 1 video')
		self._outputfile 		= ControlText('Output zip file')
		self._refraction_index 	= ControlText('Refraction index', '1.4')
		self._exc_btn 		= ControlButton('Run')		

		self.has_progress = True

		self.formset = [ 	'_scenefile'	,
							('_videofile0', '_trackfile0'),
							('_videofile1', '_trackfile1'),
							('_outputfile', '_refraction_index'),
							'_exc_btn', ' ']

		self._exc_btn.value = self.execute
		self._scenefile.changed_event = self.__scenefile_changed
		
	def __scenefile_changed(self):  
		head, tail 	  	 = os.path.split(self._scenefile.value)
		filename, 	extention 	 = os.path.splitext(tail)
		self._outputfile.value   = os.path.join('output', "{0}_3d_tracking.csv".format(filename))


	def execute(self):
		if not os.path.exists('output'): os.makedirs('output')

		DEBUG 				= True		
		#SCENE_FILE 			= '/media/ricardo/Elements/DOLPHINS/New Videos/2013.04.21_12.51/2013.04.21_12.51_scene.obj'
		#VIDEO0 				= '/media/ricardo/Elements/DOLPHINS/New Videos/2013.04.21_12.51/2013 04 21 12 51_Entrada (2).MP4'
		#VIDEO1 				= '/media/ricardo/Elements/DOLPHINS/New Videos/2013.04.21_12.51/2013 04 21 12 51_Cascata (2).MP4'
		#TRACKING_FILE0 		= '/home/ricardo/Downloads/output/2013 04 21 12 51_Entrada (2)_out.csv'
		#TRACKING_FILE1 		= '/home/ricardo/Downloads/output/2013 04 21 12 51_Cascata (2)_out.csv'
		#REFRACTION_INDEX 		= 1.4
		#OUTPUT_FILE 			= os.path.join( '..','output', '3dpositions.csv')


		SCENE_FILE 			= self._scenefile.value
		VIDEO0 				= self._videofile0.value
		VIDEO1 				= self._videofile1.value
		TRACKING_FILE0 		= self._trackfile0.value
		TRACKING_FILE1 		= self._trackfile1.value
		REFRACTION_INDEX 	= eval(self._refraction_index.value)
		OUTPUT_FILE 		= self._outputfile.value

		world 			= WavefrontOBJReader(SCENE_FILE)
		scene 			= Scene()
		scene.objects 	= world.objects
		scene.cameras 	= world.cameras

		cameras 		= scene.cameras
		objects 		= scene.objects
		pool 			= scene.getObject('Pool')
		camera_filter	= scene.getCamera('Camera1')
		camera1			= scene.getCamera('Camera2')
		floor 			= scene.getObject('Floor')
		floor.refraction = REFRACTION_INDEX

		print "loading files"
		tracking0 = PoolCamera(TRACKING_FILE0)
		tracking1 = PoolCamera(TRACKING_FILE1)
		############################################################
		#Check of any of the cameras did not detect the first frame
		#If not instanciate it
		b0 = tracking0.fitBlob(0)
		b1 = tracking1.fitBlob(0)


		if b0==None and b1!=None:
			ray = camera1.addRay( *b1.position ); ray.collidePlanZ(0); 
			pixel = camera_filter.calcPixel(*ray.endPoint); tracking0.setPosition(0, pixel)
		if b0!=None and b1==None:
			ray = camera_filter.addRay( *b0.position ); ray.collidePlanZ(0); 
			pixel = camera1.calcPixel(*ray.endPoint); tracking1.setPosition(0, pixel)


		############################################################

		print "clean paths"
		trackings = [tracking0, tracking1]
		for i, tracking in enumerate(trackings):
			tracking.CleanPositions();
			tracking.InterpolatePositions()

		camera_filterPos = tuple(camera_filter.position.tolist()[0])
		camera1Pos = tuple(camera1.position.tolist()[0])

		self.max_progress = len(tracking0.moments)*2

		last3dPos = None
		count = 0

		print "getting the 3d position"
		for index, (m0, m1) in enumerate(zip(tracking0.moments, tracking1.moments)):
			p0, p1 = m0.fitBlob().position, m1.fitBlob().position

			for cam in cameras: cam.cleanRays()
			ray0 = camera_filter.addRay( p0[0], p0[1], 30 ) if p0 else None
			ray1 = camera1.addRay( p1[0], p1[1], 30 ) if p1 else None

			if (count % 1000)==0: print count
			if (count==6000) and not DEBUG: break
			count+=1
			
			d, pA,pB, current3dPos = Ray.FindClosestPointBetweenRays(ray0, ray1)
			if last3dPos==None: last3dPos = current3dPos


			DISTANCE_LIMIT = 0.6
			if m0.found and m1.found: DISTANCE_LIMIT = 0.6

			if d>DISTANCE_LIMIT:

				cam0Distance = lin3d_distance(camera_filterPos, last3dPos)
				cam1Distance = lin3d_distance(camera1Pos, last3dPos)

				diff = abs(cam0Distance-cam1Distance)
				

				flag = (m0.found and (not m1.found)) if diff<=0.6 else (cam0Distance<cam1Distance)
				
				if flag:
					camA 	  = camera_filter
					trackingA = tracking0
					camB 	  = camera1
					trackingB = tracking1			
				else:
					camA 	  = camera1
					trackingA = tracking1
					camB 	  = camera_filter
					trackingB = tracking0
					
				previousRay = camA.addRay(  *trackingA.fitBlob(index-1).position )
				currentRay  = camA.addRay( 	*trackingA.fitBlob(index).position )

				previousRay.collidePlanZ(0); prevSurfPoint = previousRay.endPoint
				currentRay.collidePlanZ(0);  currSurfPoint = currentRay.endPoint

				prevPixel = camB.calcPixel(*prevSurfPoint);
				currPixel = camB.calcPixel(*currSurfPoint);
				velocity = [currPixel[0]-prevPixel[0], currPixel[1]-prevPixel[1]]

				p = trackingB.fitBlob(index-1).position
				newPos = (p[0]+velocity[0], p[1]+velocity[1])
				
				rayA = camA.addRay( *trackingA.fitBlob(index).position )
				rayB = camB.addRay( *newPos )
				rayA.collidePlanZ(0); surfPointA = rayA.endPoint
				rayB.collidePlanZ(0); surfPointB = rayB.endPoint

				if lin3d_distance(surfPointA, surfPointB)>2.0:
					newPos = camB.calcPixel(*surfPointA);

				trackingB.setPosition(index, newPos)

			else:
				last3dPos = current3dPos

			self.progress = index

		for tracking in trackings: tracking.SmoothPositions(sigma=32);

		if not DEBUG:

			csvfile = open( OUTPUT_FILE, 'w')
			spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|',quoting=csv.QUOTE_MINIMAL)
			objects = [floor]

			for i, (m0, m1) in enumerate( zip(tracking0.moments, tracking1.moments) ):
				camera_filter.cleanRays()
				camera1.cleanRays()

				if (i % 1000)==0: print i
				
				frame  = m0.frame
				pixel0 = m0.fitBlob().position
				pixel1 = m1.fitBlob().position
				found0 = m0.found
				found1 = m1.found

				ray0 = camera_filter.addRay(pixel0[0], pixel0[1], z=30, color=(0,1.0,0) )
				ray1 = camera1.addRay(pixel1[0], pixel1[1], z=30, color=(0,1.0,0))


				ray0.collide( objects ); ray1.collide( objects )

				res = Ray.FindClosestPointBetweenRays(ray0, ray1)
				point = res[3]
				
				
				spamwriter.writerow( [frame] + list(point) + list(pixel0) + [found0] + list(pixel1)  + [found1] )

				self.progress = index+len(tracking0.moments)
				
			csvfile.close()	








def main(): pyforms.start_app( SmoothPath, geometry=(100,100,900,200) )

if __name__ == "__main__":	main()