


import numpy as np
import typing as tp


# TNDArray1D = np.ndarray[tuple[tp.Any], tp.Any];
# TNDArray2D = np.ndarray[tuple[tp.Any, tp.Any], tp.Any];
# TNDArrayAny = np.ndarray[tuple[tp.Any, tp.Any], tp.Any];

# TNDArray1DL10 = np.ndarray[tuple[tp.Literal[10]], tp.Any];


# a1: TNDArray1DL10 = np.zeros((10,))
# a2 = np.empty((10, 10))


# def process1(x: TNDArray1D, y: TNDArray1D): ...
# process1(a1, a1)


# def process2(x: TNDArray2D, y: TNDArray2D): ...
# process2(a2, a2)


# def process3(x: TNDArray1DL10, y: TNDArray2D): ...
# process3(a1, a2)



def process1(x: np.ndarray[tuple[int], np.dtype[np.signedinteger]]): ...

a1 = np.empty(100, dtype=np.int16)
process1(a1) # mypy passes

a2 = np.empty(100, dtype=np.uint8)
process1(a2) # mypy fails
# tp_array.py:38: error: Argument 1 to "process1" has incompatible type "ndarray[tuple[int], dtype[unsignedinteger[_8Bit]]]"; expected "ndarray[tuple[int], dtype[signedinteger[Any]]]"  [arg-type]


a3 = np.empty((100, 100, 100), dtype=np.int64)
process1(a3) # mypy fails
# tp_array.py:43: error: Argument 1 to "process1" has incompatible type "ndarray[tuple[int, int, int], dtype[signedinteger[_64Bit]]]"; expected "ndarray[tuple[int], dtype[signedinteger[Any]]]"  [arg-type]



import static_frame as sf
@sf.CallGuard.check
def process2(x: np.ndarray[tuple[int], np.dtype[np.signedinteger]]): ...

a2 = np.empty(100, dtype=np.uint8)
process2(a2)
# static_frame.core.type_clinic.ClinicError:
# In args of (x: ndarray[tuple[int], dtype[signedinteger]]) -> Any
# └── In arg x
#     └── ndarray[tuple[int], dtype[signedinteger]]
#         └── dtype[signedinteger]
#             └── Expected signedinteger, provided uint8 invalid

process2(a3) # fails

