import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x_val = []
y_val = []

def getData(i):
    while True:
        with open("data.txt") as file:
            # read the contents of the file
            contents = file.read()
            if contents:
                string = contents.strip("[]")
                array = np.fromstring(string, dtype=float, sep=" ")

                if array.any():
                    x_val.clear()
                    y_val.clear()
                    for i in range(0,360):
                        if array[i] > 1 and array[i] < 1000:
                            x_val.append((math.cos(math.radians(i)))*array[i])
                            y_val.append((math.sin(math.radians(i)))*array[i])

                    plt.clf()
                    plt.scatter(x_val, y_val)
                    break

ani = animation.FuncAnimation(plt.gcf(), getData, interval=100)
plt.tight_layout()
plt.show()