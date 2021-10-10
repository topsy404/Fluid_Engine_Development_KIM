"""
-*-coding = utf-8 -*-
__author: topsy
@time:2021/10/10 10:16
"""
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation

kBufferSize = 80
frames = 1000
M_PI = 3.1425926

kGrayScaleTable = " 123456789";
kGrayScaleTableSize = len(kGrayScaleTable)


class HelloFluid:
    def __init__(self):
        self.x = 0.0
        self.y = 1.0
        self.speedX = 1.0
        self.speedY = -0.5
        self.waveLengthX = 0.8
        self.waveLengthY = 1.2
        self.maxHeightX = 0.5
        self.maxHeightY = 0.4
        self.fps = 100
        self.timeInterval = 1.0 / self.fps
        self.heightField = [0.0] * kBufferSize

    def init_ani(self):
        """
        initial the animation
        :return:
        """
        self.ax.set_xlim(0, 1.0)
        self.ax.set_ylim(-0.1, 1.1)
        return self.ln,

    def update_ani(self, frames):
        """
        update the frame
        :param frames:
        :return:
        """
        # new position of x and y
        self.x, self.speedX = self._updateWave(self.x, self.speedX)
        self.y, self.speedY = self._updateWave(self.y, self.speedY)
        print("x: {:.4f}, y: {:.4f}".format(self.x, self.y))
        # update the heightField
        self.heightField = [0.0] * kBufferSize
        self.accumulateWaveToHeightField(self.x, self.waveLengthX, self.maxHeightX)
        self.accumulateWaveToHeightField(self.y, self.waveLengthY, self.maxHeightY)
        # new frame
        xData = np.linspace(0, 1, kBufferSize)
        yData = self.heightField
        self.ln.set_data(xData, yData)
        return self.ln,

    def _updateWave(self, x, speed):
        """
        update the position of wave after one time interval
        :param x:
        :param speed:
        :return:
        """
        x += self.timeInterval * speed
        # boundary conditions
        if x >= 1.0:
            speed = -speed
            x = 1.0 + self.timeInterval * speed
        elif x <= 0.0:
            speed = -speed
            x = self.timeInterval * speed
        return x, speed

    def accumulateWaveToHeightField(self, x, waveLength, maxHeight):
        """
        update the height field
        :param x:
        :param waveLength:
        :param maxHeight:
        :return:
        """
        quarteWaveLength = 0.25 * waveLength
        start = int((x - quarteWaveLength) * kBufferSize)
        end = int((x + quarteWaveLength) * kBufferSize)
        start = max(0, start)
        end = min(end, kBufferSize - 1)
        for i in range(start, end + 1):
            position = i / kBufferSize
            distance = min(1.0, abs(position - x) / quarteWaveLength)
            height = np.cos(distance * M_PI / 2) * maxHeight
            self.heightField[i] += height

    def run(self):
        self.fig, self.ax = plt.subplots()
        self.ln, = plt.plot([], [])
        ani = FuncAnimation(self.fig, self.update_ani, frames=frames, init_func=self.init_ani, blit=True)
        ani.save("./helloFluid.gif", writer="imagemagick", fps=10)
        # plt.show()


def run():
    demo = HelloFluid()
    demo.run()


if __name__ == "__main__":
    run()
