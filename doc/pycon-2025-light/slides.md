---
theme: default
class: text-center
highlighter: shiki
lineNumbers: false
transition: slide-left
aspectRatio: 16/9
favicon: /favicon.ico
title: "Doing More with NumPy Array Type Annotations"
# background: /IMG_4390.jpg

---

<!--
Do More with NumPy Array Type Annotations
NumPy Array Type Annotations for Static Analysis and Runtime Validation
New Opportunities with NumPy Array Type Hints
 -->

# New Opportunities with NumPy Array Type Hints

<br />
<br />

#### Christopher Ariza
#### CTO, Research Affiliates


<style>
h1 {font-size: 3.5em !important; line-height: 1.3 !important;}
</style>



---

# Shallow Typing


<Transform :scale="1.25">

```python {all}
import numpy as np

def process(
    x: np.ndarray,
    y: np.ndarray,
    ) -> np.ndarray: ...
```
</Transform>



---

# Deep Array Typing


<Transform :scale="1.25">

```python {all}
import numpy as np

def process(
    x: np.ndarray[tuple[int, int], np.dtype[np.floating]],
    y: np.ndarray[tuple[int], np.dtype[np.bool_]],
    ) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]: ...
```
</Transform>



---

# The Generic `np.ndarray`

<Transform :scale="1.25">
<v-clicks>

* Two type variables
    * shape
    * dtype
* until NumPy 2.1:
    ```python
    np.ndarray[Any, np.dtype[np.int8]]
    ```
* from NumPy 2.1:
    ```python
    np.ndarray[tuple[int, ...], np.dtype[np.int8]]
    ```
</v-clicks>
</Transform>




---

# Shapes are `tuple`


<Transform :scale="1.25">

```python {1|2|3|4}
tuple[int, ...]  # ND
tuple[int]  # 1D
tuple[int, int] # 2D
tuple[Literal[20], int] # 2D, 20 rows

```
</Transform>


---

# Dtypes are Generic


<Transform :scale="1.25">

```python {1-3|4|5|6|7}
import numpy as np

np.dtype[np.int8]
np.dtype[np.uint16]
np.dtype[np.integer]
np.dtype[np.floating]
np.dtype[np.number]

```
</Transform>




---

# Concretizing `np.ndarray`


<Transform :scale="1.25">

```python {1-2|3-4|5-6}
# 1D, any 8 bit integer
def process(x: np.ndarray[tuple[int], np.dtype[np.int8]]): ...
# 2D, any integer
def process(x: np.ndarray[tuple[int, int], np.dtype[np.integer]]): ...
# ND, datetime64
def process(x: np.ndarray[tuple[int, int], np.dtype[np.datetime64]]): ...
```
</Transform>


---

# Static Type Checking with `mypy`


<Transform :scale="1.25">

```python {1|1-4|1,5-10|1,11-}
def process1(x: np.ndarray[tuple[int], np.dtype[np.signedinteger]]): ...

a1 = np.empty(100, dtype=np.int16)
process1(a1) # mypy passes

a2 = np.empty(100, dtype=np.uint8)
process1(a2) # mypy fails
# error: Argument 1 to "process1" has incompatible type
# "ndarray[tuple[int], dtype[unsignedinteger[_8Bit]]]";
# expected "ndarray[tuple[int], dtype[signedinteger[Any]]]"

a3 = np.empty((100, 100, 100), dtype=np.int64)
process1(a3) # mypy fails
# error: Argument 1 to "process1" has incompatible type
# "ndarray[tuple[int, int, int], dtype[signedinteger[_64Bit]]]";
# expected "ndarray[tuple[int], dtype[signedinteger[Any]]]"
```
</Transform>

---
layout: center

---

## Runtime Validation of `np.ndarray` Types?


<!-- Need run-time type checker Specialized for NumPy -->



---
layout: center

---

## StaticFrame 3: `TypeClinic`



---

# Run-time Type Checking with `TypeClinic`

<Transform :scale="1.25">

```python {1-3|1-12}
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
```
</Transform>



---

# Run-time Type Checking with `TypeClinic`

<Transform :scale="1.25">

```python {1-3|1-12}
import static_frame as sf
@sf.CallGuard.check
def process2(x: np.ndarray[tuple[int], np.dtype[np.signedinteger]]): ...

a3 = np.empty((100, 100, 100), dtype=np.int64)
process2(a3)
# static_frame.core.type_clinic.ClinicError:
# In args of (x: ndarray[tuple[int], dtype[signedinteger]]) -> Any
# └── In arg x
#     └── ndarray[tuple[int], dtype[signedinteger]]
# TODO: update!
```
</Transform>


---

# Conclusion

<Transform :scale="1.25">
<v-clicks>

Make your NumPy arrays concrete

Type check with `mypy`

Runtime validation with `TypeClinic`

</v-clicks>
</Transform>



---
layout: cover

---

# Thank you


