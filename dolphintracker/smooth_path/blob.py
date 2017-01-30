


class Blob(object):
	def __init__(self, row=None, index=None, position=None):
		self.x 		= None
		self.y 		= None
		self.area 	= None

		#Initialize the blob from the csv
		if row!=None and index!=None:
			try:
				self.x 		= float(row[1+index*3])
				self.y 		= float(row[2+index*3])
				self.area 	= float(row[3+index*3])
			except: pass

		#Initialize from the position
		elif position!=None:
			self.x     = position[0]
			self.y     = position[1]
			self.area  = 0

	@property
	def isEmpty(self): return self.x==None or self.y==None or self.area==None

	@property
	def position(self): return self.x, self.y