---
theme: default
class: text-center
highlighter: shiki
lineNumbers: false
transition: slide-left
aspectRatio: 16/9
favicon: /favicon.ico
title: "Improving Code Quality with Array and DataFrame Type Hints"

---

# Improving Code Quality with Array and DataFrame Type Hints

### Christopher Ariza
### CTO, Research Affiliates

<style>
h1 {font-size: 1.5em;}
</style>


---

# About Me

<Transform :scale="1.5">
<v-clicks>

CTO at Research Affiliates

Python programmer since 2000

PhD in music composition, professor of music technology

Python for algorithmic composition, computational musicology

Since 2012, builder of financial systems in Python

Creator of StaticFrame, an alternative DataFrame library
</v-clicks>
</Transform>


---

# Type Hints Improve Code Quality

<Transform :scale="1.25">
<v-clicks>

- Increase maintainability
    - Code as documentation
    - Avoid relying on variable name or comments
- Statically verifiable type usage
    - mypy (1.9), Pyright
    - IDE integration / autocomplete
- Run-time validation
    - DRY: avoid redundant validations
    - Prove hints are correct

</v-clicks>
</Transform>



---
layout: center
---
# Simple Type hints



---

# I: Static Analysis of Type Hints

<Transform :scale="1.25">

```python

def process(v, q): ...

# adding type hints
def process(v: int, q: bool) -> list[float]: ...

x = process(v=5, q=20)
# tp_basic.py: error: Argument "q" to "process"
# has incompatible type "int"; expected "bool"  [arg-type]

y: tp.Sequence[int] = process(v=5, q=False)
# tp_basic.py: error: Incompatible types in assignment
# (expression has type "list[float]", variable has type
# "Sequence[int]")  [assignment]
```

</Transform>


---

# I: Runtime Validation

<Transform :scale="1.25">

```python
# adding run-time type checks
def process(v, q):
    assert isinstance(v, int)
    assert isinstance(q, bool)
    result = [x * (0.5 if q else 0.25) for x in range(v)]
    assert isinstance(result, list)
    assert all(isinstance(x, float) for x in result)
    return result
```
</Transform>


---
---
# I: Runtime Validation with `CallGuard`

<Transform :scale="1.25">
<v-clicks>

- Use type annotations for run-time checks
- General-purpose tools
    - `typeguard`
    - `beartype`
- `CallGuard`
    - Specialized for NumPy and StaticFrame containers
    - Handles standard Python types and collections
    - Deployed as a decorator
        - `sf.CallGuard.check`: raise `ClinicError` on failure
        - `sf.CallGuard.warn`: issue a warning on failure

</v-clicks>
</Transform>


---
---
# I: Runtime Validation

<Transform :scale="1.25">

```python

# runtime type checks with CallGuard
@sf.CallGuard.check
def process(v: int, q: bool) -> list[float]:
    return [x * (0.5 if q else 0.25) for x in range(v)]

z = process(v=6, q='foo')
# static_frame.core.type_clinic.ClinicError:
# In args of (v: int, q: bool) -> list[float]
# └── Expected bool, provided int invalid

```
</Transform>




---
layout: center
---
# Type-hinting generic arrays



---

# II: Type Hinting Collections

<Transform :scale="1.5">
<v-clicks>

- Collection types can contain other types
- Generic typed collections permit nested specification
    - `list[float]`
    - `tuple[tuple[int, int], tuple[str, str]]`
- Generic arguments are positional only
- `ndarray` supported Generic specification with NumPy 1.20

</v-clicks>
</Transform>


---

# II: Type Hinting NumPy Arrays: Generic Arguments

<Transform :scale="1.25">
<v-clicks>

- Generic `np.ndarray` take two arguments
    - Shape
    - `dytpe`
    - `np.ndarray[tp.Any, np.dtype[np.float64]]`
- `np.typing.NDArray[]`
    - A single-argument shortcut
    - Only requires dtype

</v-clicks>
</Transform>

---

# II: Type Hinting NumPy Arrays: Generic Arguments

<Transform :scale="1.25">
<v-clicks>

- Shape is placeholder for a future shape definition
    - Might use `tp.Literal[4]` for 1D specfication
    - Might use `tuple[tp.Literal[4], tp.Literal[12]]` for 2D specification
    - Shape is often a run-time concern
- `dtype` is itself generic
    - A NumPy "generic" is the generic argument
    - Might use `np.dytpe[np.integer]` for any integer type
    - Might use `np.dtype[np.uint8]` for a narrow specified integer

</v-clicks>
</Transform>


---

# II: Type Hinting NumPy Arrays: Practical Approaches

<Transform :scale="1.5">
<v-clicks>

- Ignore shape parameter with `tp.Any`
- Create type aliases of `np.ndarray` generics
    - `TNDArrayBool = np.ndarray[tp.Any, np.dtype[np.bool_]]`
    - `TNDArrayFloat64 = np.ndarray[tp.Any, np.dtype[np.float64]]`
    - `TNDArrayIntAny = np.ndarray[tp.Any, np.dtype[np.signedinteger[tp.Any]]]`

</v-clicks>
</Transform>


---

# II: Typing NumPy Arrays: Static Analysis

<Transform :scale="1.25">

```python
TNDArrayBool = np.ndarray[tp.Any, np.dtype[np.bool_]]
TNDArrayInt8 = np.ndarray[tp.Any, np.dtype[np.int8]]
TNDArrayFloat64 = np.ndarray[tp.Any, np.dtype[np.float64]]

def process1(
        v: TNDArrayInt8,
        q: TNDArrayBool,
        ) -> TNDArrayFloat64:
    r = np.where(q, 0.5, 1)
    s = np.where(q, 1, 0.25)
    return tp.cast(TNDArrayFloat64, v * r * s)
```
</Transform>


---

# II: Typing NumPy Arrays: Static Analysis

<Transform :scale="1.25">

```python
def process1(v: TNDArrayInt8, q: TNDArrayBool) -> TNDArrayFloat64: ...

v1: TNDArrayInt8 = np.arange(20, dtype=np.int8)
x = process1(v1, v1)
# tp_np.py: error: Argument 2 to "process1" has incompatible type "ndarray[Any, dtype[floating[_64Bit]]]"; expected "ndarray[Any, dtype[bool_]]"  [arg-type]

v2: np.ndarray[tp.Any, np.dtype[np.int64]] = np.arange(20, dtype=np.int64)
q: TNDArrayBool = np.arange(20) % 3 == 0
x = process1(v2, q)
# tp_np.py: error: Argument 1 to "process1" has incompatible type "ndarray[Any, dtype[signedinteger[_64Bit]]]"; expected "ndarray[Any, dtype[signedinteger[_8Bit]]]"  [arg-type]

y: TNDArrayBool = process1(v1, q)
# tp_np.py: error: Incompatible types in assignment (expression has type "ndarray[Any, dtype[floating[_64Bit]]]", variable has type "ndarray[Any, dtype[bool_]]")  [assignment]
```
</Transform>


---

# II: Typing NumPy Arrays: Static Analysis

<Transform :scale="1.25">

```python
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
v3: TNDArrayFloat64 = np.arange(20, dtype=np.float64) * 0.5
x = process2(v3, q)
# tp_np.py: error: Argument 1 to "process2" has incompatible type
# "ndarray[Any, dtype[floating[_64Bit]]]";
# expected "ndarray[Any, dtype[signedinteger[Any]]]"  [arg-type]
```
</Transform>


---

# II: Typing NumPy Arrays: Runtime Validation

<Transform :scale="1.25">

```python
@sf.CallGuard.check
def process3(
        v: TNDArrayIntAny,
        q: TNDArrayBool,
        ) -> TNDArrayFloat64:
    r = np.where(q, 0.5, 1)
    s = np.where(q, 1, 0.25)
    return tp.cast(TNDArrayFloat64, v * r * s)

x = process3(v1, q)
x = process3(v2, q)
v3: TNDArrayFloat64 = np.arange(20, dtype=np.float64) * 0.5
x = process3(v3, q)
# static_frame.core.type_clinic.ClinicError:
# In args of (v: ndarray[Any, dtype[signedinteger[Any]]], q: ndarray[Any, dtype[bool_]]) -> ndarray[Any, dtype[float64]]
# └── ndarray[Any, dtype[signedinteger[Any]]]
#     └── dtype[signedinteger[Any]]
#         └── Expected signedinteger, provided float64 invalid
```
</Transform>


---

# II: Extending Runtime Validation: `sf.Require`

<Transform :scale="1.25">
<v-clicks>

- Shape and other characteristics can be validated at run time.
- `sf.Require` provides a family of validators
    - `sf.Require.Len`
    - `sf.Require.Shape`
    - `sf.Require.Apply`
    - `sf.Require.Name`
    - `sf.Require.LabelsMatch`
    - `sf.Require.LabelsOrder`
</v-clicks>
</Transform>


---

# II: Extending Runtime Validation: `tp.Annotated`

<Transform :scale="1.25">
<v-clicks>

- `tp.Annotated` permits arbitrary objects to be bundled with type annotations
- `sf.Require` Deployed within `tp.Annotated`
    - `TNDArrayInt8` -> `tp.Annotated[TNDArrayInt8, sf.Require.Len(24)]`
    - `TNDArrayFloat64` -> `tp.Annotated[TNDArrayInt8, sf.Require.Shape(..., 4)]`
</v-clicks>
</Transform>


---

# II: Runtime Validation with `sf.Require`

<Transform :scale="1.25">

```python
@sf.CallGuard.check
def process4(
        v: tp.Annotated[TNDArrayInt8, sf.Require.Shape(24)],
        q: tp.Annotated[TNDArrayBool, sf.Require.Shape(24)],
        ) -> tp.Annotated[TNDArrayFloat64, sf.Require.Shape(24)]:
    r = np.where(q, 0.5, 1)
    s = np.where(q, 1, 0.25)
    return tp.cast(TNDArrayFloat64, v * r * s)

x = process4(v1, q)
# static_frame.core.type_clinic.ClinicError:
# In args of (v: Annotated[ndarray[Any, dtype[int8]], Shape((24,))], q: Annotated[ndarray[Any, dtype[bool_]], Shape((24,))]) -> Annotated[ndarray[Any, dtype[float64]], Shape((24,))]
# └── Annotated[ndarray[Any, dtype[int8]], Shape((24,))]
#     └── Shape((24,))
#         └── Expected shape ((24,)), provided shape (20,)
```
</Transform>





---
layout: center
---
# Type hinting DataFrames



---

# III: DataFrames are Collections of Nested Types

<Transform :scale="1.5">
<v-clicks depth="3">

- Data values are typed by column
- Index and column labels have distinct types
- Interfaces rely on these types
    - Is the index a string or a date?
    - Are values all floats or integers?

</v-clicks>
</Transform>


---

# III: The Challenge of Typing DataFrames

<Transform :scale="1.5">
<v-clicks>

- A DataFrame has a variable number of columns (and thus types)
- Requires a variadic generic: `TypeVarTuple`
- Hierarchical indices also require variadic types
- In-place mutation (as in Pandas) negates static typing
    - Adding columns adds types
    - In-place mutation can change a columnar type
- Static typing benefits from immutability

</v-clicks>
</Transform>



---

# III: Type Annotations with Pandas

<Transform :scale="1.5">

```python
import pandas as pd

def process(f: pd.DataFrame) -> pd.Series: ...
```

</Transform>



---

# III: Third-Party Tools for Typing Pandas

<Transform :scale="1.25">
<v-clicks depth="3">

- `pandas-stubs`
    - Built from Microsoft and VirtusLabs
    - Offers a generic `Series` but with an untyped index
    - Does not offer a generic `Frame`
- `nptyping`
    - Offers alternative generic types
    - Uses strings to document components
        - `NDArray[Shape["2, 2"], Int]`
        - `DataFrame[S["name: Str, x: Float, y: Float"]]`

</v-clicks>
</Transform>


---

# III: Third-Party Tools for Typing Pandas

<Transform :scale="1.5">
<v-clicks depth="3">

- Pandera
    - Offers alternative subclasses that are generic
    - DataFrames must be defined with a Schema class
    - Assumes immutability
- Even if third-party tools exist, is it sensible?

</v-clicks>
</Transform>


---

# III: Statically Typing Mutable Collections is Messy


<Transform :scale="1.5">

```python
import pandas as pd

>>> s: "Series[np.int64]" = pd.Series([10, 20, 30])
>>> s[2] = 30.5
>>> s.dtype
dtype('float64')
>>> s[1] = False
>>> s.dtype
dtype('O')
```

</Transform>



---

# III: Full Generic DataFrame Specification in StaticFrame

<Transform :scale="1.5">

```python
from typing import Any
from static_frame import Frame, Index, TSeriesAny

def process(f: Frame[   # type of the container
        Any,            # type of the index labels
        Index[np.str_], # type of the column labels
        np.int_,        # type of the first column
        np.str_,        # type of the second column
        np.float64,     # type of the third column
        ]) -> TSeriesAny: ...
```

</Transform>







---

# Thank You

<Transform :scale="1.5">

StaticFrame: https://static-frame.dev
</Transform>


