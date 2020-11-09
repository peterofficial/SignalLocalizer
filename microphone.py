import helpers

#Class to represent a microphone object
class Microphone:

    def __init__(self, position, sensitivity):
        # in units of volume/distance
        self.position = position
        self.sensitivity = sensitivity
        self.volume = 0

    #Send a signal too the microphone and store the resulting volume
    def sendSignal(self, position, signal):
        distance = helpers.get3DDistance(self.position, position)
        if distance <= 0:
            print("Signal occurred inside microphone, sensor clipping, volume reset.")
            return
        self.volume = (signal/distance)*self.sensitivity

    #Return the volume the microphone has registered
    def getVolume(self):
        return self.volume