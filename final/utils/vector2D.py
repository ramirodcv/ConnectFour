# basic cartesian coordinate 2D vector
class Vector2D(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # set self values
    def set(self, x=0, y=0):
        self.x = x
        self.y = y
        return self

    # add other to self values
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    # add self to other and return a new Vector2D containing the result
    def __add__(self, other):
        return Vector2D(x=(self.x + other.x), y=(self.y + other.y))

    # subtract other from self and return a new Vector2D with the result
    def __sub__(self, other):
        return Vector2D(x=(self.x - other.x), y=(self.y - other.y))

    # set this Vector2D to an other Vector2D
    def __eq__(self, other):
        self.x = other.x
        self.y = other.y
        return self

    # return this Vector2D's str representation
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    # scale this Vector2D
    def scale(self, scale):
        return Vector2D(self.x * scale, self.y * scale)
