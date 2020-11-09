#Class to represent a Room object
class Room:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        print("-> Room generated with dimensions x: {0}, y: {1}, z: {2}".format(x, y, z))