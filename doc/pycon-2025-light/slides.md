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

<div class="bg-black bg-opacity-80 p-4 rounded-xl text-white">

# Doing More with Your NumPy Type Annotation

<br />
<br />

#### Christopher Ariza
#### CTO, Research Affiliates

</div>

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
    x: np.ndarray[tuple[Any, Any], np.dtype[np.floating]],
    y: np.ndarray[tuple[Any], np.dtype[np.bool_]],
    ) -> np.ndarray[tuple[Any, Any], np.dtype[np.float64]]: ...
```
</Transform>



---

# The Generic `np.ndarray`

<Transform :scale="1.25">
<v-clicks>

* Two arguments
    * shape
    * dtype
* until NumPy 2.1:
    ```python
    np.ndarray[Any, np.dtype[np.int8]]
    ```
* from NumPy 2.1:
    ```python
    np.ndarray[tuple[Any, ...], np.dtype[np.int8]]
    ```
</v-clicks>
</Transform>



---

# Dtypes are Generic


<Transform :scale="1.25">

```python {1-3|4|5|6}
import numpy as np

np.dtype[np.int8]
np.dtype[np.integer]
np.dtype[np.floating]
np.dtype[np.number]

```
</Transform>


---

# Shapes are Generic


<Transform :scale="1.25">

```python {1|2|3|4}
tuple[Any, ...]
tuple[Any]
tuple[Any, Any]
tuple[Literal[20], Any]

```
</Transform>



---

# Concretizing `np.ndarray`


<Transform :scale="1.25">

```python {all}

def process(x: np.ndarray[tp.Any, np.dtype[np.uint8]]): ...
```
</Transform>







---
layout: cover
background: /IMG_4390.jpg

---
<div class="bg-black bg-opacity-80 p-4 rounded-xl text-white">

# Thank you

</div>

