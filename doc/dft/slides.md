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

<!-- #### Christopher Ariza
#### CTO, Research Affiliates -->

<style>
h1 {font-size: 1.5em;}
</style>


<!-- ---

# About Me

<Transform :scale="1.25">
<v-clicks>

CTO at Research Affiliates

Python programmer since 2000

PhD in music composition, professor of music technology

Python for algorithmic composition, computational musicology

Since 2012, builder of financial systems in Python

Creator of StaticFrame, an alternative DataFrame library
</v-clicks>
</Transform> -->


---

# Type Hints Improve Code Quality

<Transform :scale="1.25">
<v-clicks depth="2">

- Increase maintainability
    - Code as documentation
    - Avoid relying on names or comments
- Statically verifiable type usage
    - `mypy`, Pyright
    - IDE integration and autocomplete
- Run-time validation of type
    - Avoid redundant definitions
    - Prove hints are correct

</v-clicks>
</Transform>


---

# Type Hints Are Not a Free Lunch

<Transform :scale="1.25">
<v-clicks depth="2">

- Incorrect or invalid type hints are common
    - `from __future__ import annotations` means hints are not evaluated
    - IDE will use what it can without complaint
    - A source of technical debt
- Use `mypy` or `Pyright` to at least evaluate that hints are valid
    - `mypy` offers configuration to incrementally increase strictness
    - `mypy --strict` is used here

</v-clicks>
</Transform>

---

# Typing Facilities on the Bleeding Edge

<Transform :scale="1.25">
<v-clicks depth="2">

- Many important typing utilities are only available in modern Python
- Use `typing-extensions>=4.10.0` for back-ports
- Use latest `mypy` or `Pyright` versions
- Use recent packages
    - `static-frame>=2.5.1`
    - `numpy>=1.23.5`

</v-clicks>
</Transform>

---
layout: center
---
# Elemental type hints

---

# I: Static Analysis of Type Hints: `mypy`

<Transform :scale="1.25">

```python {all|1|3-4|6-8|10-13}
def process(v, q): ... # no type information

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

# Static Analysis v Runtime Validation

<Transform :scale="1.25">
<v-clicks depth="2">

- Static type analysis is based on markup, not reality
    - Does not affect runtime performance
    - Type annotations can be wrong
- Reusing type hints for validation ensures coherence
- Runtime validation
    - May affect runtime performance
    - Within a function
    - With a decorator

</v-clicks>
</Transform>

---

# I: Runtime Validation within a Function

<Transform :scale="1.25">

```python {all|1-2|1-4|5|6-8}
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
# I: Runtime Validation with a Decorator

<Transform :scale="1.25">
<v-clicks depth="2">

- Reuse type annotations for run-time type checks
    - `typeguard`
    - `beartype`
    - `sf.CallGuard`
</v-clicks>
</Transform>


---
---
# I: Runtime Validation: `CallGuard`

<Transform :scale="1.25">
<v-clicks depth="2">

- Class within StaticFrame
- Handles standard Python types and collections
- Specialized for NumPy and StaticFrame containers
- Deployed as a decorator
    - `sf.CallGuard.check`: raise `ClinicError` on failure
    - `sf.CallGuard.warn`: issue a warning on failure

</v-clicks>
</Transform>

---
---
# I: Runtime Validation: `CallGuard`

<Transform :scale="1.25">

```python {all|1-2|1-4|5-9}
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

<Transform :scale="1.25">
<v-clicks depth="2">

- Collection types can contain other types
- Generic collections permit nested specification
    - `list[float]`
    - `tuple[tuple[int, int], tuple[str, str]]`
- Generic arguments are positional only
- NumPy 1.20 introduced generic specification of `ndarray`

</v-clicks>
</Transform>


---

# II: Type Hinting NumPy Arrays: Generic Arguments

<Transform :scale="1.25">
<v-clicks depth="2">

- Generic `np.ndarray` takes two arguments
    - Shape
    - `dytpe`
- N-dimensional float array: `np.ndarray[tp.Any, np.dtype[np.float64]]`

</v-clicks>
</Transform>

---

# II: Type Hinting NumPy Arrays: Generic Arguments

<Transform :scale="1.25">
<v-clicks depth="2">

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

<Transform :scale="1.25">
<v-clicks depth="2">

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

```python {all|1|2|3|5-6|5-7|5-8|5-9|5-10}
TNDArrayBool = np.ndarray[tp.Any, np.dtype[np.bool_]]
TNDArrayInt8 = np.ndarray[tp.Any, np.dtype[np.int8]]
TNDArrayFloat64 = np.ndarray[tp.Any, np.dtype[np.float64]]

def process1(
        v: TNDArrayInt8,
        q: TNDArrayBool,
        ) -> TNDArrayFloat64:
    s = np.where(q, 0.5, 0.25)
    return tp.cast(TNDArrayFloat64, v * s)
```
</Transform>


---

# II: Typing NumPy Arrays: Static Analysis

<Transform :scale="1.25">

```python {all|1-4|6-10|12-}
v1: TNDArrayInt8 = np.arange(20, dtype=np.int8)
x = process1(v1, v1)
# tp_np.py: error: Argument 2 to "process1" has incompatible type
# "ndarray[Any, dtype[floating[_64Bit]]]"; expected "ndarray[Any, dtype[bool_]]"  [arg-type]

v2: np.ndarray[tp.Any, np.dtype[np.int64]] = np.arange(20, dtype=np.int64)
q: TNDArrayBool = np.arange(20) % 3 == 0
x = process1(v2, q)
# tp_np.py: error: Argument 1 to "process1" has incompatible type
# "ndarray[Any, dtype[signedinteger[_64Bit]]]"; expected "ndarray[Any, dtype[signedinteger[_8Bit]]]"  [arg-type]

y: TNDArrayBool = process1(v1, q)
# tp_np.py: error: Incompatible types in assignment (expression has type
# "ndarray[Any, dtype[floating[_64Bit]]]", variable has type "ndarray[Any, dtype[bool_]]")  [assignment]
```
</Transform>

---

# II: More with NumPy `generic`

<Transform :scale="1.25">
<v-clicks depth="2">

- Can specify integers independent of size
    - `np.signedinteger[tp.Any]`
    - `np.unsignedinteger[tp.Any]`
    - `np.integer[tp.Any]`
- Can specify inexact independent of size
    - `np.floating[tp.Any]`
    - `np.complexfloating[tp.Any, tp.Any]`
    - `np.inexact[tp.Any]`
- Any type of number: `np.number[tp.Any]`

</v-clicks>
</Transform>



---

# II: Typing NumPy Arrays: Static Analysis

<Transform :scale="1.25">

```python {all|1|2-7|6-10|11|11-}
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
# tp_np.py: error: Argument 1 to "process2" has incompatible type
# "ndarray[Any, dtype[floating[_64Bit]]]";
# expected "ndarray[Any, dtype[signedinteger[Any]]]"  [arg-type]
```
</Transform>


---

# II: Typing NumPy Arrays: Runtime Validation

<Transform :scale="1.25">

```python {all|1|1-4|6-7|8|8-}
@sf.CallGuard.check
def process3(v: TNDArrayIntAny, q: TNDArrayBool) -> TNDArrayFloat64:
    s = np.where(q, 0.5, 0.25)
    return tp.cast(TNDArrayFloat64, v * s)

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
<v-clicks depth="2">

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
<v-clicks depth="2">

- `tp.Annotated` permits arbitrary objects to be bundled with type annotations
- `sf.Require` Deployed within `tp.Annotated`
    - `TNDArrayInt8` -> `tp.Annotated[TNDArrayInt8, sf.Require.Len(24)]`
    - `TNDArrayFloat64` -> `tp.Annotated[TNDArrayInt8, sf.Require.Shape(..., 4)]`
</v-clicks>
</Transform>


---

# II: Runtime Validation with `sf.Require`

<Transform :scale="1.25">

```python {all|1|1-5|1-7|9-}
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
```
</Transform>





---
layout: center
---
# Type hinting DataFrames


---

# III: DataFrames are Collections of Nested Types

<Transform :scale="1.25">
<v-clicks depth="2">

- Data values are typed by column
- Index and column labels have distinct types
- Interfaces rely on these types
    - Is the index a string or a date?
    - Are values all floats or integers?

</v-clicks>
</Transform>


---

# III: The Challenge of a Generic DataFrame

<Transform :scale="1.25">
<v-clicks depth="2">

- A DataFrame has a variable number of columns (and thus types)
    - Requires a variadic generic: `TypeVarTuple`
        - First released in Python 3.11
        - Backward compatibility available with `typing-extensions`
    - Hierarchical indices also require variadic types
- StaticFrame offers the first fully generic DataFrame
    - Supported by an immutable data model
    - Builds on NumPy's generic specification
- Pandas does not support generic specification

</v-clicks>
</Transform>


---

# III: Third-Party Tools for Typing Pandas

<Transform :scale="1.25">
<v-clicks depth="3">

- Many third-party approaches to typing Pandas
- `pandas-stubs`
    - Built from Microsoft and VirtusLabs
    - Offers a generic `Series` but with an untyped index
    - Does not offer a generic `Frame`
- `nptyping`
    - Offers alternative generic types
    - Uses strings to define components
        - `NDArray[Shape["2, 2"], Int]`
        - `DataFrame[S["name: Str, x: Float, y: Float"]]`

</v-clicks>
</Transform>


---

# III: Third-Party Tools for Typing Pandas

<Transform :scale="1.25">
<v-clicks depth="3">

- Pandera
    - Offers alternative subclasses that are generic
    - DataFrames must be defined with a Schema class
    - Pretends Pandas DataFrames are immutable
- Even if third-party tools exist, is it sensible?

</v-clicks>
</Transform>


---

# III: Statically Typing Mutable Collections is Messy

<Transform :scale="1.25">

```python {all|1|2-3|4|5-6|7|8-|all}
>>> s: Series[np.int64] = pd.Series([10, 20, 30])
>>> s.dtype
dtype('int64')
>>> s[2] = 30.5
>>> s.dtype
dtype('float64')
>>> s[1] = False
>>> s.dtype
dtype('O')
```

</Transform>


---

# III: Pandas Only Permits Shallow DataFrame Typing

<Transform :scale="1.25">

```python
import pandas as pd

def process(v: pd.DataFrame, q: pd.Series) -> pd.Series: ...
```

</Transform>


---

# III: StaticFrame Offers Deep DataFrame Typing

<Transform :scale="1.25">

```python {all|1|2-2|2-3|2-4|2-5|2-7|8|8-9|8-11|12|12-13|12-14|all}
def process(
    v: sf.Frame[
        sf.IndexDate,      # type of Frame index labels
        sf.Index[np.str_], # type of Frame column labels
        np.int64,          # type of Frame first column
        np.int64,          # type of Frame second column
        ],
    q: sf.Series[
        sf.IndexYearMonth, # type of Series index labels
        np.bool_,          # type of Series values
        ],
    ) -> Series[
        sf.IndexDate,      # type of Series in0dex labels
        np.float64,        # type of Series values
        ]: ...
```
</Transform>


---

# III: Generic Containers in StaticFrame

<Transform :scale="1.25">
<v-clicks depth="2">

- Generic `sf.Frame` takes at least two arguments
    - Index type
    - Columns type
    - Zero or more columnar value types
- Generic `sf.Series` take two arguments
    - Index type
    - Value type
- Generic `sf.Index` take one argument: value type
- `datetime64` indices do not require arguments: `sf.IndexDate`
- Generic `sf.IndexHierarchy` take one or more `sf.Index` arguments

</v-clicks>
</Transform>


---
layout: center
---
# But this is too complex!


---

# III: Managing Type Complexity

<Transform :scale="1.25">
<v-clicks depth="2">

- Reduce the complexity of your interfaces!
- Use type aliases
    - `TSeriesDFloat = sf.Series[sf.IndexDate, np.float64]`
    - `TFrameDateNums = sf.Frame[sf.IndexDate, sf.Index[np.str_], *tuple[np.number[tp.Any], ...]]`
- Use "any" aliases
    - `sf.TFrameAny`
    - `sf.TSeriesAny`
- Discover the type annotation from the container: `via_type_clinic`

</v-clicks>
</Transform>


---

# III: Discovering Annotations from Containers

<Transform :scale="1.25">

```python {all|1-2|3-12|14-}
>>> v1 = sf.Frame.from_fields([range(5), np.arange(3, 8) * 0.5],
columns=('a', 'b'), index=sf.IndexDate.from_date_range('2021-12-30', '2022-01-03'))
>>> v1
<Frame>
<Index>         a       b         <<U1>
<IndexDate>
2021-12-30      0       1.5
2021-12-31      1       2.0
2022-01-01      2       2.5
2022-01-02      3       3.0
2022-01-03      4       3.5
<datetime64[D]> <int64> <float64>

# get a string representation of the annotation
>>> v1.via_type_clinic
Frame[IndexDate, Index[str_], int64, float64]
```
</Transform>

---

# III: Discovering Annotations from Containers

<Transform :scale="1.25">

```python {all}
# get type objects
>>> v1.via_type_clinic.to_hint()
static_frame.core.frame.Frame[static_frame.core.index_datetime.IndexDate,
static_frame.core.index.Index[numpy.str_], numpy.int64, numpy.float64]
```
</Transform>


---

# III: Checking Types at Runtime

<Transform :scale="1.25">

```python {all|1-2|4-}
>>> v2 = sf.Frame.from_fields([range(5), range(3, 8)],
columns=('a', 'b'), index=sf.IndexDate.from_date_range('2021-12-30', '2022-01-03'))

# can validate v1 against the hint of v2
>>> v1.via_type_clinic.check(v2.via_type_clinic.to_hint())
static_frame.core.type_clinic.ClinicError:
In Frame[IndexDate, Index[str_], int64, int64]
└── Expected int64, provided float64 invalid
```
</Transform>


---
layout: center
---
# Fully typed DataFrame interfaces



---

# III: Typed DataFrame Interfaces

<Transform :scale="1.25">

```python {all|1|2|3|5-8|5-6|5-7|5-8}
TFrameDateInts = sf.Frame[sf.IndexDate, sf.Index[np.str_], np.int64, np.int64]
TSeriesYMBool = sf.Series[sf.IndexYearMonth, np.bool_]
TSeriesDFloat = sf.Series[sf.IndexDate, np.float64]

def process1(v: TFrameDateInts, q: TSeriesYMBool) -> TSeriesDFloat:
    t = v.index.iter_label().apply(lambda l: q[l.astype('datetime64[M]')]) # type: ignore
    s = np.where(t, 0.5, 0.25)
    return tp.cast(TSeriesDFloat, (v.via_T * s).mean(axis=1))
```
</Transform>


---

# III: Typed DataFrame Static Analysis: `mypy`

<Transform :scale="1.25">

```python {all|1-2|4-}
q: TSeriesYMBool = sf.Series([True, False],
index=sf.IndexYearMonth.from_date_range('2021-12', '2022-01'))

x = process1(q, q)
# tpst_frame.py: error: Argument 1 to "process1" has incompatible type
# "Series[IndexYearMonth, bool_]"; expected
# "Frame[IndexDate, Index[str_], signedinteger[_64Bit], signedinteger[_64Bit]]"  [arg-type]
```
</Transform>


---

# III: Typed DataFrame Static Analysis: `mypy`

<Transform :scale="1.25">

```python {all|1-2|1-4|6-9|11-12|14}
# a Frame with an int and float column
TFrameDateIntFloat = sf.Frame[sf.IndexDate, sf.Index[np.str_], np.int64, np.float64]
v1: TFrameDateIntFloat = sf.Frame.from_fields([range(5), np.arange(3, 8) * 0.5],
columns=('a', 'b'), index=sf.IndexDate.from_date_range('2021-12-30', '2022-01-03'))

x = process1(v1, q)
# tpst_frame.py: error: Argument 1 to "process1" has incompatible type
# "Frame[IndexDate, Index[str_], signedinteger[_64Bit], floating[_64Bit]]"; expected
# "Frame[IndexDate, Index[str_], signedinteger[_64Bit], signedinteger[_64Bit]]"  [arg-type]

v2: TFrameDateInts = sf.Frame.from_fields([range(5), range(3, 8)],
columns=('a', 'b'), index=sf.IndexDate.from_date_range('2021-12-30', '2022-01-03'))

x = process1(v2, q) # no mypy error
```
</Transform>


---

# III: Using Type Hints for Runtime Validation

<Transform :scale="1.25">
<v-clicks depth="3">

- The same type hints can be used for run-time validation
- Deploy with the `sf.CallGuard.check` decorator
- Runtime validations can be extended with `sf.Require`

</v-clicks>
</Transform>


---

# III: DataFrame Runtime Validation: `CallGuard`

<Transform :scale="1.25">

```python {all|1-2|4-8|10-}
# define columns as any type of number
TFrameDateNum = sf.Frame[sf.IndexDate, sf.Index[np.str_], np.number[tp.Any], np.number[tp.Any]]

@sf.CallGuard.check
def process3(v: TFrameDateNum, q: TSeriesYMBool) -> TSeriesDFloat:
    t = v.index.iter_label().apply(lambda l: q[l.astype('datetime64[M]')]) # type: ignore
    s = np.where(t, 0.5, 0.25)
    return tp.cast(TSeriesDFloat, (v.via_T * s).mean(axis=1))

# no mypy error with floats or ints
x = process3(v1, q)
x = process3(v2, q)
```
</Transform>


---

# III: DataFrame Runtime Validation: `CallGuard`

<Transform :scale="1.25">

```python {all|1-2|4-5|7-}
# a Frame of three columns of integers
TFrameDateIntIntInt = sf.Frame[sf.IndexDate, sf.Index[np.str_], np.int64, np.int64, np.int64]

v3: TFrameDateIntIntInt = sf.Frame.from_fields([range(5), range(3, 8), range(1, 6)],
columns=('a', 'b', 'c'), index=sf.IndexDate.from_date_range('2021-12-30', '2022-01-03'))

x = process3(v3, q)
# static_frame.core.type_clinic.ClinicError:
# In args of (v: Frame[IndexDate, Index[str_], number[Any], number[Any]],
# q: Series[IndexYearMonth, bool_]) -> Series[IndexDate, float64]
# └── Frame[IndexDate, Index[str_], number[Any], number[Any]]
#     └── Expected Frame has 2 dtype, provided Frame has 3 dtype
```
</Transform>


---
layout: center
---
# But what if variable column counts is appropriate?


---

# III: Expressive Usage of `TypeVarTuple`

<Transform :scale="1.25">
<v-clicks depth="3">

- Many ways to provide type arguments to a `TypeVarTuple` region
- A variadic generic means a variable numbers of args
    - `Frame[IndexDate, Index[str_], int64]`
    - `Frame[IndexDate, Index[str_], int64, int64, int64, bool_, float64`

</v-clicks>
</Transform>

---

# III: Expressive Usage of `TypeVarTuple`

<Transform :scale="1.25">
<v-clicks depth="3">

- What if we want to be flexible regarding number of columns?
- Using `Unpack`
    - A syntax to define a region of zero or more of the same type
    - Python 3.11: `*tuple[int64, ...]`
    - Pre 3.11: `Unpack[tuple[int64, ...]]`

</v-clicks>
</Transform>

---

# III: Expressive Usage of `Unpack`

<Transform :scale="1.25">
<v-clicks depth="3">

- A single `Unpack` can express zero or more columns of the same type
    - `Frame[IndexDate, Index[str_], *tuple[int64, ...]]`
- Can combine explicit types with one `Unpack`
    - `Frame[IndexDate, Index[str_], bool_, *tuple[int64, ...]]`
    - `Frame[IndexDate, Index[str_], *tuple[int64, ...], float64]`

</v-clicks>
</Transform>



---

# III: DataFrame Runtime Validation: `CallGuard`

<Transform :scale="1.25">

```python {all|1-2|4|4-8|10-}
# define a Frame with 0 or more numerical columns
TFrameDateNums = sf.Frame[sf.IndexDate, sf.Index[np.str_], *tuple[np.number[tp.Any], ...]]

@sf.CallGuard.check
def process4(v: TFrameDateNums, q: TSeriesYMBool) -> TSeriesDFloat:
    t = v.index.iter_label().apply(lambda l: q[l.astype('datetime64[M]')]) # type: ignore
    s = np.where(t, 0.5, 0.25)
    return tp.cast(TSeriesDFloat, (v.via_T * s).mean(axis=1))

# a Frame with three integer columns passes
x = process4(v3, q)
```
</Transform>


---

# III: Extended Runtime Validation

<Transform :scale="1.25">
<v-clicks depth="3">

- If already checking types, why not other attributes?
- Can use `tp.Annotated` to bundle `sf.Require`-defined checks

</v-clicks>
</Transform>


---

# III: DataFrame Runtime Validation: `CallGuard` and `Require`

<Transform :scale="1.25">

```python {all|1|2|2-3|2-4|5|5-6|5-7|8|all}
TFrameDateNumsValid = sf.Frame[
    tp.Annotated[
        sf.IndexDate,                           # type of Frame index labels
        sf.Require.Len(10)],                    # require length of 10
    tp.Annotated[
        sf.Index[np.str_],                      # type of Frame column labels
        sf.Require.LabelsOrder('a', 'b', ...)], # require first two labels to be 'a', 'b'
    *tuple[np.number[tp.Any], ...]              # type of Frame columns
    ]

```
</Transform>


---

# III: DataFrame Runtime Validation: `CallGuard` and `Require`

<Transform :scale="1.25">

```python {all|1|1-5|7-}
@sf.CallGuard.check
def process5(v: TFrameDateNumsValid, q: TSeriesYMBool) -> TSeriesDFloat:
    t = v.index.iter_label().apply(lambda l: q[l.astype('datetime64[M]')]) # type: ignore
    s = np.where(t, 0.5, 0.25)
    return tp.cast(TSeriesDFloat, (v.via_T * s).mean(axis=1))

x = process5(v3, q)
# static_frame.core.type_clinic.ClinicError:
# In args of (v: Frame[Annotated[IndexDate, Len(10)], Index[str_], Unpack[tuple[number[Any], ...]]], q: Series[IndexYearMonth, bool_]) -> Series[IndexDate, float64]
# └── Frame[Annotated[IndexDate, Len(10)], Index[str_], Unpack[tuple[number[Any], ...]]]
#     └── Annotated[IndexDate, Len(10)]
#         └── Len(10)
#             └── Expected length 10, provided length 5
```
</Transform>



---

# Conclusion

<Transform :scale="1.25">
<v-clicks depth="3">

✨ Type annotations improve code quality

🔎 If you write type hints, check them

♻️ Reuse type-hints for run-time validation with `sf.CallGuard`

🛡️ Extend run-time validation with `sf.Require`

⚠️ Pandas mutability makes static typing unreliable at best

🗜️ StaticFrame's immutable data model supports static typing

</v-clicks>
</Transform>



---

# Thank You

<Transform :scale="1.25">

StaticFrame: https://static-frame.dev
</Transform>


