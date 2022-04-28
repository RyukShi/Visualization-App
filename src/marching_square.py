from decimal import localcontext, Context, Inexact
import math
import random
import numpy as np
import matplotlib.pyplot as plt


class MarchingSquare():

    def __init__(self) -> None:

        self.randomData = []
        self.maxPts = 256
        # change dim (3d)
        self.dim = '2d'
        self.xMax = 0
        self.generateRandomData(size=256)
        self.randomNumber = self.generateRandomNumber()

    def run(self):

        self.figure = plt.figure(figsize=(8, 8), dpi=100)

        if (self.dim == '2d'):

            self.axes = self.figure.add_subplot(111)

            self.axes.set_title('2D visualization (square)')
            self.axes.set_aspect('equal', adjustable='box')
            self.axes.set_facecolor('#e1e1e1')

            self.structuringData()
            self.getBinaryMatrix()
            self.drawPoints()
            self.isoValues()

        elif (self.dim == '3d'):

            self.axes3D = self.figure.add_subplot(111, projection=self.dim)
            self.axes3D.set_title('3D visualization (surface)')
            self.plotSurface()

        plt.show()

    def generateRandomData(self, rangeMin=2.5, rangeMax=6.5, size=49):

        if size <= self.maxPts and size >= 4 and self.isPerfectSquare(size):
            self.randomData = np.random.uniform(rangeMin, rangeMax, size)
            self.xMax = int(math.sqrt(len(self.randomData)))
            print("Random data generated successfully!")
        else:
            print("Incorrect value for size (min: 4 pts ; max: 256 pts)")

    def generateRandomNumber(self) -> float:
        return random.uniform(min(self.randomData), max(self.randomData))

    def isPerfectSquare(self, x):

        with localcontext(Context()) as ctx:
            ctx.prec = math.ceil(math.log10(x or 1)) + 1
            ctx.sqrt(x).to_integral_exact()
            return not ctx.flags[Inexact]

    ########## 3D projection graph ##########

    def coordinatesProjection3D(self, data):

        self.X = []
        self.Y = []
        self.Z = data

        for i in range(0, self.xMax):
            for j in range(0, self.xMax):
                self.X.append(j)
                self.Y.append(i)

    def plotSurface(self):

        self.coordinatesProjection3D(data=self.randomData)

        surface = self.axes3D.plot_trisurf(
            self.X, self.Y, self.Z, cmap='winter', linewidth=0, antialiased=False)
        self.axes3D.set_zlim(min(self.Z), max(self.Z))

        self.figure.colorbar(surface, shrink=0.5, aspect=5)

        self.axes3D.set_xlabel('X')
        self.axes3D.set_ylabel('Y')
        self.axes3D.set_zlabel('Z')

    ########## 2D projection graph ##########

    def structuringData(self):

        self.structuredData = np.empty(
            [self.xMax, self.xMax], dtype=float)

        index = 0

        for i in range(0, self.xMax):
            for j in range(0, self.xMax):
                self.structuredData[i, j] = self.randomData[index]
                index += 1

    def drawPoints(self, values=False, points=True):

        if (points):
            for i in range(0, self.xMax):
                for j in range(0, self.xMax):
                    if (self.binaryMatrix[i, j] == 0):
                        self.axes.scatter(j, i, c='#4f4f4f', s=8)
                    else:
                        self.axes.scatter(j, i, c='#14c606', s=8)
                    if (values):
                        self.axes.text(j + 0.01, i + 0.05,
                                       str(round(self.structuredData[i, j], 1)))

    def getBinaryMatrix(self):

        self.binaryMatrix = np.empty(
            [self.xMax, self.xMax], dtype=int)

        for i in range(0, self.xMax):
            for j in range(0, self.xMax):
                if (self.structuredData[i, j] >= self.randomNumber):
                    self.binaryMatrix[i, j] = 1
                else:
                    self.binaryMatrix[i, j] = 0

    def linearInterpolation(self, evaluatedValue, x, y):
        return np.interp(evaluatedValue, x, y)

    def isoValues(self, states=False, points=False):

        for i in range(0, self.xMax - 1):
            for j in range(0, self.xMax - 1):
                p1 = self.binaryMatrix[i + 1, j]
                p2 = self.binaryMatrix[i + 1, j + 1]
                p3 = self.binaryMatrix[i, j]
                p4 = self.binaryMatrix[i, j + 1]

                """
                v1 = self.structuredData[i + 1, j]
                v2 = self.structuredData[i + 1, j + 1]
                v3 = self.structuredData[i, j]
                v4 = self.structuredData[i, j + 1]
                """

                if ((p1, p2, p3, p4) == (0, 0, 1, 0)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '2')

                    x = [j + 0.5, j]
                    y = [i, i + 0.5]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (0, 0, 0, 1)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '3')

                    x = [j + 0.5, j + 1]
                    y = [i, i + 0.5]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (0, 0, 1, 1)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '4')

                    x = [j, j + 1]
                    y = [i + 0.5, i + 0.5]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (0, 1, 0, 0)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '5')

                    x = [j + 0.5, j + 1]
                    y = [i + 1, i + 0.5]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (0, 1, 1, 0)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '6')

                    x = [j + 0.5, j + 1, j + 0.5, j]
                    y = [i + 1, i + 0.5, i, i + 0.5]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x[:2], y[:2], c='#f69b41')
                    self.axes.plot(x[-2:], y[-2:], c='#f69b41')

                elif ((p1, p2, p3, p4) == (0, 1, 0, 1)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '7')

                    x = [j + 0.5, j + 0.5]
                    y = [i, i + 1]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (0, 1, 1, 1)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '8')

                    x = [j, j + 0.5]
                    y = [i + 0.5, i + 1]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (1, 0, 0, 0)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '9')

                    x = [j, j + 0.5]
                    y = [i + 0.5, i + 1]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (1, 0, 1, 0)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '10')

                    x = [j + 0.5, j + 0.5]
                    y = [i, i + 1]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (1, 0, 0, 1)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '11')

                    x = [j, j + 0.5, j + 0.5, j + 1]
                    y = [i + 0.5, i + 1, i, i + 0.5]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x[:2], y[:2], c='#f69b41')
                    self.axes.plot(x[-2:], y[-2:], c='#f69b41')

                elif ((p1, p2, p3, p4) == (1, 0, 1, 1)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '12')

                    x = [j + 0.5, j + 1]
                    y = [i + 1, i + 0.5]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (1, 1, 0, 0)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '13')

                    x = [j, j + 1]
                    y = [i + 0.5, i + 0.5]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (1, 1, 1, 0)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '14')

                    x = [j + 0.5, j + 1]
                    y = [i, i + 0.5]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')

                elif ((p1, p2, p3, p4) == (1, 1, 0, 1)):

                    if (states):
                        self.axes.text(j + 0.5, i + 0.5, '15')

                    x = [j + 0.5, j]
                    y = [i, i + 0.5]

                    if (points):
                        self.axes.scatter(x, y, c='#f69b41', s=8)
                    self.axes.plot(x, y, c='#f69b41')


def main():

    marching_square = MarchingSquare()
    marching_square.run()


if __name__ == '__main__':
    main()
