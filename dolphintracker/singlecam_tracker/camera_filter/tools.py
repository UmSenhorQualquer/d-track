import cv2, math
from numpy import *

#def lin_dist(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)


def lin_dist( p1, p2 ):   return linalg.norm( (p1[0]-p2[0], p1[1]-p2[1]) )

def points_angle(p1, p2): 
    x1, y1 = p1
    x2, y2 = p2
    rads = math.atan2(-(y2-y1),x2-x1)
    rads %= 2*pi
    return rads

def min_dist_angles(ang1, ang2):
    tmp = max(ang1, ang2)
    ang2 = min(ang1, ang2)
    ang1 = tmp
    angle1 = abs(ang1-ang2)
    angle2 = abs(ang1-(pi*2)-ang2)
    #return min(angle1, angle2)
    angle3 = abs(ang1+(pi*2)-ang2)
    return min(angle1, angle2, angle3)
    #if angle1>pi: return 2*pi - angle1
    #return angle1

def getTranslationMatrix2d(dx, dy):
    """
    Returns a numpy affine transformation matrix for a 2D translation of
    (dx, dy)
    """
    return matrix([[1, 0, dx], [0, 1, dy], [0, 0, 1]])

def rotate_image(image, angle):
    """
    Rotates the given image about it's centre
    """

    image_size = (image.shape[1], image.shape[0])
    image_center = tuple(array(image_size) / 2)

    rot_mat = vstack([cv2.getRotationMatrix2D(image_center, angle, 1.0), [0, 0, 1]])
    trans_mat = identity(3)

    w2 = image_size[0] * 0.5
    h2 = image_size[1] * 0.5

    rot_mat_notranslate = matrix(rot_mat[0:2, 0:2])

    tl = (array([-w2, h2]) * rot_mat_notranslate).A[0]
    tr = (array([w2, h2]) * rot_mat_notranslate).A[0]
    bl = (array([-w2, -h2]) * rot_mat_notranslate).A[0]
    br = (array([w2, -h2]) * rot_mat_notranslate).A[0]

    x_coords = [pt[0] for pt in [tl, tr, bl, br]]
    x_pos = [x for x in x_coords if x > 0]
    x_neg = [x for x in x_coords if x < 0]

    y_coords = [pt[1] for pt in [tl, tr, bl, br]]
    y_pos = [y for y in y_coords if y > 0]
    y_neg = [y for y in y_coords if y < 0]

    right_bound = max(x_pos)
    left_bound = min(x_neg)
    top_bound = max(y_pos)
    bot_bound = min(y_neg)

    new_w = int(abs(right_bound - left_bound))
    new_h = int(abs(top_bound - bot_bound))
    new_image_size = (new_w, new_h)

    new_midx = new_w * 0.5
    new_midy = new_h * 0.5

    dx = int(new_midx - w2)
    dy = int(new_midy - h2)

    trans_mat = getTranslationMatrix2d(dx, dy)
    affine_mat = (matrix(trans_mat) * matrix(rot_mat))[0:2, :]
    result = cv2.warpAffine(image, affine_mat, new_image_size, flags=cv2.INTER_LINEAR)

    return result



def rotate_poly(pts,cnt,ang=pi/4):
    '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
    result = array( dot(pts-cnt,array([[cos(ang),sin(ang)],[-sin(ang),cos(ang)]]))+cnt, dtype=int32 )
    return result









def groupImagesHorizontally( images, color=False ):
    final_width, final_height = sum([ x.shape[1] for x in images ]), max([ x.shape[0] for x in images ])
    if color:
        final_image = zeros( (final_height, final_width, 3), dtype=uint8 )
    else:
        final_image = zeros( (final_height, final_width), dtype=uint8 )
    cursor = 0
    for image in images:
        final_image[0:image.shape[0],cursor:cursor+image.shape[1]] = image
        cursor += image.shape[1]
    return final_image


def groupImagesVertically( images, color=False ):
    final_width, final_height = max([ x.shape[1] for x in images ]), sum([ x.shape[0] for x in images ])
    if color:
        final_image = zeros( (final_height, final_width, 3), dtype=uint8 )
    else:
        final_image = zeros( (final_height, final_width), dtype=uint8 )
    cursor = 0
    for image in images:
        final_image[cursor:cursor+image.shape[0],0:image.shape[1]] = image
        cursor += image.shape[0]
    return final_image

def groupImage( images,color=False ):
    himages = []
    for group in images:
        if isinstance(group, list):
            himages.append( groupImagesVertically(group,color) )
        else:
            himages.append( group )

    return groupImagesHorizontally(himages,color)



def biggestContour(contours, howmany=1):
    biggest = []
    for blob in contours:
        area = cv2.contourArea(blob)
        biggest.append( (area, blob) )
    if len(biggest)==0: return None
    biggest = sorted( biggest, key=lambda x: -x[0])
    if howmany==1: return biggest[0][1]
    return [x[1] for x in biggest[:howmany] ]

def getBiggestContour(image, howmany=1):
    (_, blobs, dummy) = cv2.findContours( image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    return biggestContour(blobs, howmany)





def smooth(x,beta, window_len=32):
    """ kaiser window smoothing """
    # extending the data at beginning and at the end
    # to apply the window at the borders
    s = r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    w = kaiser(window_len,beta)
    y = convolve(w/w.sum(),s,mode='valid')
    return y[5:len(y)-5]


def smoothContours( positions, window_len=32,s=2 ):
    one_xs = array([ x[0][0] for x in positions])
    one_ys = array([ x[0][1] for x in positions])
    one_xs = smooth(one_xs, s, window_len)
    one_ys = smooth(one_ys, s, window_len)
    return [ [( int(math.ceil( one_xs[i])) ,  int(math.ceil( one_ys[i])) )] for i in range(len(one_xs))]


def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b





def circlesIntersection(point_a, point_b, ac_length, bc_length):
    ab_length = lin_dist(point_b, point_a)
    if ab_length > (ac_length + bc_length): raise Exception("Given points do not intersect!")    
    elif ab_length < abs(ac_length - bc_length): raise Exception("The circle of the points do not intersect")    
    ad_length = (ab_length**2 + ac_length**2 - bc_length**2)/(2.0 * ab_length)    
    h  = sqrt(abs(ac_length**2 - ad_length**2))
    d_x = point_a[0] + ad_length * (point_b[0] - point_a[0])/ab_length
    d_y = point_a[1] + ad_length * (point_b[1] - point_a[1])/ab_length
    point_d = (d_x, d_y)    
    c_x1 = point_d[0] + h * (point_b[1] - point_a[1])/ab_length
    c_x2 = point_d[0] - h * (point_b[1] - point_a[1])/ab_length
    c_y1 = point_d[1] - h * (point_b[0] - point_a[0])/ab_length
    c_y2 = point_d[1] + h * (point_b[0] - point_a[0])/ab_length    

    point_c1 = (c_x1, c_y1)
    point_c2 = (c_x2, c_y2)    
    return point_c1, point_c2 

def linesIntersection(p1, p2, p3, p4):
    x1 = p1[0]
    x2 = p2[0]
    x3 = p3[0]
    x4 = p4[0]
    y1 = p1[1]
    y2 = p2[1]
    y3 = p3[1]
    y4 = p4[1]
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if d == 0: return None
    pre = (x1*y2 - y1*x2)
    post = (x3*y4 - y3*x4)
    x = ( pre * (x3 - x4) - (x1 - x2) * post ) / d;
    y = ( pre * (y3 - y4) - (y1 - y2) * post ) / d;
    if ( x < min(x1, x2) or x > max(x1, x2) or x < min(x3, x4) or x > max(x3, x4) ): return None;
    if ( y < min(y1, y2) or y > max(y1, y2) or y < min(y3, y4) or y > max(y3, y4) ): return None;
     
    return (x,y)

def closestPoint2Line(p, p1,p2):
    d1 = lin_dist(p,p1)
    d2 = lin_dist(p,p2)
    _p1, _p2 = circlesIntersection(p1, p2, d1, d2)
    res = linesIntersection(_p1,_p2,p1,p2)
    if res==None: return res
    return int(res[0]),int(res[1])



def splitImage(img):
    contour = getBiggestContour(img)
    hull = cv2.convexHull(contour,returnPoints= False)
    defects = cv2.convexityDefects(contour,hull)

    defects_with_dist = []
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])
        closest_p = closestPoint2Line(far,start,end)
        if closest_p==None: continue
        dist = lin_dist(closest_p, far)
        defects_with_dist.append( (dist,closest_p,far) )
     
    defects_with_dist = sorted(defects_with_dist, key=lambda x: -x[0])
    if len(defects_with_dist)>0:
        d, closest_p, far = defects_with_dist[0]
        cut_points = [far]
        if len(defects_with_dist)>1:
            d1, closest_p1,far1 = defects_with_dist[1]
            if lin_dist(far,far1)<=50: cut_points.append(far1)
        if len(cut_points)<2: 
            vector = array(far)-array(closest_p)
            p = far[0]+30*vector[0], far[1]+30*vector[1]
            cut_points.append(p)

        cv2.line( img, cut_points[0], cut_points[1], 0, 2)

    return getBiggestContour( img, 2 )

        #cv2.circle(img,cut_points[0],7,[200,0,255],-1)
        #cv2.circle(img,cut_points[1],7,[200,0,255],-1)   
    #cv2.imshow("distanceTransform", img)
    #cv2.imshow("blob._rotated_image_mask", blob._rotated_image_mask)



def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]


def combinations( l1, l2 ):
    """
    Make combinations between the 2 lists without repeating
    """
    for i in range(len(l1)):
        yield zip( l1,l2)
        l1.insert(0,l1.pop())