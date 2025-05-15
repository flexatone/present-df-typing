


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



def process1(x: np.ndarray[tuple[tp.Any], np.dtype[np.integer]]): ...

a1 = np.empty(100, dtype=np.int16)
process1(a1) # passes

a2 = np.empty(100, dtype=np.int8)
process1(a2) # passes

a3 = np.empty(100, dtype=np.float64)
process1(a3) # fails
# tp_array.py:41: error: Argument 1 to "process1" has incompatible type "ndarray[tuple[int], dtype[float64]]"; expected "ndarray[tuple[Any], dtype[integer[Any]]]"  [arg-type]

a4 = np.empty((100, 100, 100), dtype=np.int16)
process1(a4) # fails
# tp_array.py:47: error: Argument 1 to "process1" has incompatible type "ndarray[tuple[int, int, int], dtype[signedinteger[_16Bit]]]"; expected "ndarray[tuple[Any], dtype[integer[Any]]]"  [arg-type]

# then do the same with SF.typeguard


import static_frame as sf

@sf.CallGuard.check
def process2(x: np.ndarray[tuple[tp.Any], np.dtype[np.integer]]): ...

# process2(a3) # fails
# static_frame.core.type_clinic.ClinicError:
# In args of (x: ndarray[tuple[Any], dtype[integer]]) -> Any
# └── In arg x
#     └── ndarray[tuple[Any], dtype[integer]]
#         └── dtype[integer]
#             └── Expected integer, provided float64 invalid

process2(a4) # fails

print(sf.CallGuard.check)