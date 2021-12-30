import turtle
import math
import time
# global constants for window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


def init():
    turtle.tracer(0, 0)
    turtle.setworldcoordinates(-WINDOW_WIDTH / 2, -WINDOW_HEIGHT / 2,
                               WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    turtle.up()
    turtle.setx(-300)


def draw_maze(solution):
    init()
    draw_squares(solution)


def draw_squares(maze):
    side = 500 / len(maze)
    for row in maze:
        for item in row:
            draw_square(item, side)
        turtle.up()
        turtle.right(90)
        turtle.forward(side)
        turtle.left(90)
        turtle.backward(len(row) * side)
    turtle.left(90)
    turtle.forward(len(maze) * side)
    turtle.mainloop()


def draw_square(item, side):
    turtle.down()
    if item == "1":
        turtle.fillcolor("#666666")
    elif item == "X":
        turtle.fillcolor("#66ffee")
    elif item == "0":
        turtle.fillcolor("white")
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(side)
        turtle.right(90)
    turtle.end_fill()
    turtle.up()
    turtle.forward(side)
