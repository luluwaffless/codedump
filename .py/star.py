import turtle
n = 50
scale = 400/n
turtle.speed(0)
turtle.hideturtle()
def draw_line(p1, p2):
    turtle.penup()
    turtle.goto(p1[0]*scale, p1[1]*scale)
    turtle.pendown()
    turtle.goto(p2[0]*scale, p2[1]*scale)
for i in range(n):
    draw_line((-n + i, 0), (0, 1 + i))
    draw_line((-n + i, 0), (0, -1 - i))
    draw_line((0, n - i), (1 + i, 0))
    draw_line((0, -n + i), (1 + i, 0))
draw_line((-n, 0), (n, 0))  # X axis
draw_line((0, -n), (0, n))  # Y axis
turtle.done()