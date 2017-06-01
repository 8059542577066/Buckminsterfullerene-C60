from math import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Sphere:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def distanceSquared(self, eye_pos):
        eye_x, eye_y, eye_z = eye_pos
        x, y, z = self.center
        return (x - eye_x) ** 2 + (y - eye_y) ** 2 + (z - eye_z) ** 2

    def draw(self):
        x, y, z = self.center
        quadric = gluNewQuadric()

        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor4f(0.6, 0.6, 0.6, 1.0)
        gluSphere(quadric, self.radius, 32, 32)
        glPopMatrix()


class Line:
    def __init__(self, p1, p2, radius):
        self.p1 = p1
        self.p2 = p2
        self.radius = radius

    def center(self):
        x1, y1, z1 = self.p1
        x2, y2, z2 = self.p2
        return (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2

    def distanceSquared(self, eye_pos):
        eye_x, eye_y, eye_z = eye_pos
        x, y, z = self.center()
        return (x - eye_x) ** 2 + (y - eye_y) ** 2 + (z - eye_z) ** 2

    def surfacePoints(self):
        x1, y1, z1 = self.p1
        x2, y2, z2 = self.p2
        distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        s1 = tuple([x1 + (x2 - x1) * self.radius / distance,
                    y1 + (y2 - y1) * self.radius / distance,
                    z1 + (z2 - z1) * self.radius / distance])
        s2 = tuple([x2 - (x2 - x1) * self.radius / distance,
                    y2 - (y2 - y1) * self.radius / distance,
                    z2 - (z2 - z1) * self.radius / distance])
        return s1, s2

    def draw(self):
        s1, s2 = self.surfacePoints()

        glLineWidth(2)
        glColor4f(0, 0, 0, 1)
        glBegin(GL_LINES)
        glVertex3fv(s1)
        glVertex3fv(s2)
        glEnd()


def rotateX(vertices, rad):
    rotated = []
    for x, y, z in vertices:
        rotated.append((x,
                        y * cos(rad) - z * sin(rad),
                        y * sin(rad) + z * cos(rad)))
    return tuple(rotated)

def rotateY(vertices, rad):
    rotated = []
    for x, y, z in vertices:
        rotated.append((x * cos(rad) + z * sin(rad),
                        y,
                        z * cos(rad) - x * sin(rad)))
    return tuple(rotated)

def rotateZ(vertices, rad):
    rotated = []
    for x, y, z in vertices:
        rotated.append((x * cos(rad) - y * sin(rad),
                        x * sin(rad) + y * cos(rad),
                        z))
    return tuple(rotated)

def rotateAtomsByMouseXY(vertices, radX, radY):
    return rotateX(rotateY(vertices, radX), radY)

def rotateAtomsByScrollX(vertices, rad):
    return rotateZ(vertices, rad)
