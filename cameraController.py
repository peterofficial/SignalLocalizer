import math

import numpy as np
import helpers
from itertools import combinations

#Class to represent an embedded camera controller object
class CameraController:
    def __init__(self, position, orientation, dsp, room):
        self.position = position
        self.orientation = orientation
        self.dsp = dsp
        self.micPositions = []
        self.micSensitivity = 0
        self.room = room

    #Set microphone sensitivity, this should align with the sensitivities of the microphones in the dsp
    def setMicSensitivity(self, sensitivity):
        self.micSensitivity = sensitivity

    #Inform the controller of the positions of microphones in the room
    def setMicPositions(self, micPositions):
        self.micPositions = micPositions

    #Retrieve mic positions array
    def getMicPositions(self):
        return self.micPositions

    #Poll DSP signals from the microphones
    def getSignalsFromDSP(self):
        return self.dsp.pollSignals()

    #Predict the strength of the signal in the room (work in progress, requires calibration step)
    def predictSignalStrength(self, signalArray):
        predictedVolume = (sum(signalArray) / len(signalArray)) / self.micSensitivity #*avgPredictedDistance
        return predictedVolume

    #Generate radius of signal from microphones in the room
    def getSignalDistances(self, actualVolume):
        micPositions = self.micPositions
        micSensitivity = self.micSensitivity
        signalArray = self.getSignalsFromDSP()

        if not micSensitivity:
            print("Microphone sensitivity not set, please set sensitivity before trying to localize.")
            return
        if len(micPositions) < self.dsp.getNumActiveMics():
            print("Please make sure you have location data for all microphones in the system, got {0} positions and {1} active microphones.".format(len(micPositions), self.dsp.getNumActiveMics()))
            return

        predictedVolume = self.predictSignalStrength(signalArray)
        predictedVolume = actualVolume
        distanceArray = []

        for x in range(0, len(signalArray)):
            if signalArray[x] <= 0:
                print("Error with signal from microphone {0}, expected a positive, non-zero reading and got: {1}".format(x, signalArray[x]))
                return
            distanceToMic = (predictedVolume/signalArray[x])*micSensitivity
            distanceArray.append(distanceToMic)

        return distanceArray

    #Predict the position of an audio signal in the room
    def getSignalPosition(self, actualVolume):
        micPositions = self.micPositions
        distanceArray = self.getSignalDistances(actualVolume)
        activeMicCount = self.dsp.getNumActiveMics()

        microphoneSphereStats = []

        #Generate sphere data from the microphones possible pickup pattern
        for x in range(0, activeMicCount):
            radius = float(distanceArray[x])
            offSetX = float(micPositions[x][0])
            offSetY = float(micPositions[x][1])
            offSetZ = float(micPositions[x][2])

            microphoneSphereStats.append([np.array([offSetX, offSetY, offSetZ]), radius])

            for y in range(x+1, activeMicCount):
                separationDistance = helpers.get3DDistance(micPositions[x], micPositions[y])

        #Find all non-repeating permutations of 3 microphone pickup spheres in the room
        spherePerms = combinations(microphoneSphereStats, 3)

        #Calculate all mathematically relevant sphere trilaterations for the mircophone permutations
        intersectionList = []
        for x in spherePerms:
            try:
                intersection = helpers.trilaterate(x[0][0], x[1][0], x[2][0], x[0][1], x[1][1], x[2][1])
            except:
                continue
            if not np.isnan(intersection[0][0]) and not np.isnan(intersection[1][0]):
                intersectionList.append(intersection)

        #Sort the predicted intersections by z value
        intersectionList = sortPoints(intersectionList)

        lowerPoint = [0, 0, 0]
        upperPoint = [0, 0, 0]

        #Average all estimated upper and lower points to find center of signal prediction
        for x in intersectionList:
            for y in range(0, 3):
                lowerPoint[y] += x[0][y]
                upperPoint[y] += x[1][y]
        for y in range(0, 3):
            lowerPoint[y] = lowerPoint[y]/len(intersectionList)
            upperPoint[y] = upperPoint[y]/len(intersectionList)

        #Determine which of the predicted signal locations is within the bounds of the room (this could theoretically flip if the microphone array was on the floor)
        predictedSignalLocation = inRoom([lowerPoint, upperPoint], self.room)

        return predictedSignalLocation

    #Determine the necessary angle offsets to point camera towards the signal
    def rePositionCamera(self, predictedSignalLocation):
        currOrientation = self.orientation
        cameraPosition = self.position

        signalUnitVector = helpers.getUnitVector(predictedSignalLocation, cameraPosition)
        signalDegrees = helpers.getDegreeHeading(signalUnitVector)

        print("->>> Redirecting camera from orientation alpha: {0}, beta: {1}, to orientation alpha: {2}, beta: {3}"
              .format(round(currOrientation[0], 2), round(currOrientation[1], 2), round(signalDegrees[0], 2), round(signalDegrees[1], 2)))

        self.orientation = signalDegrees

#Sort intersection points in the intersection vector list by their y values
def sortPoints(intersectionList):
    for x in range(0, len(intersectionList)):
        if intersectionList[x][0][2] > intersectionList[x][1][2]:
            intersectionList[x] = (intersectionList[x][1], intersectionList[x][0])
    return intersectionList

#Determine which points fall inside of the room (one intersection should be above the ceiling)
def inRoom(points, room):
    point = []
    for x in points:
        if x[0] <= room.x and x[1] <= room.y and x[2] <= room.z:
            point = [round(x[0], 2), round(x[1], 2), round(x[2], 2)]
    return point



