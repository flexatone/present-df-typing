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
    s = np.where(q, 0.5, 0.25)
    return tp.cast(TNDArrayFloat64, v * s)


v1: TNDArrayInt8 = np.arange(20, dtype=np.int8)
q: TNDArrayBool = np.arange(20) % 3 == 0
x = process1(v1, v1)
# tp_np.py:23: error: Argument 2 to "process1" has incompatible type "ndarray[Any, dtype[floating[_64Bit]]]"; expected "ndarray[Any, dtype[bool_]]"  [arg-type]

v2: TNDArrayInt64 = np.arange(20, dtype=np.int64)
q: TNDArrayBool = np.arange(20) % 3 == 0
x = process1(v2, q)
# tp_np.py:29: error: Argument 1 to "process1" has incompatible type "ndarray[Any, dtype[signedinteger[_64Bit]]]"; expected "ndarray[Any, dtype[signedinteger[_8Bit]]]"  [arg-type]

y: TNDArrayBool = process1(v1, q)
# tp_np.py:51: error: Incompatible types in assignment (expression has type "ndarray[Any, dtype[floating[_64Bit]]]", variable has type "ndarray[Any, dtype[bool_]]")  [assignment]



TNDArrayIntAny = np.ndarray[tp.Any, np.dtype[np.signedinteger[tp.Any]]]

def process2(
        v: TNDArrayIntAny,
        q: TNDArrayBool,
        ) -> TNDArrayFloat64:
    s = np.where(q, 0.5, 0.25)
    return tp.cast(TNDArrayFloat64, v * s)

x = process2(v1, q)
x = process2(v2, q)
v3: TNDArrayFloat64 = np.arange(20, dtype=np.float64) * 0.5
x = process2(v3, q)
# tp_np.py:47: error: Argument 1 to "process2" has incompatible type "ndarray[Any, dtype[floating[_64Bit]]]"; expected "ndarray[Any, dtype[signedinteger[Any]]]"  [arg-type]

@sf.CallGuard.check
def process3(
        v: TNDArrayIntAny,
        q: TNDArrayBool,
        ) -> TNDArrayFloat64:
    s = np.where(q, 0.5, 0.25)
    return tp.cast(TNDArrayFloat64, v * s)

x = process3(v1, q)
x = process3(v2, q)
# x = process3(v3, q)
# static_frame.core.type_clinic.ClinicError:
# In args of (v: ndarray[Any, dtype[signedinteger[Any]]], q: ndarray[Any, dtype[bool_]]) -> ndarray[Any, dtype[float64]]
# └── ndarray[Any, dtype[signedinteger[Any]]]
#     └── dtype[signedinteger[Any]]
#         └── Expected signedinteger, provided float64 invalid




@sf.CallGuard.check
def process4(
        v: tp.Annotated[TNDArrayInt8, sf.Require.Shape(24)],
        q: tp.Annotated[TNDArrayBool, sf.Require.Shape(24)],
        ) -> tp.Annotated[TNDArrayFloat64, sf.Require.Shape(24)]:
    s = np.where(q, 0.5, 0.25)
    return tp.cast(TNDArrayFloat64, v * s)

x = process4(v1, q)
# static_frame.core.type_clinic.ClinicError:
# In args of (v: Annotated[ndarray[Any, dtype[int8]], Shape((24,))], q: Annotated[ndarray[Any, dtype[bool_]], Shape((24,))]) -> Annotated[ndarray[Any, dtype[float64]], Shape((24,))]
# └── Annotated[ndarray[Any, dtype[int8]], Shape((24,))]
#     └── Shape((24,))
#         └── Expected shape ((24,)), provided shape (20,)

