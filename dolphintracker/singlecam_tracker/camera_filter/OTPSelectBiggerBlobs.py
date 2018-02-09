import cv2, time, itertools
from numpy import *
from math import *

from dolphintracker.singlecam_tracker.camera_filter.OTPBase import *


class OTPSelectBiggerBlobs(OTPBase):
    """
    Selects the biggest blobs
    Return: Return the number of blobs setted in the variable _param_n_blobs
    """

    def __init__(self, **kwargs):
        super(OTPSelectBiggerBlobs, self).__init__(**kwargs)
        
        self._param_n_blobs = 1

    def compute(self, blobs):
        blobs = sorted(blobs,key=lambda a:a._area,reverse=True)
        if len(blobs)>self._param_n_blobs: return blobs[:self._param_n_blobs]
        else: return blobs

    def process(self, blobs):
        blobs = super(OTPSelectBiggerBlobs, self).process(blobs)
        return OTPSelectBiggerBlobs.compute(self,blobs)