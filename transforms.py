import numpy as np
from math import sin, cos, tan, radians, atan


def rotation_x(theta):
    r_x = np.matrix(([1,          0,          0, 0],
                     [0, cos(theta),-sin(theta), 0],
                     [0, sin(theta), cos(theta), 0],
                     [0,          0,          0, 1]))
    
    return r_x

def rotation_y(theta):
    r_x = np.matrix(([cos(theta), 0, -sin(theta), 0],
                     [         0, 1,           0, 0],
                     [sin(theta), 0,  cos(theta), 0],
                     [         0, 0,           0, 1]))
    
    return r_x 

def rotation_z(theta):
    r_x = np.matrix(([cos(theta),-sin(theta), 0, 0],
                     [sin(theta), cos(theta), 0, 0],
                     [         0,          0, 1, 0],
                     [         0,          0, 0, 1]))
    
    return r_x

def translation(tx, ty, tz):

    t_matrix = np.identity(4)

    t_matrix[0,3] = tx
    t_matrix[1,3] = ty
    t_matrix[2,3] = tz

    return t_matrix

def perspective(fov:float, aspect:float, znear:float, zfar:float):

    m = np.zeros((4,4))

    e = 1 / tan(radians(fov/2))

    m = np.matrix(([e,0,0,0],
                   [0,e,0,0],
                   [0,0,(znear)/(zfar-znear),-(zfar*znear)/(zfar-znear)],
                   [0,0,1,0]))

    test = [[aspect*e,0,0,0],
            [0,e,0,0],
            [0,0,-(zfar+znear)/(zfar-znear), -(2*zfar*znear)/(zfar-znear)],
            [0,0,-1,0]]

    return test

def camera_translation(pos):
    camera_matrix = np.matrix([[1,0,0,-pos[0]],
                               [0,1,0,-pos[1]],
                               [0,0,1,-pos[2]],
                               [0,0,0,      1]]) 
    

    return camera_matrix

def camera_orientation(u,v,n):

    orientation_matrix = np.matrix(([u[0,0], u[0,1], u[0,2], 0],
                                    [v[0,0], v[0,1], v[0,2], 0],
                                    [n[0,0], n[0,1], n[0,2], 0],
                                    [     0,      0,      0, 1])),

    return orientation_matrix

def viewport(width, height):

    view = np.matrix(([width//2, 0,0,0],
                      [0,height//2,0,0],
                      [0,0,1/2,1/2],
                      [0,0,0,1]))
    

    return view