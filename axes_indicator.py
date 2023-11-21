from typing import Tuple
import pygame
from transforms import *

class AxesIndicator:
    def __init__(self, angles: Tuple, center: Tuple[int], line_size:int) -> None:
        self.angle_x, self.angle_y, self.angle_z = angles
        self.center = center
        self.line_size = line_size
    
    def update(self, new_angles):
        self.angle_x, self.angle_y, self.angle_z = new_angles

    def draw(self, screen: pygame.Surface):
        projection_matrix = np.array(([1, 0, 0, 0], [0, 1, 0, 0]))
        add_center_matrix = np.array(([self.center[0], self.center[1]], 
                                      [self.center[0], self.center[1]], 
                                      [self.center[0], self.center[1]],
                                      [self.center[0], self.center[1]]))
        
        projected_rotation = projection_matrix @ rotation_x(self.angle_x) @ rotation_y(self.angle_y) @ rotation_z(self.angle_z)
        transposed_rotation = (projected_rotation * self.line_size).transpose()
        lines_end_positions = (transposed_rotation + add_center_matrix).tolist()

        pygame.draw.line(screen, "red", self.center, lines_end_positions[0], 2)
        pygame.draw.line(screen, "green", self.center, lines_end_positions[1], 2)
        pygame.draw.line(screen, "blue", self.center, lines_end_positions[2], 2)