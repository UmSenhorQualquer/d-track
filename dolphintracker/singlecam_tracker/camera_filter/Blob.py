import cv2, numpy as np, math, tools

class Blob(object):

    def __text(self, frame, text, pos, color=(0,0,255) ):
        cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_PLAIN, 1.5, (255,255,255), thickness=10, lineType=cv2.LINE_AA)
        cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_PLAIN, 1.5, color, thickness=2, lineType=cv2.LINE_AA)
         
    def draw_properties(self, frame, color=(0,0,255)):
        if len(self._contour)<5: return
        p = self._centroid

        #area = cv2.contourArea(self._contour)
        self.__text( frame, "Ang: %.2f" % self.angle_degrees,(p[0]+40,p[1]-30), color=(0,150,0) )
        self.__text( frame, "Area: %.2f" % self._area,(p[0]+40,p[1]), color=(0,150,0) )
        #if hasattr(self, '_direction_checked'):         
        #    self.__text( frame, "Dir Chk: %s" % str(self._direction_checked),(p[0]+40,p[1]), color=(0,150,0) )
        


        cv2.line(frame,self._centroid,self._head,(255,0,255),2, lineType=cv2.LINE_AA)
        
        
        if hasattr(self, '_vel_vector') and self._vel_vector[0]!=None:
            p1 = self._centroid
            p2 = self._centroid[0]+self._vel_vector[0], self._centroid[1]+self._vel_vector[1] 
            cv2.line(frame,p1,p2,(255,255,255),4, lineType=cv2.LINE_AA)
        
            


    def draw(self, frame, color=(255,255,0), thickness=2): 
        if thickness>0:  cv2.polylines(frame, np.array( [self._contour] ), True, color, thickness)
        else: cv2.fillPoly(frame, np.array( [self._contour] ), color)

        if hasattr(self, '_head'): cv2.circle( frame, self._head, 3, (100, 0,255), -1 )
        if hasattr(self, '_tail'): cv2.circle( frame, self._tail, 3, (100, 0,255), -1 )

    def distanceTo(self, blob):
        p0 = self._centroid
        p1 = blob._centroid
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

    def angleBetween(self, previous_blob, next_blob):
        if isinstance( previous_blob, tuple ) and isinstance( next_blob, tuple ):
            pt0, pt1, pt2 = previous_blob, self._centroid, next_blob
        else:
            pt0, pt1, pt2 = previous_blob._centroid, self._centroid, next_blob._centroid
        dx1 = pt0[0] - pt1[0]
        dy1 = pt0[1] - pt1[1]
        dx2 = pt2[0] - pt1[0]
        dy2 = pt2[1] - pt1[1]
        nom = dx1*dx2 + dy1*dy2
        denom = math.sqrt( (dx1*dx1 + dy1*dy1) * (dx2*dx2 + dy2*dy2) + 1e-10 )
        ang = nom / denom
        return math.degrees( math.acos(ang) )

    def cutBlob(self, image):
        (x,y),(xx,yy) = self._bounding
        return (x,y), image[y:yy,x:xx]

    def translateBlob( self, pos ):
        self._contour = np.array( [   [ p[0][0]+pos[0], p[0][1]+pos[1] ] for p in self._contour ], dtype=np.int32 )
        (x,y),(xx,yy) = self._bounding; self._bounding = (x+pos[0], y+pos[1]), (xx+pos[0], yy+pos[1])
        self._centroid = self._centroid[0]+pos[0], self._centroid[1]+pos[1]
        if hasattr( self, '_head' ): self._head = self._head[0]+pos[0], self._head[1]+pos[1]
        if hasattr( self, '_tail' ): self._tail = self._tail[0]+pos[0], self._tail[1]+pos[1]

    def flip(self):
        #Flip the blob to correct the detection
        if hasattr( self, '_head' ) and hasattr( self, '_tail' ) : 
            tmp = self._tail
            self._tail = self._head
            self._head = tmp
        
        if hasattr( self, '_rotated_image' ): self._rotated_image = tools.rotate_image(self._rotated_image, 180 )
        if hasattr( self, '_rotated_oimage' ): self._rotated_oimage = tools.rotate_image(self._rotated_oimage, 180 )
        if hasattr( self, '_rotated_image_mask' ): self._rotated_image_mask = tools.rotate_image(self._rotated_image_mask, 180 )
        



    @property
    def roi(self):
        x, y, w, h = cv2.boundingRect(self._contour)
        return x, y, x+w, y+h

    @property
    def angle_radians(self): return tools.points_angle( self._tail, self._head )

    @property
    def angle_degrees(self): return math.degrees( self.angle_radians )

