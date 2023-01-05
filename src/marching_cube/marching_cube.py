import matplotlib.pyplot as plt
import numpy as np
from random import uniform
from itertools import product, combinations
from constant import TRI_TABLE


class MarchingCube():

    def __init__(
        self,
        rangeMin: float = 2.5,
        rangeMax: float = 6.5,
        specificState: int = None,
        verbose: bool = False
    ):
        self.rangeMin = rangeMin
        self.rangeMax = rangeMax
        self.verbose = verbose

        if specificState:
            if specificState < 0 and specificState > 255:
                raise ValueError(
                    "The value must not be negative, and must be greater than or equal to 0 and not exceed 255.")
            else:
                self.state = specificState
        else:
            self.state = self.getState()

    def run(self):
        f = plt.figure(figsize=(8, 8), dpi=100)
        self.axes = f.add_subplot(111, projection='3d')
        f.suptitle(f"Cette figure représente l'état {self.state}", fontsize=12)
        self.drawCube()
        self.drawTriangle()
        plt.show()

    def generateRandomData(self) -> list:
        return [uniform(self.rangeMin, self.rangeMax) for _ in range(0, 8)]

    def generateRandomNumber(self) -> float:
        return uniform(self.rangeMin, self.rangeMax)

    def drawCube(self):
        r = [0, 1]
        for s, e in combinations(np.array(list(product(r, r, r))), 2):
            if np.sum(np.abs(s-e)) == r[1]-r[0]:
                self.axes.plot3D(*zip(s, e), color="red")

        self.axes.set_xlabel('X axis')
        self.axes.set_ylabel('Y axis')
        self.axes.set_zlabel('Z axis')

    def getState(self) -> int:
        randomNumber = self.generateRandomNumber()
        randomData = self.generateRandomData()
        if self.verbose:
            print(f"randomNumber = {randomNumber}")
            print(f"randomData = {randomData}")

        binary = ''
        for i in range(0, 8):
            if randomData[i] >= randomNumber:
                binary += '1'
            else:
                binary += '0'
        return int(binary, 2)

    def drawTriangle(self):
        triangles = TRI_TABLE[self.state]
        i = 0
        while (triangles[i] != -1 and triangles[i + 1] != -1 and triangles[i + 2] != -1):
            p1 = self.getEdgeCoordinates(triangles[i])
            p2 = self.getEdgeCoordinates(triangles[i+1])
            p3 = self.getEdgeCoordinates(triangles[i+2])
            self.axes.scatter(p1[0], p1[1], p1[2], marker='o', color='blue')
            self.axes.scatter(p2[0], p2[1], p2[2], marker='o', color='blue')
            self.axes.scatter(p3[0], p3[1], p3[2], marker='o', color='blue')
            self.axes.plot_trisurf([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], [
                                   p1[2], p2[2], p3[2]], color='purple', alpha=0.5)
            i += 3

    def getEdgeCoordinates(self, edge: int) -> list:
        if edge == 0:
            return [0.5, 1, 0]
        elif edge == 1:
            return [1, 0.5, 0]
        elif edge == 2:
            return [0.5, 0, 0]
        elif edge == 3:
            return [0, 0.5, 0]
        elif edge == 4:
            return [0.5, 1, 1]
        elif edge == 5:
            return [1, 0.5, 1]
        elif edge == 6:
            return [0.5, 0, 1]
        elif edge == 7:
            return [0, 0.5, 1]
        elif edge == 8:
            return [0, 1, 0.5]
        elif edge == 9:
            return [1, 1, 0.5]
        elif edge == 10:
            return [1, 0, 0.5]
        elif edge == 11:
            return [0, 0, 0.5]
        else:
            return None

    def interpBetweenTwoPoints(self, p1: list, p2: list, t: float) -> list:
        return [p1[i] + t * (p2[i] - p1[i]) for i in range(len(p1))]
