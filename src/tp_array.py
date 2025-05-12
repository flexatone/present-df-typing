


import numpy as np
import typing as tp


TNDArray1D = np.ndarray[tuple[tp.Any], tp.Any];
TNDArray2D = np.ndarray[tuple[tp.Any, tp.Any], tp.Any];
TNDArrayAny = np.ndarray[tuple[tp.Any, tp.Any], tp.Any];

TNDArray1DL10 = np.ndarray[tuple[tp.Literal[10]], tp.Any];


a1: TNDArray1DL10 = np.zeros((10,))
a2 = np.empty((10, 10))


def process1(x: TNDArray1D, y: TNDArray1D): ...
process1(a1, a1)


def process2(x: TNDArray2D, y: TNDArray2D): ...
process2(a2, a2)


def process3(x: TNDArray1DL10, y: TNDArray2D): ...
process3(a1, a2)

