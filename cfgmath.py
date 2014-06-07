import math

class Vec:
    def __init__(self, x=0, y=None, z=None):
        if (y and z) is None:
            self.x, self.y, self.z, = (x, x, x)
        else:
            self.x, self.y, self.z, = (x, y, z)

    def str(self):
        return "{0} {1} {2}".format(self.x, self.y, self.z)

    def __add__(self, other):
        v = Vec()
        if type(other) is vec:
            v.x = self.x + other.x
            v.y = self.y + other.y
            v.z = self.z + other.z
        elif type(other) is int:
            v.x = self.x + other
            v.y = self.y + other
            v.z = self.z + other
        return v

    def __sub__(self, other):
        v = Vec()
        if type(other) is vec:
            v.x = self.x - other.x
            v.y = self.y - other.y
            v.z = self.z - other.z
        elif type(other) is int:
            v.x = self.x - other
            v.y = self.y - other
            v.z = self.z - other
        return v

    def __mul__(self, other):
        v = Vec()
        if type(other) is vec:
            v.x = self.x * other.x
            v.y = self.y * other.y
            v.z = self.z * other.z
        elif type(other) is int:
            v.x = self.x * other
            v.y = self.y * other
            v.z = self.z * other
        return v

    def __div__(self, other):
        v = Vec()
        if type(other) is vec:
            v.x = self.x / other.x
            v.y = self.y / other.y
            v.z = self.z / other.z
        elif type(other) is int:
            v.x = self.x / other
            v.y = self.y / other
            v.z = self.z / other
        return v

    def __truediv__(self, other):
        return self.__div__(other)

    def rotate(self, origin, axis, angle):
        angle = math.radians(angle)
        if (axis == 'x'):
            x = self.x
            y = ((self.y - origin.y) * math.cos(angle)) - ((origin.z - self.z) * math.sin(angle)) + origin.y
            z = ((self.z - origin.z) * math.cos(angle)) + ((origin.y - self.y) * math.sin(angle)) + origin.z
        elif (axis == 'y'):
            x = ((self.x - origin.x) * math.cos(angle)) - ((origin.z - self.z) * math.sin(angle)) + origin.x
            y = self.y
            z = ((self.z - origin.z) * math.cos(angle)) + ((origin.x - self.x) * math.sin(angle)) + origin.z
        elif (axis == 'z'):
            x = ((self.x - origin.x) * math.cos(angle)) - ((origin.y - self.y) * math.sin(angle)) + origin.x
            y = ((self.y - origin.y) * math.cos(angle)) + ((origin.x - self.x) * math.sin(angle)) + origin.y
            z = self.z

        self.x = x
        self.y = y
        self.z = z
        return self

    def magnitude(self):
        mag = math.sqrt(pow(self.x,2) + pow(self.y,2) + pow(self.z,2))
        return mag

    def normalize(self):
        nvec = Vec()

        mag = self.magnitude()

        nvec.x = self.x/mag
        nvec.x = self.y/mag
        nvec.x = self.z/mag

        return nvec
