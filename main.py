# Peter Donaldson - 11/7/2020
from microphone import Microphone
from dsp import DSP
from cameraController import CameraController
import helpers
from room import Room
from visualizer import visualize
from tkinter import *
import matplotlib.pyplot as plt

def runVisualizer(roomDimensions, microphoneSensitivity, signalPos, sigStrength, micGrid, gridOffset, gridHeight, camPos):
    # Room parameters
    width = roomDimensions[0]
    length = roomDimensions[1]
    ceiling = roomDimensions[2]

    # Define room
    room = Room(width, length, ceiling)

    # Create a microphone array
    microphonePositions = helpers.generateMicArray(micGrid[0], micGrid[1], gridOffset, gridHeight)
    if not helpers.allInRoom(microphonePositions, room):
        print("Some microphones fell outside the boundaries of the room, please re-enter data.")
        return

    # Microphone parameters
    numMicrophones = len(microphonePositions)
    microphoneArray = []
    micSensitivity = microphoneSensitivity

    # Set up microphone objects
    for x in range(0, numMicrophones):
        microphoneArray.append(Microphone(microphonePositions[x], micSensitivity))

    # Configure DSP object
    dsp = DSP(99, microphoneArray)

    # Set up camera controller
    cameraPosition = camPos
    if not helpers.allInRoom([cameraPosition], room):
        print("The camera fell outside the boundaries of the room, please re-enter data.")
        return
    cameraOrientation = [0, 0]  # pointing along x-axis in degrees
    cameraController = CameraController(cameraPosition, cameraOrientation, dsp, room)
    cameraController.setMicSensitivity(micSensitivity)
    cameraController.setMicPositions(microphonePositions)

    # Define Signal parameters
    signalPosition = signalPos
    if not helpers.allInRoom([signalPosition], room):
        print("The signal fell outside the boundaries of the room, please re-enter data.")
        return
    signalStrength = sigStrength

    # Send signal to all microphones
    for microphone in microphoneArray:
        microphone.sendSignal(signalPosition, signalStrength)
    print(
        "-> Audio signal at position x: {0}, y: {1}, z: {2} with strength {3} broadcast to all microphones".format(
            signalPosition[0], signalPosition[1], signalPosition[2], signalStrength))

    # Predict signal location using sphere trilateration
    predictedSignalLocation = cameraController.getSignalPosition(signalStrength)
    print("->>> Predicted Signal Location: {0}, Actual Signal Location: {1}".format(predictedSignalLocation,
                                                                                  signalPosition))

    cameraController.rePositionCamera(predictedSignalLocation)

    visualize(cameraController, signalStrength, predictedSignalLocation)

def getEntryList(entryField):
    outputArray = entryField.get().replace(" ", "").split(",")
    for i in range(0, len(outputArray)):
        outputArray[i] = float(outputArray[i])
    return outputArray

def getEntryListInt(entryField):
    outputArray = entryField.get().replace(" ", "").split(",")
    for i in range(0, len(outputArray)):
        outputArray[i] = int(outputArray[i])
    return outputArray

if __name__ == '__main__':
    app = Tk()
    app.title('Signal Tracker')
    app.geometry('350x350')

    def runProgram():
        plt.close('all')

        try:
            roomDimensions = getEntryList(roomDims)
            microphoneSensitivity = float(micSensitivity.get())
            signalPos = getEntryList(signalPosition)
            sigStrength = float(signalStrength.get())
            micGrid = getEntryListInt(micGridDims)
            gridOffset = float(micGridOffset.get())
            gridHeight = float(micGridHeight.get())
            camPos = getEntryList(cameraPosition)

            if min(roomDimensions) < 0 or microphoneSensitivity < 0 or min(signalPos) < 0 or sigStrength < 0 or min(micGrid) < 0 or gridOffset < 0 or gridHeight < 0 or min(camPos) < 0:
                print("Please ensure no negative values are used.")
                return
        except:
            print("Please ensure entry fields comply with the given formats.")
            return

        runVisualizer(roomDimensions, microphoneSensitivity, signalPos, sigStrength, micGrid, gridOffset, gridHeight, camPos)

    # create text fields
    w = Label(app, text="Room Dimensions (float, float, float):")
    w.pack()
    roomDims = Entry(app, width=50)
    roomDims.pack(fill=NONE, side=TOP)
    roomDims.insert(END, "10, 10, 5")

    w = Label(app, text="Microphone Sensitivity (float):")
    w.pack()
    micSensitivity = Entry(app, width=50)
    micSensitivity.pack(fill=NONE, side=TOP)
    micSensitivity.insert(END, "10")

    w = Label(app, text="Signal Position (float, float, float):")
    w.pack()
    signalPosition = Entry(app, width=50)
    signalPosition.pack(fill=NONE, side=TOP)
    signalPosition.insert(END, "6, 6, 2")

    w = Label(app, text="Signal Strength (float):")
    w.pack()
    signalStrength = Entry(app, width=50)
    signalStrength.pack(fill=NONE, side=TOP)
    signalStrength.insert(END, "3")

    w = Label(app, text="Mic Grid Dimensions (int, int):")
    w.pack()
    micGridDims = Entry(app, width=50)
    micGridDims.pack(fill=NONE, side=TOP)
    micGridDims.insert(END, "3, 3")

    w = Label(app, text="Mic Grid Offset (float):")
    w.pack()
    micGridOffset = Entry(app, width=50)
    micGridOffset.pack(fill=NONE, side=TOP)
    micGridOffset.insert(END, "5")

    w = Label(app, text="Mic Grid Height (float):")
    w.pack()
    micGridHeight = Entry(app, width=50)
    micGridHeight.pack(fill=NONE, side=TOP)
    micGridHeight.insert(END, "5")

    w = Label(app, text="Camera Position (float, float, float):")
    w.pack()
    cameraPosition = Entry(app, width=50)
    cameraPosition.pack(fill=NONE, side=TOP)
    cameraPosition.insert(END, "0, 0, 2")

    # create button to open file
    openBtn = Button(app, text='Open', command=runProgram)
    openBtn.pack(expand=FALSE, fill=X, side=TOP)

    app.mainloop()
