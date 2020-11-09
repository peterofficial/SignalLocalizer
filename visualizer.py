import matplotlib.pyplot as plt
import numpy as np

#Function to visualize the signal prediction
def visualize(cameraController, actualVolume, signal):
    distanceArray = cameraController.getSignalDistances(actualVolume)
    activeMicCount = cameraController.dsp.getNumActiveMics()
    micPositions = cameraController.getMicPositions()

    microphoneDisplays = []

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    maxScale = max(cameraController.room.x, cameraController.room.y, cameraController.room.z)

    ax.set_xlim3d(-1, maxScale)
    ax.set_ylim3d(-1, maxScale)
    ax.set_zlim3d(-1, maxScale)

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    #Generate sphere data from the microphones possible pickup pattern
    for x in range(0, activeMicCount):
        radius = float(distanceArray[x])
        offSetX = float(micPositions[x][0])
        offSetY = float(micPositions[x][1])
        offSetZ = float(micPositions[x][2])

        # Make data
        a = radius * np.outer(np.cos(u), np.sin(v)) + offSetX
        b = radius * np.outer(np.sin(u), np.sin(v)) + offSetY
        c = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + offSetZ

        microphoneDisplays.append([a,b,c])

        x = [offSetX, signal[0]]
        y = [offSetY, signal[1]]
        z = [offSetZ, signal[2]]

        # Plot vector between microphones and signal
        ax.plot(x, y, z, 'c--', linewidth=1, markersize=12, zorder=6)

    #Plot microphone spheres of effect
    for x in microphoneDisplays:
        ax.plot_surface(x[0], x[1], x[2], alpha=0.035, color='b', zorder=4)

    #Plot microphone positions
    for x in micPositions:
        ax.plot(x[0], x[1], x[2], 'bo', zorder=7)

    #Plot position of camera
    ax.plot(cameraController.position[0], cameraController.position[1], cameraController.position[2], 'go', linewidth=2, markersize=12, zorder=9)

    #Plot predicted signal position
    ax.plot(signal[0], signal[1], signal[2], 'r+', linewidth=6, markersize=10, zorder=10)

    x = [cameraController.position[0], signal[0]]
    y = [cameraController.position[1], signal[1]]
    z = [cameraController.position[2], signal[2]]

    # Plot vector between camera and signal
    ax.plot(x, y, z, 'g--', linewidth=1, markersize=12, zorder=8)

    #Plot the bounds of the room
    rect_prism(ax,
               np.array([0, cameraController.room.x]),
               np.array([0, cameraController.room.y]),
               np.array([0, cameraController.room.z]))

    ax.set_box_aspect([1,1,1])
    plt.show()

#Draw a rectangular prism on the graph
def rect_prism(ax, x_range, y_range, z_range):
    color = "m:"
    alpha = 1
    zorder = 5
    ax.plot(x_range, [y_range[0], y_range[0]], [z_range[0], z_range[0]], color, alpha=alpha, zorder=zorder)
    ax.plot(x_range, [y_range[1], y_range[1]], [z_range[0], z_range[0]], color, alpha=alpha, zorder=zorder)
    ax.plot(x_range, [y_range[0], y_range[0]], [z_range[1], z_range[1]], color, alpha=alpha, zorder=zorder)
    ax.plot(x_range, [y_range[1], y_range[1]], [z_range[1], z_range[1]], color, alpha=alpha, zorder=zorder)

    ax.plot([x_range[0], x_range[0]], y_range, [z_range[0], z_range[0]], color, alpha=alpha, zorder=zorder)
    ax.plot([x_range[0], x_range[0]], y_range, [z_range[1], z_range[1]], color, alpha=alpha, zorder=zorder)
    ax.plot([x_range[1], x_range[1]], y_range, [z_range[0], z_range[0]], color, alpha=alpha, zorder=zorder)
    ax.plot([x_range[1], x_range[1]], y_range, [z_range[1], z_range[1]], color, alpha=alpha, zorder=zorder)

    ax.plot([x_range[0], x_range[0]], [y_range[0], y_range[0]], z_range, color, alpha=alpha, zorder=zorder)
    ax.plot([x_range[0], x_range[0]], [y_range[1], y_range[1]], z_range, color, alpha=alpha, zorder=zorder)
    ax.plot([x_range[1], x_range[1]], [y_range[0], y_range[0]], z_range, color, alpha=alpha, zorder=zorder)
    ax.plot([x_range[1], x_range[1]], [y_range[1], y_range[1]], z_range, color, alpha=alpha, zorder=zorder)