import numpy as np
import math
from tools import *
from OTPBase import OTPBase


class OTPBlobImageExtraction(OTPBase):

    def __init__(self, **kwargs):
        super(OTPBlobImageExtraction, self).__init__(**kwargs)
        self._out_image_segmentation =None
        self._out_original_image = None
        self._blobimg_cfilter = None
    
    def compute(self, blobs): 
        
        for blob in blobs:

            p1, p2 = blob._bounding
            cut_x, cut_y, cut_xx, cut_yy = p1[0]-30, p1[1]-30, p2[0]+30, p2[1]+30
            if cut_x<0: cut_x=0
            if cut_y<0: cut_y=0
            if cut_xx>self._in_original_image.shape[1]: cut_xx=self._in_original_image.shape[1]
            if cut_yy>self._in_original_image.shape[0]: cut_yy=self._in_original_image.shape[0]

            partial_image = self._in_original_image[cut_y:cut_yy, cut_x:cut_xx]

            if self._blobimg_cfilter!=None:
                partial_image_mask = self._blobimg_cfilter(partial_image)
            else: 
                partial_image_mask = self._out_segmented_image[cut_y:cut_yy, cut_x:cut_xx]
            
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
            
            blob._image = partial_image_masked
            blob._oimage = partial_image
            blob._rotated_oimage = rotate_image(partial_image, rot )
            blob._rotated_image = rotate_image( partial_image_masked, rot )
            blob._rotated_image_mask = rotate_image(partial_image_mask, rot )
            blob._image_mask = partial_image_mask

            contour = getBiggestContour(blob._rotated_image_mask)
            box = cv2.boundingRect(contour)
            p1, p2 = (box[0], box[1]), (box[0]+box[2], box[1]+box[3])

            blob._rotated_image = blob._rotated_image[p1[1]:p2[1], p1[0]:p2[0]]
            blob._rotated_image_mask = blob._rotated_image_mask[p1[1]:p2[1], p1[0]:p2[0]]
            blob._rotated_image_mask[blob._rotated_image_mask>0] = 255

            if len(blob._rotated_image.shape)==3:
                blob._rotated_image[:,:,0] = cv2.bitwise_and(blob._rotated_image_mask, blob._rotated_image[:,:,0])
                blob._rotated_image[:,:,1] = cv2.bitwise_and(blob._rotated_image_mask, blob._rotated_image[:,:,1])
                blob._rotated_image[:,:,2] = cv2.bitwise_and(blob._rotated_image_mask, blob._rotated_image[:,:,2])
            else:
                blob._rotated_image = cv2.bitwise_and(blob._rotated_image_mask, blob._rotated_image)

            

        return blobs

    def process(self, image):
    	blobs = super(OTPBlobImageExtraction, self).process(image)
        return OTPBlobImageExtraction.compute(self, blobs)

