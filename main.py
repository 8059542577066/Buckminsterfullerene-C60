from jmol import *
from geometry import *  # in order to use glFunctions without GL. prefix

import pygame
from pygame.locals import *


# Starting Constants.
VERTICES = tuple(c60_atoms)

EYE_POS = (0, 0, 30)
CENTER = (0, 0, 0)
UP_VEC = (0, 1, 0)


def c60(vertices, edges, eye_pos):
    radius = 0.4
    o1 = [Sphere(vertex, radius) for vertex in vertices]
    o2 = [Line(vertices[edge[0]], vertices[edge[1]], radius) for edge in edges]
    objects = o1 + o2
    for object in sorted(objects,
                         key = lambda obj: obj.distanceSquared(eye_pos),
                         reverse = True):
        object.draw()

def draw(vertices, edges, eye_pos):
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    c60(vertices, edges, eye_pos)
    pygame.display.flip()
    pygame.time.wait(5)

def lookAtCenter(eye_pos, center, up_vec):
    glLoadIdentity()
    gluLookAt(eye_pos[0], eye_pos[1], eye_pos[2],
              center[0], center[1], center[2],
              up_vec[0], up_vec[1], up_vec[2])

def reset():
    return list(VERTICES), list(EYE_POS), list(CENTER), list(UP_VEC)


def main():
    # Molecule coordinates & bonds loading.
    vertices = VERTICES
    edges = tuple(c60_bonds)

    # pygame window setup.
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    display = (800, 800)
    pygame.display.set_caption("Buckminsterfullerene C60")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Perspective setup.
    glMatrixMode(GL_PROJECTION)
    gluPerspective(20, float(display[0]) / display[1], 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)

    # Lighting.
    gl_position = (-5, 5, -10, 0)
    gl_spot_direction = (0, 0, 0, 0)
    gl_ambient = (0, 0, 0, 1.0)
    gl_diffuse = (1.0, 1.0, 1.0, 1.0)

    glLight(GL_LIGHT0, GL_POSITION, gl_position)
    glLight(GL_LIGHT0, GL_SPOT_DIRECTION, gl_spot_direction)
    glLight(GL_LIGHT0, GL_AMBIENT, gl_ambient)
    glLight(GL_LIGHT0, GL_DIFFUSE, gl_diffuse)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    # Camera Setting.
    eye_pos = list(EYE_POS)
    center = list(CENTER)
    up_vec = list(UP_VEC)

    lookAtCenter(eye_pos, center, up_vec)
    dragging = False
    scrolling = False

    while True:
        draw(vertices, edges, eye_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    vertices, eye_pos, center, up_vec = reset()
                    lookAtCenter(eye_pos, center, up_vec)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # if left mouse button is clicked.
                    dragging = True
                    start_x, start_y = event.pos
                elif event.button == 2:  # Clicking mouse wheel
                    scrolling = True
                    start_x, start_y = event.pos
                elif event.button == 4:  # pushing wheel away
                    if eye_pos[2] > 1:
                        eye_pos[2] -= 1
                    lookAtCenter(eye_pos, center, up_vec)
                elif event.button == 5:  # pulling wheel
                    if eye_pos[2] < 120:
                        eye_pos[2] += 1
                    lookAtCenter(eye_pos, center, up_vec)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # if left mouse button is lifted.
                    dragging = False
                elif event.button == 2:  # if mouse wheel is lifted.
                    scrolling = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = event.pos
                    delta_x = float(mouse_x - start_x) / 300
                    delta_y = float(mouse_y - start_y) / 300
                    vertices = rotateAtomsByMouseXY(vertices, delta_x, delta_y)
                    start_x, start_y = mouse_x, mouse_y
                elif scrolling:
                    mouse_x, mouse_y = event.pos
                    delta_x = float(mouse_x - start_x) / 300
                    vertices = rotateAtomsByScrollX(vertices, -delta_x)
                    start_x = mouse_x


if __name__ == "__main__":
    main()
