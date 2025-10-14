import turtle

# Function to draw a semicircle divided into n equal parts
def draw_semicircle_divided(n):
    turtle.penup()
    turtle.goto(0, 0)
    turtle.pendown()
    turtle.right(180)
    turtle.forward(200)
    turtle.backward(200)
    # Draw the divisions
    for _ in range(n):
        turtle.penup()
        turtle.goto(0, 0)
        turtle.pendown()
        turtle.right(180 / n)
        turtle.forward(200)
        turtle.backward(200)

    turtle.hideturtle()
    turtle.done()

# Draw a semicircle divided into 10 equal parts
draw_semicircle_divided(10)