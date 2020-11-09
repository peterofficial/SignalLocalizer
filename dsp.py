#Class to represent a DSP object
class DSP:
    def __init__(self, numPorts, microphones):
        self.numPorts = numPorts

        #Ensure plugged in microphones don't exceed the capacity of the DSP
        if (len(microphones) > numPorts):
            self.microphones = microphones[0:numPorts-1]
            print("Plugged in too many microphones, reduced to {}.".format(numPorts))
        else:
            self.microphones = microphones

        self.signalArray = []

        #If microphones are already receiving a signal, poll them and populate the signal array on DSP initiation
        for microphone in microphones:
            self.signalArray.append(microphone.getVolume())

    #Poll microphones to populate signal array
    def pollSignals(self):
        self.signalArray = []
        for microphone in self.microphones:
            self.signalArray.append(microphone.getVolume())
        return self.signalArray

    #Return the DSP signal array
    def getSignalArray(self):
        return self.signalArray

    #Return the number of active microphones in the system
    def getNumActiveMics(self):
        return len(self.microphones)

