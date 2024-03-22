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

# Type Hints Improve Code Quality: Static Analysis

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

# Type Hints Improve Code Quality: Run-Time Validation

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

# Runtime Validation with `CallGuard`

<Transform :scale="1.25">
<v-clicks>

- Use type annotations for run-time checks
- General-purpose tools
    - `typeguard`
    - `beartype`
- `CallGuard`
    - Specialized for NumPy and StaticFrame containers
    - Handles standard Python type and collections
    - Deployed as a decorator
        - `sf.CallGuard.check`: raise `ClinicError` on failure
        - `sf.CallGuard.warn`: issue a warning on failure

</v-clicks>
</Transform>


---

# Type Hints Improve Code Quality: Run-Time Validation

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

# Type Hinting Collections

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

# Type Hinting NumPy Arrays: Generic Arguments

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

# Type Hinting NumPy Arrays: Generic Arguments

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

# Type Hints with NumPy Arrays: Examples

<Transform :scale="1.5">

```python

def process(v, q): ...

def process(
        v: np.ndarray[tp.Any, np.dtype[np.int8]],
        q: np.ndarray[tp.Any, np.dtype[np.bool_]],
        ) -> np.ndarray[tp.Any, np.float64]: ...

def process(v, q):
    assert v.dtype == np.int64
    assert q.dtype == np.bool_

    result = ...
    assert result.dtype == np.float64
    return result

@sf.CallGuard.check
def process(
        v: np.ndarray[tp.Any, np.dtype[np.int8]],
        q: np.ndarray[tp.Any, np.dtype[np.bool_]],
        ) -> np.ndarray[tp.Any, np.float64]: ...

```
</Transform>



---

# Practical Type Hints with NumPy Arrays

<Transform :scale="1.5">
<v-clicks>

- Ignore shape parameter for now
- Create domain-specific type aliases of `np.ndarray` specifications
    - `TNDArrayBool = np.ndarray[tp.Any, np.dtype[np.bool_]]`
    - `TNDArrayFloat64 = np.ndarray[tp.Any, np.dtype[np.float64]]`
- Use `sf.CallGuard.check` for run-time validation
- Use `sf.Require.Shape()` for run-time shape validation

</v-clicks>
</Transform>


---

# Practical Type Hints with NumPy Arrays: Examples

<Transform :scale="1.5">

```python

TNDArrayBool = np.ndarray[tp.Any, np.dtype[np.bool_]]
TNDArrayFloat64 = np.ndarray[tp.Any, np.dtype[np.float64]]
TNDArrayInt8 = np.ndarray[tp.Any, np.dtype[np.float64]]

@sf.CallGuard.check
def process(
        v: TNDArrayInt8,
        q: TNDArrayBool,
        ) -> TNDArrayFloat64: ...


@sf.CallGuard.check
def process(
        v: tp.Annotate[TNDArrayInt8, sf.Require.Shape(24)],
        q: tp.Annotate[TNDArrayBool, sf.Require.Shape(24)],
        ) -> tp.Annotate[TNDArrayFloat64, sf.Require.Shape(24)]: ...

```
</Transform>



---

# DataFrames are Collections of Nested Types

<Transform :scale="1.5">
<v-clicks depth="3">

- Index and column labels have distinct types
- Data values are typed by column
- Interfaces rely on these types
    - Is the index a string or a date?
    - Are values all floats or integers?

</v-clicks>
</Transform>


---

# The Challenge of Typing DataFrames

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

# Type Annotations with Pandas

<Transform :scale="1.5">

```python
import pandas as pd

def process(f: pd.DataFrame) -> pd.Series: ...
```

</Transform>



---

# Third-Party Tools for Type Annotations with Pandas

<Transform :scale="1.5">
<v-clicks depth="3">

- `pandas-stubs`
    - Built from Microsoft and VirtusLabs
    - Types Pandas interfaces
    - Offers a generic `Series` but with an untyped index
    - Does not offer a generic `Frame`
- `nptyping`
    - Offers alternative generic types
    - Uses strings to document components
        - `NDArray[Shape["2, 2"], Int]`
        - `DataFrame[S["name: Str, x: Float, y: Float"]]`
- Pandera
    - Offers alternative subclasses that are generic
    - DataFrames must be defined with a Schema class
    - Assumes immutability

</v-clicks>
</Transform>



---

# Statically Typing Mutable Collections is Messy


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

# Full Generic DataFrame Specification in StaticFrame

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
---
# Thank You

<Transform :scale="1.5">


StaticFrame: https://static-frame.dev
</Transform>
