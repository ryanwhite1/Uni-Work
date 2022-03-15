import turtle

def koch_curve(depth, length):
    """Draw a Koch Curve.

    Parameters:
        depth (int): Depth of recursion.
        length (int): Length of line.
    """
    if depth == 0:
        turtle.forward(length)
    else:
        koch_curve(depth - 1, length // 3)
        turtle.right(60)
        koch_curve(depth - 1, length // 3)
        turtle.left(120)
        koch_curve(depth - 1, length // 3)
        turtle.right(60)
        koch_curve(depth - 1, length // 3)

def koch_snowflake(depth, length):
    """Draw a Koch Curve.

    Parameters:
        depth (int): Depth of recursion.
        length (int): Length of line.
    """
    turtle.reset()
    turtle.up()
    turtle.goto(-(length/2), -(length/3))
    turtle.down()
    koch_curve(depth, length)
    turtle.left(120)
    koch_curve(depth, length)
    turtle.left(120)
    koch_curve(depth, length)
    turtle.left(120)
    

def level1_koch_curve(length):
    turtle.reset()
    turtle.forward(length//3)
    turtle.right(60)
    turtle.forward(length//3)
    turtle.left(120)
    turtle.forward(length//3)
    turtle.right(60)
    turtle.forward(length//3)
