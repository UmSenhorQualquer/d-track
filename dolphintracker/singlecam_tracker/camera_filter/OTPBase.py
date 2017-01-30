import cv2, time, itertools
from numpy import *
from math import *

class OTPBase(object):

	def __init__(self, **kwargs):
		super(OTPBase, self).__init__()

	def compute(self, frame):
		return frame

	def process(self, frame):
		return frame