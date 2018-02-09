import numpy as np, cv2
from dolphintracker.singlecam_tracker.camera_filter.OTPFindBlobs import OTPFindBlobs
from dolphintracker.singlecam_tracker.camera_filter.OTPSelectBiggerBlobs import OTPSelectBiggerBlobs
from dolphintracker.singlecam_tracker.camera_filter.OTPAdaptativeThreshold import OTPAdaptativeThreshold
from dolphintracker.singlecam_tracker.camera_filter.OTPMaskFromGeometry import OTPMaskFromGeometry
from dolphintracker.singlecam_tracker.camera_filter.OTPBlobImage import OTPBlobImage

from dolphintracker.singlecam_tracker.camera_filter.OTPRemoveBackground import OTPRemoveBackground
from dolphintracker.singlecam_tracker.camera_filter.BackGroundDetector import BackGroundDetector


class FilterAllPool( OTPAdaptativeThreshold):
    def __init__(self, **kwargs):
        super(FilterAllPool, self).__init__(**kwargs)

        self._param_tb_color_component  = 0
        self._param_tb_color_domain     = cv2.COLOR_BGR2GRAY
        self._param_tb_adaptive_method  = cv2.ADAPTIVE_THRESH_MEAN_C
        self._param_tb_threshold_type   = cv2.THRESH_BINARY_INV
        self._param_tb_block_size       = 201
        self._param_tb_c                = 283

    #def process(self, frame):
    #    return super(FilterAllPool, self).process(g)

    def filter(self, frame, mask):
        b, g, r = cv2.split(frame)
        gray = g
        filterResult = self.process(gray)
        #g = self.process(g)
        #b = self.process(b)

        #cv2.imshow('i', cv2.bitwise_and(g,b) )
        #cv2.waitKey(2)

        filterResult = cv2.bitwise_and(filterResult, gray)
        filterResult = cv2.bitwise_and(filterResult, mask)
        #filterResult[filterResult>80] = 0; 
        #filterResult[filterResult>100] = 0; 
        #filterResult[filterResult>0] = 255

        filterResult = cv2.erode(  filterResult, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (3,3) ), iterations=1 )
        filterResult = cv2.dilate( filterResult, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (5,5) ), iterations=2 )
        return filterResult

class SearchBlobs(OTPSelectBiggerBlobs,OTPFindBlobs):

    def __init__(self, **kwargs):
        super(SearchBlobs, self).__init__(**kwargs)

        self._param_min_area = 20
        self._param_max_area = 100000
        self._param_n_blobs = 1


def filterFunc( frame):
    filterAllPool   = FilterAllPool()
    img = filterAllPool.process(frame)
    img = cv2.dilate( img, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (3,3) ), iterations=1 )
    #cv2.imshow("2", img)

    #cv2.waitKey(1)
    
    return img

















if __name__ == "__main__":
    import cv2
    capture = cv2.VideoCapture("/home/ricardo/subversion/MEShTracker/Dolphin/DOLPHINS/13_02_2015/2013 03 12 15 44_Entrada.MP4")
    capture.set(cv2.CAP_PROP_POS_FRAMES, 60000)

    filterAllPool   = FilterAllPool()
    filterDolphin   = FilterDolphin()

    #bg = cv2.imread('color_background.png')
    #bg = cv2.adaptiveThreshold( bg, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    #    cv2.THRESH_BINARY_INV, 51, 0)

    #cv2.imshow("Capture", bg)
    #key = cv2.waitKey(0)
    detector = BackGroundDetector(capture=capture, filterFunction=filterFunc)
    bg = detector.detect(4000, 2000, 180)
    bg = 255-bg
    bg[bg<255]=0
    cv2.imshow('bg', bg)
    #cv2.waitKey(0)
    while True:
        res, frame = capture.read()
        if not res: break;
        
        filterResult  = filterAllPool.process(frame)
        filterResult = cv2.bitwise_and(filterResult, bg)

        #filterResult = cv2.erode ( filterResult, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (3,3) ), iterations=2 )
        #filterResult = cv2.dilate( filterResult, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (3,3) ), iterations=2 )
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_and(filterResult, gray)
        gray[gray>80] = 0; gray[gray>0] = 255
        
        filterResult = cv2.dilate( gray, kernel=cv2.getStructuringElement( cv2.MORPH_RECT, (5,5) ), iterations=2 )

        cv2.imshow('res', gray)
        cv2.imshow('filterResult', filterResult)
        #cv2.waitKey(0)
        
        blobs         = findDolphin.process(filterResult)

        for b in blobs: b.draw(frame)


        cv2.imshow("Capture", frame)

        key = cv2.waitKey(1)
        if key == ord('q'): break