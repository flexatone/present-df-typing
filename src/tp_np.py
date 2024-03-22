import typing as tp
import static_frame as sf
import numpy as np

TNDArrayBool = np.ndarray[tp.Any, np.dtype[np.bool_]]
TNDArrayInt8 = np.ndarray[tp.Any, np.dtype[np.int8]]
TNDArrayInt64 = np.ndarray[tp.Any, np.dtype[np.int64]]
TNDArrayFloat64 = np.ndarray[tp.Any, np.dtype[np.float64]]

def process1(
        v: TNDArrayInt8,
        q: TNDArrayBool,
        ) -> TNDArrayFloat64:
    r = np.where(q, 0.5, 1)
    s = np.where(q, 1, 0.25)
    return tp.cast(TNDArrayFloat64, v * r * s)


v1: TNDArrayInt8 = np.arange(20, dtype=np.int8)
q: TNDArrayBool = np.arange(20) % 3 == 0
x = process1(v1, v1)
# tp_np.py:23: error: Argument 2 to "process1" has incompatible type "ndarray[Any, dtype[floating[_64Bit]]]"; expected "ndarray[Any, dtype[bool_]]"  [arg-type]

v2: TNDArrayInt64 = np.arange(20, dtype=np.int64)
q: TNDArrayBool = np.arange(20) % 3 == 0
x = process1(v2, q)

# tp_np.py:29: error: Argument 1 to "process1" has incompatible type "ndarray[Any, dtype[signedinteger[_64Bit]]]"; expected "ndarray[Any, dtype[signedinteger[_8Bit]]]"  [arg-type]


TNDArrayIntAny = np.ndarray[tp.Any, np.dtype[np.signedinteger[tp.Any]]]

def process2(
        v: TNDArrayIntAny,
        q: TNDArrayBool,
        ) -> TNDArrayFloat64:
    r = np.where(q, 0.5, 1)
    s = np.where(q, 1, 0.25)
    return tp.cast(TNDArrayFloat64, v * r * s)

x = process2(v1, q)
x = process2(v2, q)



y: TNDArrayBool = process2(v1, q)
# tp_np.py:51: error: Incompatible types in assignment (expression has type "ndarray[Any, dtype[floating[_64Bit]]]", variable has type "ndarray[Any, dtype[bool_]]")  [assignment]

