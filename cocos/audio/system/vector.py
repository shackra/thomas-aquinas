"""
Binding for the CSFML Vector2x structures.
"""

##########################################################################################
#============================== standard library imports ================================#
##########################################################################################

import ctypes


##########################################################################################
#=================================== Vector2x base ======================================#
##########################################################################################

class _Vector2(ctypes.Structure):
    """
    Base class for Vector2x classes.
    """

    #: The x component of the Vector2
    x = 0

    #: The y component of the Vector2
    y = 0

    def __add__(self, other):
        """
        Returns a new Vector2 instance containing the result of the addition between the
        current Vector2 and the given Vector2 instance.

        :param other: The Vector2 instance to add.

        :rtype: _Vector2
        :return: A Vector2 containing the result of the addition.
        """
        return type(self)(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        """
        Adds the given Vector2 to the current Vector2 in-place.
        """
        self.x += other.x
        self.y += other.y

        return self

    def __div__(self, x):
        """
        Returns a new Vector2 instance containing the result of the division between the
        current Vector2 and the given value.

        :param x: The value to divide by.

        :rtype: _Vector2
        :return: A Vector2 containing the result of the division.
        """
        return type(self)(self.x / x, self.y / x)

    def __idiv__(self, x):
        """
        Divides the current Vector2 instance by x in-place.

        :param x: The value to divide by.

        :rtype: _Vector2
        """
        self.x /= x
        self.y /= x

        return self

    def __eq__(self, other):
        """
        Compares a given Vector2 instance with the current instance and returns if they are
        equal.

        :param other: A Vector2 instance to compare with.

        :return: Whether the Vector2s are equal.
        """
        return self.x == other.x and self.y == other.y

    def __mul__(self, x):
        """
        Returns a Vector2 containing the result of the current Vector2 multiplied by x.

        :param x: The value to multiply the Vector2 by.

        :rtype: _Vector2
        """
        return type(self)(self.x * x, self.y * x)

    def __imul__(self, x):
        """
        Multiplies the current Vector2 instance by x in-place.

        :param x: The value to multiply the Vector2 by.

        :rtype: _Vector2
        """
        self.x *= x
        self.y *= x

        return self

    def __ne__(self, other):
        """
        Returns whether the given Vector2 is not equal to the current instance.

        :return: true if the given Vector2 was not equal.
        """
        return self.x != other.x or self.y != other.y

    def __neg__(self):
        """
        Returns the negative of the current Vector2 instance.

        :rtype: _Vector2
        :return: The negated Vector2.
        """
        return type(self)(-self.x, -self.y)

    def __sub__(self, other):
        """
        Returns a new Vector2 instance containing the result of the subtraction between
        the current Vector2 and the given Vector2 instance.

        :param other: The Vector2 instance to subtract.

        :rtype: _Vector2
        :return: A Vector2 containing the result of the subtraction.
        """
        return type(self)(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        """
        Subtracts the given Vector2 from the current Vector2 in-place.
        """
        self.x -= other.x
        self.y -= other.y

        return self


##########################################################################################
#================================== Vector2f struct =====================================#
##########################################################################################

class Vector2f(_Vector2):
    """
    Utility class for manipulating 2-dimensional vectors with float components.
    """

    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float)
    ]

    def __init__(self, x=0, y=0):
        """
        Initialise a new Vector2f structure instance.

        :param x: The x co-ordinate of the vector2f.
        :param y: The y co-ordinate of the vector2f.
        """
        super(Vector2f, self).__init__(x, y)

        #: The x co-ordinate of the Vector2f.
        self.x = x

        #: The y co-ordinate of the Vector2f.
        self.y = y

    def __repr__(self):
        """
        Friendly representing of a Vector2f object.
        """
        return "<Vector2f({}, {})>".format(self.x, self.y)


##########################################################################################
#================================== Vector2i struct =====================================#
##########################################################################################

class Vector2i(_Vector2):
    """
    Utility class for manipulating 2-dimensional vectors with integer components.
    """

    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int)
    ]

    def __init__(self, x=0, y=0):
        """
        Initialise a new Vector2i structure instance.

        :param x: The x co-ordinate of the vector2i.
        :param y: The y co-ordinate of the vector2i.
        """
        super(Vector2i, self).__init__(x, y)

        #: The x co-ordinate of the Vector2i.
        self.x = x

        #: The y co-ordinate of the Vector2i.
        self.y = y

    def __repr__(self):
        """
        Friendly representing of a Vector2i object.
        """
        return "<Vector2i({}, {})>".format(self.x, self.y)


##########################################################################################
#================================== Vector2u struct =====================================#
##########################################################################################

class Vector2u(_Vector2):
    """
    Utility class for manipulating 2-dimensional vectors with unsigned integer components.
    """

    _fields_ = [
        ("x", ctypes.c_uint),
        ("y", ctypes.c_uint)
    ]

    def __init__(self, x=0, y=0):
        """
        Initialise a new Vector2u structure instance.

        :param x: The x co-ordinate of the Vector2u.
        :param y: The y co-ordinate of the Vector2u.
        """
        super(Vector2u, self).__init__(x, y)

        #: The x co-ordinate of the Vector2u.
        self.x = x

        #: The y co-ordinate of the Vector2u.
        self.y = y

    def __repr__(self):
        """
        Friendly representing of a Vector2uobject.
        """
        return "<Vector2u({}, {})>".format(self.x, self.y)


##########################################################################################
#=================================== Vector3x base ======================================#
##########################################################################################

class _Vector3(ctypes.Structure):
    """
    Base class for Vector3x structures.
    """

    #: The x component of the Vector3
    x = 0

    #: The y component of the Vector3
    y = 0

    #: The z component of the Vector3
    z = 0

    def __add__(self, other):
        """
        Returns a new Vector3 instance containing the result of the addition between the
        current Vector3 and the given Vector3 instance.

        :param other: The Vector3 instance to add.

        :rtype: _Vector3
        :return: A Vector3 containing the result of the addition.
        """
        return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        """
        Adds the given Vector3 to the current Vector3 in-place.
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def __div__(self, x):
        """
        Returns a new Vector3 instance containing the result of the division between the
        current Vector3 and the given value.

        :param x: The value to divide by.

        :rtype: _Vector3
        :return: A Vector3 containing the result of the division.
        """
        return type(self)(self.x / x, self.y / x, self.z / x)

    def __idiv__(self, x):
        """
        Divides the current Vector3 instance by x in-place.

        :param x: The value to divide by.

        :rtype: _Vector3
        """
        self.x /= x
        self.y /= x
        self.z /= x

        return self

    def __eq__(self, other):
        """
        Compares a given Vector3 instance with the current instance and returns if they are
        equal.

        :param other: A Vector3 instance to compare with.

        :return: Whether the Vector3s are equal.
        """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __mul__(self, x):
        """
        Returns a Vector3 containing the result of the current Vector3 multiplied by x.

        :param x: The value to multiply the Vector3 by.

        :rtype: _Vector3
        """
        return type(self)(self.x * x, self.y * x, self.z * x)

    def __imul__(self, x):
        """
        Multiplies the current Vector3 instance by x in-place.

        :param x: The value to multiply the Vector3 by.

        :rtype: _Vector3
        """
        self.x *= x
        self.y *= x
        self.z *= x

        return self

    def __ne__(self, other):
        """
        Returns whether the given Vector3 is not equal to the current instance.

        :return: true if the given Vector3 was not equal.
        """
        return self.x != other.x or self.y != other.y or self.z != other.z

    def __neg__(self):
        """
        Returns the negative of the current Vector3 instance.

        :rtype: _Vector3
        :return: The negated Vector3.
        """
        return type(self)(-self.x, -self.y, -self.z)

    def __sub__(self, other):
        """
        Returns a new Vector3 instance containing the result of the subtraction between
        the current Vector3 and the given Vector3 instance.

        :param other: The Vector3 instance to subtract.

        :rtype: _Vector3
        :return: A Vector3 containing the result of the subtraction.
        """
        return type(self)(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other):
        """
        Subtracts the given Vector3 from the current Vector2 in-place.
        """
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

        return self

##########################################################################################
#================================== Vector3f struct =====================================#
##########################################################################################

class Vector3f(_Vector3):
    """
    Utility class for manipulating 3-dimensional vectors with float components.
    """

    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float)
    ]

    def __repr__(self):
        """
        Friendly representing of a Vector3f object.
        """
        return "<Vector3f({}, {})>".format(self.x, self.y)


##########################################################################################
