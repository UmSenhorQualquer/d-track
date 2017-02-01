import csv, numpy as np
from dolphintracker.smooth_path import tools
from dolphintracker.smooth_path.blob import Blob
from dolphintracker.smooth_path import smooth_filters
from dolphintracker.smooth_path.time_moment import TimeMoment
from scipy.interpolate import interp1d
from PyQt4 import QtGui

START_FRAME = 0
END_FRAME 	= 18000000



def interpolatePositions(values, begin, end):
	computed_time = np.array(range(begin, end+1))
	frames 		= []
	measures_x 	= []
	measures_y 	= []
	
	for i, pos in values:
		x, y = pos
		frames.append(i)
		measures_x.append(x)
		measures_y.append(y)
	
	frames 		= np.array(frames)
	measures_x 	= np.array(measures_x)
	measures_y 	= np.array(measures_y)
	kind = 'slinear'
	if len(frames)==3: kind = 'quadratic'
	if len(frames)>=4: kind = 'cubic'

	
	cubic_interp  = interp1d(frames, measures_x, kind=kind)
	measures_x 	  = cubic_interp(computed_time)
	cubic_interp  = interp1d(frames, measures_y, kind=kind)
	measures_y    = cubic_interp(computed_time)

	results = []
	for frame, x,y in zip( range(begin,end+1), measures_x, measures_y):
		results.append( [frame, (x,y)] )
	return results





class PoolCamera(object):

	DOLPHIN_MAX_VEL_PIXEL = 3

	def __init__(self, filename):
		self.__load(filename)


	def exportTo(self, filename):
		csvfile = open( filename, 'w')
		spamwriter = csv.writer(csvfile, delimiter=';',quotechar='|',quoting=csv.QUOTE_MINIMAL)
		for moment in self.moments:
			blob = moment.fitBlob()
			spamwriter.writerow([moment.frame, blob.x, blob.y, blob.found])
		csvfile.close()


	def __load(self, filename):
		self._firstFrame = None
		self.moments = []

		with open(filename, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
			lastframe = None
			for row in spamreader:
				QtGui.QApplication.processEvents()

				moment = TimeMoment(row)

				if self._firstFrame==None: self._firstFrame = moment.frame
				if moment.isEmpty:
					self.moments.append( None )
				else:
					#Check if frames are missing
					if lastframe!=None:
						diff = (moment.frame-lastframe)
						if diff>1:
							#in case they are missing, add them as non
							for i in range(diff-1): self.moments.append( None )

					if moment.frame<=START_FRAME: 	continue
					if moment.frame>=END_FRAME: 	break

					self.moments.append( moment )			

				lastframe = moment.frame






	###########################################################################
	###########################################################################
	###########################################################################

	def fitBlob(self, index, lastPos=None):
		moment = self.moments[index]
		if moment==None: return None
		return moment.fitBlob(lastPos)

	def setPosition(self, index, position):
		if self.moments[index]!=None:
			self.moments[index].setPosition(position)
		else:
			m = TimeMoment(position=position, frame=(index+self._firstFrame) )
			self.moments[index] = m
			self.moments[index].found = False




	def CleanPositions(self):
		last_pos = None
		velocity = None

		noPosCounter = 0
		for i, moment in enumerate( self.moments ):
			QtGui.QApplication.processEvents()
			if last_pos==None and moment!=None: last_pos = moment.fitBlob().position
			
			velocity = None
			
			point = None
			if moment!=None and last_pos!=None:
				point = moment.fitBlob( lastPos=last_pos ).position
				velocity = tools.lin_dist(point, last_pos)
			
				#If the velocity is higher, this may indicate a jump error.
				maxPossibleDistance = (noPosCounter+1)*self.DOLPHIN_MAX_VEL_PIXEL
				if velocity>maxPossibleDistance: 
					#Check if the blob returns back to the same place
					for j in range(i+1, i+60):
						if j>=len(self.moments): break

						jPos = self.fitBlob(j, lastPos=last_pos)
						if j>=len(self.moments) or jPos==None: continue
						dist = tools.lin_dist(jPos.position, last_pos)
						
						#Detected a blob jump. The detection returned to the same place
						if dist<maxPossibleDistance:
							for k in range(i+1, j): self.moments[k]=None #Clean jump issues
							break

			if point!=None: last_pos = point
		




	def InterpolatePositions(self):

		positions = []
		for i, moment in enumerate( self.moments ):
			QtGui.QApplication.processEvents()
			#in case there is a tracking value
			if moment!=None:
				positions.append([moment.frame, moment.fitBlob().position])
		begin = positions[0][0]
		end = positions[-1][0]
		positions = interpolatePositions(positions, begin, end)
		for i, p in enumerate(positions):
			self.setPosition(self._firstFrame-begin+i, p[1] ) 
							
		"""
		lastFoundPosition = None
		for i, moment in enumerate( self.moments ):
			
			#in case there is a tracking value
			if moment!=None:
				if lastFoundPosition!=None:
					nframes = i - lastFoundPosition
					if nframes>1:
						p = moment.fitBlob().position
						lastPos = self.fitBlob(lastFoundPosition).position
						vector = p[0]-lastPos[0], p[1]-lastPos[1]
						vel = float(vector[0])/float(nframes), float(vector[1])/float(nframes)
						for j,index in enumerate( range(lastFoundPosition, i)):
							self.setPosition(index, (lastPos[0]+(j+1)*vel[0], lastPos[1]+(j+1)*vel[1]) ) 
							
				lastFoundPosition = i
		"""

		#Fill in the positions at the beginning of the list
		for i in range(len(self.moments)/2, -1, -1):
			if self.moments[i]==None: self.setPosition(i, self.fitBlob(i+1).position )

		#Fill in the positions at the end of the list
		for i in range(len(self.moments)/2, len(self.moments), 1):
			if self.moments[i]==None:  self.setPosition(i, self.fitBlob(i-1).position )



	def SmoothPositions(self, sigma=16): 
		positions = [ m.fitBlob().position for m in self.moments ]
		xs = [x for x,y in positions]
		ys = [y for x,y in positions]
		xs = smooth_filters.gaussian_filter(xs, sigma)
		ys = smooth_filters.gaussian_filter(ys, sigma)
		positions = [(x,y) for x,y in zip(xs, ys)]
		for i, pos in enumerate(positions):
			self.setPosition(i, pos)



if __name__=='__main__':
	import cv2

	#VIDEO = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2012.12.01_13.48/2012.12.01_13.48_Cascata (1).MP4'
	TRACKING_FILE = '../output/2012.12.01_13.48_Cascata (1)_out.csv'
	
	#VIDEO = '/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/New Videos/2013.03.16_12.18/2013 03 16 12 18_Cascata.MP4'
	#TRACKING_FILE = '../output/2013 03 16 12 18_Cascata_out.csv'
	tracking = PoolCamera(TRACKING_FILE)

	tracking.CleanPositions()
	tracking.InterpolatePositions()
	#tracking.SmoothPositions(sigma=15)

	tracking.exportTo('../output/2013 03 16 12 18_Cascata_out___.csv')


	videoCap = cv2.VideoCapture(VIDEO)
	videoCap.set(cv2.CAP_PROP_POS_FRAMES, tracking._frames[0])

	for i, p in enumerate(tracking._positions):
		res, img = videoCap.read()
		if not res: break;
		#print tracking._frames[i]
		
		if p: cv2.circle(img, (int(p[0]),int(p[1])), 6, (255,255,0), 2)
		
		cv2.imshow('img', img)
		key = cv2.waitKey(1)
		if key == 27: break