import csv,cv2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from py3dengine.cameras.Ray import Ray
from py3dengine.bin.RunScene import RunScene
import numpy as np
from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
from py3dengine.scenes.GLScene import GLScene


class RenderPositions(RunScene):

    def __init__(self, scenefilename, filename,
        camera0video,
        camera1video,
        videowriter=None):

        w = WavefrontOBJReader(scenefilename)
        scene = GLScene()
        scene.objects = w.objects
        scene.cameras = w.cameras

        super(RenderPositions, self).__init__(scene, videowriter)
        self._filename = filename



        

        self._camera0video = camera0video
        self._camera1video = camera1video

        self._rotation = [-60.29999999999993, 0, -110.70000000000022]
        self._position = [12.899999999999972, -3.100000000000002]
        self._zoom = 26


    def loadData(self):
        self._frames  = []
        self._positions = []
        self._points = []
        self._pixels0 = []
        self._pixels1 = []
        self._count = 0

        
        self._camera0   = self._scene.getCamera('Camera1')
        self._camera1   = self._scene.getCamera('Camera2')
        self._floor     = self._scene.getObject('Floor')
        #self._floor.refraction = 1.641476
        self._floor.refraction = 1.4

        handler     = open(self._filename, 'r')
        spamreader  = csv.reader(handler, delimiter=';', quotechar='|')

        for row in spamreader:
            self._frames.append( float(row[0]) )
            pos = float(row[1]), float(row[2]), float(row[3])
            pixel0 = float(row[4]), float(row[5])
            pixel1 = float(row[7]), float(row[8])
            self._points.append(pos)
            self._pixels0.append(pixel0)
            self._pixels1.append(pixel1)
            

        self._video0 = cv2.VideoCapture(self._camera0video)
        self._video1 = cv2.VideoCapture(self._camera1video)
        self._video0.set(1, self._frames[0])
        self._video1.set(1, self._frames[0])


    def process(self, scene):
        if self._count>=len(self._frames): 
            print("exit")
            exit()

        if (self._count % 1000)==0: print( self._count)

        self._camera0.cleanRays()
        self._camera1.cleanRays()

        frame  = self._frames[self._count]
        pixel0 = self._pixels0[self._count]
        pixel1 = self._pixels1[self._count]
        point = self._points[self._count]

        ray0 = self._camera0.addRay(pixel0[0], pixel0[1], z=30, color=(0,1.0,0) )
        ray1 = self._camera1.addRay(pixel1[0], pixel1[1], z=30, color=(0,1.0,0))

        ray0.collide( [self._floor] )
        ray1.collide( [self._floor] )

        self._drawPoint(point, w=0.2)

        self._positions.append(point)
        if len(self._positions)>100: self._positions.pop(0)


        self._count += 1



    def drawData(self):
        self.process(self._scene)

        glBegin( GL_LINES );
        glColor3f(1.0,0.5,0.5)
        lastPos = None
        for pos in self._positions:
            if lastPos!=None:
                glVertex3f( *lastPos );
                glVertex3f( *pos );
            lastPos = pos
        glEnd();


        



    def readScreen(self, x, y, width, height):
        img = super(RenderPositions, self).readScreen(x, y, width, height)
        
        res, img0 = self._video0.read()
        if not res: exit()
        res, img1 = self._video1.read()
        if not res: exit()

        p = self._pixels0[self._count-1]; p = int(p[0]), int(p[1])
        cv2.circle( img0, p, 5, (0,0,255), -1 )
        p = self._pixels1[self._count-1]; p = int(p[0]), int(p[1])
        cv2.circle( img1, p, 5, (0,0,255), -1 )

        img0 = cv2.resize(img0, self._windowSize)
        img1 = cv2.resize(img1, self._windowSize)

        return np.hstack( (img0,img,img1) )
        

    def _drawPoint(self, p, color=(1.0,1.0,0.0), w=0.1 ):
        glPushMatrix()
        
        glTranslatef(*p)

        glColor3f(*color)
        
        glBegin( GL_TRIANGLES );

        glVertex3f( 0.0, w, 0.0 );
        glVertex3f( -w, -w, w );
        glVertex3f( w, -w, w);

        glVertex3f( 0.0, w, 0.0);
        glVertex3f( -w, -w, w);
        glVertex3f( 0.0, -w, -w);

        glVertex3f( 0.0, w, 0.0);
        glVertex3f( 0.0, -w, -w);
        glVertex3f( w, -w, w);

        glVertex3f( -w, -w, w);
        glVertex3f( 0.0, -w, -w);
        glVertex3f( w, -w, w);
        glEnd();

        glPopMatrix()