---
theme: default
class: text-center
highlighter: shiki
lineNumbers: false
transition: slide-left
aspectRatio: 16/9
favicon: /favicon.ico
title: "Unlocking Complete DataFrame Type Hints with Python 3.11's `TypeVarTuple`"

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

<Transform :scale="1.5">
<v-clicks>

- Increase maintainability
    - Code as documentation
    - Avoid relying on variable name or comments
- Statically verifiable type usage
    - mypy, Pyright
    - IDE integration / autocomplete
- Run-time validation
    - DRY: avoid redundant validations
    - Prove hints are run-time correct

</v-clicks>
</Transform>


---

# Type Hints Improve Code Quality: Examples

<Transform :scale="1.5">

```python

def process(v, q): ...

def process(v: int, q: bool) -> list[float]: ...

def process(v, q):
    assert isinstance(v, int)
    assert isinstance(q, bool)

    result = ...
    assert isinstance(result, list)
    assert all(isinstance(x, float) for x in result)
    return result

@sf.CallGuard.check
def process(v: int, q: bool) -> list[float]: ...

```
</Transform>


---

# Type Hints with NumPy Arrays

<Transform :scale="1.5">
<v-clicks>

- Collection types can contain other types
- Generic typed collections permit nested specification
    - `list[str]`
    - `tuple[tuple[int, int], tuple[str, str]]`
- `ndarray` supported Generic specification with NumPy 1.20

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

# Type Hints with NumPy Arrays: Generic Arguments

<Transform :scale="1.5">
<v-clicks>

- Generic `np.ndarray` take two arguments
    - Shape
    - `dytpe`
- Shape is placeholder for a future shape definition
    - Might use `tp.Literal[4]` for 1D specfication
    - Might use `tuple[tp.Literal[4], tp.Literal[12]]` for 2D specfication
    - Shape is often a run-time concern
- `dtype` is generic, and requires a NumPy "generic" as an argument
- `np.typing.NDArray[]` is a single-argument shortcut

</v-clicks>
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

# DataFrames are Nested Data Structures

<Transform :scale="1.5">
<v-clicks depth="3">

- Index and column labels have distinct types
- Data values are typed by column
- << diagram? >>
- Interfaces rely on these types
    - Is the index a string or a date?
    - Are values all floats or integers

</v-clicks>
</Transform>


---

# The Common Approach

<Transform :scale="1.5">


```python
import pandas as pd

def process(f: pd.DataFrame) -> pd.Series: ...
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

# The Problem of Typing DataFrames

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

<!--
>>> df = pd.DataFrame([[True, 4], [False, 2]])
>>> df.dtypes.values.tolist()
[dtype('bool'), dtype('int64')]
>>> df[2] = (1.2, 5.3)
>>> df.dtypes.values.tolist()
[dtype('bool'), dtype('int64'), dtype('float64')]
>>> df.iloc[0, 0] = -1
>>> df.dtypes.values.tolist()
[dtype('O'), dtype('int64'), dtype('float64')]
-->







---
---
# Thank You

<Transform :scale="1.5">


StaticFrame: https://static-frame.dev
</Transform>
