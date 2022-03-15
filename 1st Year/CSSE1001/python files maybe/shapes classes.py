import math

class Shape(object):
    """An abstract definition of any shape."""
    def area(self):
        """(float) Return the area of this shape."""
        raise NotImplementedError()

    def perimeter(self):
        """(float) Return the perimeter of this shape."""
        raise NotImplementedError()

    def draw(self):
        """Draw this shape object using turtle graphics."""
        pass

    def __str__(self):
        return "an abstract shape"

    def __repr__(self):
        return "Shape()"


class Circle(Shape):
    def __init__(self, radius):
        """
        Parameters:
            radius (float): Radius of this Circle.
        """
        self._radius = radius

    def area(self):
        return math.pi * self._radius**2

    def perimeter(self):
        return 2 * math.pi * self._radius

    def __str__(self):
        return "Circle of {0:.1f} radius".format(self._radius)

    def __repr__(self):
        return "Circle({0:.1f})".format(self._radius)

class Rectangle(Shape):
    def __init__(self, height, width):
        """Parameters:
                height (float): Size of y dimension of this Rectangle.
                width (float): Size of x dimension of this Rectangle.
        """
        self._height = height
        self._width = width

    def area(self):
        return self._height * self._width
 
    def perimeter(self):
        return 2 * self._height + 2 * self._width

    def __str__(self):
        return "rectangle of {0:.1f} by {1:.1f}".format(self._height, self._width)

    def __repr__(self):
        return "Rectangle({0:.1f} {1:.1f})".format(self._height, self._width)


def demo():
    shape1 = Shape()
    circle1 = Circle(3)
    circle2 = Circle(4.4)
    rect1 = Rectangle(5,10)
    rect2 = Rectangle(3.3, 5.5)
    tri1 = Triangle(1,2,3)

    print("\nDisplay each object via polymorphic list:")
    shapes = [circle1, circle2, rect1, rect2, tri1]
    for shape in shapes:
        print("\t{0} is a {1} with a".format(repr(shape), shape))
        print("\t\tperimeter of {0:.2f} and an area of {1:.2f}"
              .format(shape.perimeter(), shape.area()))

if __name__ == "__main__":
    demo()
