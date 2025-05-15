---
theme: default
class: text-center
highlighter: shiki
lineNumbers: false
transition: slide-left
aspectRatio: 16/9
favicon: /favicon.ico
title: "."
# background: /IMG_4390.jpg

---


# Doing More with NumPy Array Type Annotations

<br />
<br />

#### Christopher Ariza
#### CTO, Research Affiliates


<style>
h1 {font-size: 3.5em !important; line-height: 1.3 !important;}
</style>



---

# Shallow Typing


<Transform :scale="1.5">

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


<Transform :scale="1.5">

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

<Transform :scale="1.5">
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

# Dtypes are Generic


<Transform :scale="1.5">

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

# Shapes are `tuple`


<Transform :scale="1.5">

```python {1|2|3|4}
tuple[int, ...]  # ND
tuple[int]  # 1D
tuple[int, int] # 2D
tuple[Literal[20], int] # 2D, 20 rows

```
</Transform>



---

# Concretizing `np.ndarray`


<Transform :scale="1.5">

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


<Transform :scale="1.5">

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
layout: cover

---

# Thank you


