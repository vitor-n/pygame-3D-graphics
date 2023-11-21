from transforms import *
from math import tan, radians, degrees, cos, sin, sqrt
import numpy as np

class Camera:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.pos_z = 0

        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.fov = 100

        self.speed = 1


        self.update_axes()
        self.matrix = self.get_rotation() @ self.get_translation()

    def update(self):
        self.update_axes()
        self.matrix = self.get_rotation() @ self.get_translation()

    def update_axes(self):
        """
        Function to get new axes for the view space (camera).
        """
        
        lookat_vector = (rotation_y(self.angle_y) @ rotation_x(self.angle_x) @ (0,0,1,0))[0,:3]
        
        n_vector = lookat_vector
        u_vector = np.cross([0,1,0], n_vector)
        v_vector = np.cross(n_vector, u_vector)

        self.n_vector = n_vector / np.linalg.norm(n_vector)
        self.u_vector = u_vector / np.linalg.norm(u_vector)
        self.v_vector = v_vector / np.linalg.norm(v_vector)

    def get_axes(self):
        return self.u_vector, self.v_vector, self.n_vector

    def get_rotation(self):
        return (rotation_y(self.angle_y) @ rotation_x(self.angle_x)).transpose()

    def get_translation(self):
        return camera_translation((self.pos_x, self.pos_y, self.pos_z))

    def move_forwards(self):
        self.pos_x += self.n_vector[0,0] * self.speed
        self.pos_z += self.n_vector[0,2] * self.speed 
    
    def move_backwards(self):
        self.pos_x -= self.n_vector[0,0] * self.speed
        self.pos_z -= self.n_vector[0,2] * self.speed 

    def move_right(self):
        self.pos_x -= self.u_vector[0,0] * self.speed
        self.pos_z -= self.u_vector[0,2] * self.speed 

    def move_left(self):
        self.pos_x += self.u_vector[0,0] * self.speed
        self.pos_z += self.u_vector[0,2] * self.speed 

    def move_upwards(self):
        self.pos_y += self.speed

    def move_downwards(self):
        self.pos_y -= self.speed

    @property
    def angle_x(self):
        return self._angle_x

    @angle_x.setter
    def angle_x(self, new_angle_x):
        if degrees(new_angle_x) > 90:
            self._angle_x = radians(90)
        elif degrees(new_angle_x) < -90:
            self._angle_x = radians(-90)
        else: 
            self._angle_x = new_angle_x