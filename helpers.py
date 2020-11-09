import math
from numpy import sqrt, dot, cross
from numpy.linalg import norm
import numpy as np

#Return the 3-dimensional distance between two points in space
def get3DDistance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

#Generate an array of microphone positions in a grid defined by the input parameters
def generateMicArray(x, y, scale, cieling):
    micArray = []
    for a in range(0, x):
        for b in range(0, y):
            micArray.append([a*scale, b*scale, cieling])
    print("-> {0}x{1} microphone array generated with spacing of {2} at z-level {3}".format(x, y, scale, cieling))
    return micArray

#Get the unit vector betwween two points
def getUnitVector(point1, point2):
    outputVector = [0, 0, 0]
    distance = get3DDistance(point1, point2)
    for x in range(0, 3):
        outputVector[x] = (point1[x] - point2[x]) / distance
    return outputVector

#Calculate degree heading from a unit vector
def getDegreeHeading(unitVector):
    angleA = np.arccos(unitVector[0])
    angleB = np.arcsin(unitVector[2])
    return [np.degrees(angleA), np.degrees(angleB)]

# Find the intersection of three spheres where P1,P2,P3 are the centers, and r1,r2,r3 are the radii
def trilaterate(P1,P2,P3,r1,r2,r3):
    temp1 = P2-P1
    e_x = temp1/norm(temp1)
    temp2 = P3-P1
    i = dot(e_x,temp2)
    temp3 = temp2 - i*e_x
    e_y = temp3/norm(temp3)
    e_z = cross(e_x,e_y)
    d = norm(P2-P1)
    j = dot(e_y,temp2)
    x = (r1*r1 - r2*r2 + d*d) / (2*d)
    y = (r1*r1 - r3*r3 -2*i*x + i*i + j*j) / (2*j)
    temp4 = r1*r1 - x*x - y*y
    if temp4<0:
        raise Exception("The three spheres do not intersect!");
    z = sqrt(temp4)
    p_12_a = P1 + x*e_x + y*e_y + z*e_z
    p_12_b = P1 + x*e_x + y*e_y - z*e_z
    return p_12_a,p_12_b

#Determine if any points fall outside the room
def allInRoom(points, room):
    for x in points:
        if x[0] > room.x or x[1] > room.y or x[2] > room.z:
            return False
    return True
