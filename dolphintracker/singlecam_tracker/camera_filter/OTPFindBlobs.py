from dolphintracker.singlecam_tracker.camera_filter.OTPBase import *
from dolphintracker.singlecam_tracker.camera_filter.Blob import Blob
import cv2

class OTPFindBlobs(OTPBase):
    """
    Find blobs in the segmented image.
    Return a list of blobs
    """

    def __init__(self, **kwargs):
        super(OTPFindBlobs, self).__init__(**kwargs)

        self._param_min_area = 0
        self._param_max_area = 100000000

    def compute(self, frame):
        ##Inserted 16.04.2015
        img = cv2.dilate( frame, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (5,5) ), iterations=3 )
        img = cv2.erode ( img, kernel=cv2.getStructuringElement( cv2.MORPH_RECT,   (5,5) ), iterations=2 )
        #####################

        _, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        objectsFound = []
        for cnt in contours:
            m = cv2.moments(cnt); m00 = m['m00']
            
            if m00 > self._param_min_area and m00 < self._param_max_area:
                if m00!=0: centroid = ( int(round(m['m10']/m00) ), int(round(m['m01']/m00)) )
                else: centroid = (0,0)

                box = cv2.boundingRect(cnt)
                p1, p2 = (box[0], box[1]), (box[0]+box[2], box[1]+box[3])
        
                obj = Blob()
                obj._contour = cnt
                obj._bounding = (p1, p2)
                obj._area = m00
                obj._centroid = centroid
                objectsFound.append( obj )
                
        return objectsFound

    def process(self, frame):
        frame = super(OTPFindBlobs, self).process(frame)
        return OTPFindBlobs.compute(self,frame)