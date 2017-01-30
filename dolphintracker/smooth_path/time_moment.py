from dolphintracker.smooth_path.blob import Blob
from dolphintracker.smooth_path import tools

class TimeMoment(object):

	def __init__(self, row=None, frame=None, position=None):
		self.blobs = []
		self.frame = None
		self.found = None 

		#Initialize from the csv
		if row!=None:
			self.frame = int(float(row[0]))
			nColumns = len(row)
			for i in range( (nColumns-1)/3 ):
				blob = Blob(row, i)
				#in case the values in the csv are not empty add it to the list
				if not blob.isEmpty: self.blobs.append( blob )
			#order the blobs by area
			self.blobs = sorted(self.blobs, key=lambda x: -x.area)
			self.found = not self.isEmpty
			
		#Initialize from the position param
		elif frame!=None and position!=None:
			blob = Blob(position=position)
			self.blobs.append(blob)
			self.frame = frame
			self.found = False 


	@property
	def isEmpty(self): return len(self.blobs)==0

	def fitBlob(self, lastPos=None):
		"""
		Find the best blob for this moment
		"""
		if len(self.blobs)==0: return None

		if lastPos!=None:
			#Find the closest blob to lastPos for this TimeMoment
			positions = [ (tools.lin_dist(lastPos, x.position), x) for x in self.blobs ]
			positions = sorted(positions, key=lambda x: x[0])
			return positions[0][1]
		else:
			#The blobs are order by area size
			#It returns the biggest blob
			return self.blobs[0]

	def setPosition(self, position):
		blob = Blob(position=position) 
		self.blobs = [blob]