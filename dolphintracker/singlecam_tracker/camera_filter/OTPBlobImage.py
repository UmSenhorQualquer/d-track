import numpy as np
import math
from dolphintracker.singlecam_tracker.camera_filter.tools import *
from dolphintracker.singlecam_tracker.camera_filter.OTPBase import OTPBase


class OTPBlobImage(OTPBase):

    def __init__(self, **kwargs):
        super(OTPBlobImage, self).__init__(**kwargs)
        self._blobimg_margin = 0
        self._blobimg_cfilter = None
    
    def compute(self, blobs): 
        for blob in blobs:
            p1, p2 = blob._bounding
            margin = self._blobimg_margin
            cut_x, cut_y, cut_xx, cut_yy = p1[0]-margin, p1[1]-margin, p2[0]+margin, p2[1]+margin
            if cut_x<0: cut_x=0
            if cut_y<0: cut_y=0
            if cut_xx>self._in_original_image.shape[1]: cut_xx=self._in_original_image.shape[1]
            if cut_yy>self._in_original_image.shape[0]: cut_yy=self._in_original_image.shape[0]

            partial_image = self._in_original_image[cut_y:cut_yy, cut_x:cut_xx]

            if self._blobimg_cfilter!=None: 
                partial_image_mask = self._blobimg_cfilter(partial_image)
            else: 
                partial_image_mask = self._captured_result_image[cut_y:cut_yy, cut_x:cut_xx]
            
            if len(partial_image.shape)>2: 
                partial_image_mask_tmp = cv2.merge( (partial_image_mask,partial_image_mask,partial_image_mask) )
            else:
                partial_image_mask_tmp = partial_image_mask

            #The mask should not have holess
            contour = getBiggestContour(partial_image_mask)
            partial_image_mask = np.zeros_like(partial_image_mask)
            cv2.fillPoly(partial_image_mask, np.array([contour]), (255,255,255))
            partial_image_masked = cv2.bitwise_and(partial_image_mask_tmp, partial_image)
            partial_image_masked[partial_image_masked==255] = 0
            #############
            
            blob._oimage = partial_image
            blob._image = partial_image_masked
            blob._image_mask = partial_image_mask
            blob._image_cut = cut_x, cut_y, cut_xx, cut_yy
            
        return blobs

    def process(self, image):
        blobs = super(OTPBlobImage, self).process(image)
        return OTPBlobImage.compute(self, blobs)

