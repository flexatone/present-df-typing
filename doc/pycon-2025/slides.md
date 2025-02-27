---
theme: default
class: text-center
highlighter: shiki
lineNumbers: false
transition: slide-left
aspectRatio: 16/9
favicon: /favicon.ico
title: "Elastic Generics: Flexible Static Typing with TypeVarTuple and Unpack"

---

# Elastic Generics: Flexible Static Typing with `TypeVarTuple` & `Unpack`

<br />
<br />

#### Christopher Ariza
#### CTO, Research Affiliates

<style>
h1 {font-size: 3.3em !important; line-height: 1.3 !important;}
</style>

<!-- /NOTE: this is tested on slidev 0.50.0, 0.51 did not work! -->


---

# Type Annotations in Python


<Transform :scale="1.25">
<v-clicks>

Since Python 3.5 (PEP 484)

An optional layer, independent of run-time

Improves code quality

Statically verifiable with tools like `mypy` and `pyright`

Numerous tools for run-time usage

</v-clicks>
</Transform>

---

# Elemental & Generic Types
<Transform :scale="1.25">
<v-clicks depth="1">

Elemental types

```python
def process(
        x: int,
        y: float,
        z: bool,
        ) -> float: ...
```

Types that contain other types are generic

```python
def process(
        x: Sequence[int],
        y: tuple[tuple[str, float], ...],
        z: dict[str, bool],
        ) -> Iterator[float]: ...
```

</v-clicks>
</Transform>


---

# Generic Types
<Transform :scale="1.25">
<v-clicks depth="1">

* Generic types are made concrete with type parameters
* Can require one or more positional parameters
* Python containers are generic
    * `list[str]`
    * `set[int]`
* Python ABC's are generic
    * `Sequence[float]`
    * `Iterator[float]`
    * `Mapping[str, bool]`


</v-clicks>
</Transform>




---

# Defining Generics in Python (< 3.12)

<Transform :scale="1.25">
<v-clicks depth="1">

Subclass from `Generic`

Provide `TypeVar` to `Generic` to specify type variables

```python
TK = TypeVar('TK')
TV = TypeVar('TV')

class Map(Generic[TK, TV]):
    def keys(self) -> Iterator[TK]: ...
    def values(self) -> Iterator[TV]: ...
    def items(self) -> Iterator[tuple[TK, TV]]: ...
    def __getitem__(self, key: TK) -> TV: ...

m1 = Map[str, bool]()
v: bool = m1[next(iter(m1.keys()))]
```

</v-clicks>
</Transform>




---

# Defining Generics in Python (>= 3.12)

<Transform :scale="1.25">
<v-clicks depth="1">

```python
class Map[TK, TV]:
    def keys() -> Iterator[TK]: ...
    def values() -> Iterator[TV]: ...
    def items() -> Iterator[tuple[TK, TV]]: ...
    def __getitem__(self, key: TK) -> TV: ...
```

No longer need to subclass `Generic`

`TypeVar` defined implicitly

</v-clicks>
</Transform>



---
layout: center
---
# Can a generic component define shape or order?




---

# Asking More from our Types

<Transform :scale="1.25">
<v-clicks depth="2">

Could a `list[str]` specify a size?

Could a `Iterator[str | bool]` specify an ordering of types?

</v-clicks>
</Transform>


---

# The Dual Capability of `tuple`

<Transform :scale="1.25">
<v-clicks depth="1">

* A sequence with defined size and ordering of types
    * `tuple[str, float, float, bool]`
* An un sized sequence of homogenous types
    * `tuple[str, ...]`


</v-clicks>
</Transform>



---

# Extending `tuple` Flexibility

<Transform :scale="1.25">
<v-clicks depth="1">

* What if you need both ordering and an unbound sequence?
* A `tuple` that starts with an `int` and a `str` and follows with zero or more `float`
* A dataset of identifiers followed by variable observations

</v-clicks>
</Transform>




---

# `TypeVarTuple` and `Unpack`

<Transform :scale="1.25">
<v-clicks depth="1">

* `TypeVarTuple` & `Unpack` introduced in Python 3.11 (PEP 646)
    * Define variadic generics with tuple-like flexibility
    * Can be combined with `TypeVar`
* `Unpack` is a component and a new syntax
    * `Unpack[tuple[int, ...]]` equivalent to `*tuple[int, ...]`
    * Backwards compatibility through `typing-extensions`

</v-clicks>
</Transform>


---

# Elastic Generics with TypeVarTuple and Unpack

<Transform :scale="1.25">
<v-clicks depth="1">

1. Typing opportunities with `tuple` and `Unpack` syntax
2. Using `TypeVarTuyple` to define generic classes
3. A compelling application: generic DataFrames

</v-clicks>
</Transform>


---
layout: center
---
# Why me?


---

# About Me

<Transform :scale="1.25">
<v-clicks>

CTO at Research Affiliates

Python programmer since 2000

PhD in music composition, professor of music technology

Python for algorithmic composition, computational musicology

Since 2012, builder of financial systems in Python

Creator of StaticFrame, an alternative DataFrame library

Long pondered static typing of DataFrames
</v-clicks>
</Transform>




---
layout: center
---
# Typing opportunities with `tuple`


---

# Annotating `tuple`

<Transform :scale="1.25">
<v-clicks depth="1">

* Since 3.5: `tuple[int, ...]` and `tuple[int, str, float]`
* Since 3.11: Unpack syntax: `tuple[int, str, *tuple[float, ...]]`


</v-clicks>
</Transform>


---

# Annotating `tuple`: Sized & Ordered

<Transform :scale="1.25">
<v-clicks depth="1">

Define size and an ordering of types

```python
def process(arg: tuple[int, str, float]): ...

process((3, 'x', 4.2)) # mypy passes

process((3, 'x', 4.2, 5.2)) # mypy fails: error:
    # Argument 1 to "process" has incompatible type
    # "tuple[int, str, float, float]"; expected "tuple[int, str, float]"
```
</v-clicks>
</Transform>


---

# Annotating `tuple`: Unsized

<Transform :scale="1.25">
<v-clicks depth="1">

Define zero or more of one type

```python
def process(arg: tuple[float, ...]): ...

process((4.2, 5.8)) # mypy passes
process(()) # mypy passes
process((4.2, 5.8, 7.2)) # mypy passes

process((4.2, 5.8, 7.2, 'y')) # mypy fails: error:
    # Argument 1 to "process" has incompatible type
    # "tuple[float, float, float, str]"; expected "tuple[float, ...]"
```
</v-clicks>
</Transform>



---

# Annotating `tuple`: Sized & Ordered & Unsized

<Transform :scale="1.25">
<v-clicks depth="1">

Can define only one unsized `Unpack` region

Ordered segments can proceed and/or follow `Unpack` region

```python
def process(arg: tuple[int, str, *tuple[float, ...]]): ...

process((3, 'x', 4.2)) # mypy passes
process((3, 'x')) # mypy passes
process((3, 'x', 4.2, 5.8, 7.2)) # mypy passes

process((3, 'x', 4.2, 5.8, 7.2, None)) # mypy fails: error:
    # Argument 1 to "process" has incompatible type
    # "tuple[int, str, float, float, float, None]";
    # expected "tuple[int, str, *tuple[float, ...]]"
```

</v-clicks>
</Transform>



---

# Annotating `tuple`: Sized & Ordered & Unsized & Sized & Ordered

<Transform :scale="1.25">
<v-clicks depth="1">

Ordered segments can proceed and/or follow `Unpack` region

```python
def process(arg: tuple[int, *tuple[float, ...], str, bool]): ...

process((3, 4.2, 5.8, 'x', False)) # mypy passes
process((3, 'y', True)) # mypy passes

process((3, 'x', 4.2, 5.8, 'y', 7.2, 'x', False)) # mypy fails: error:
    # Argument 1 to "process" has incompatible type
    # "tuple[int, str, float, float, str, float, str, bool]";
    # expected "tuple[int, *tuple[float, ...], str, bool]"
```

</v-clicks>
</Transform>





---
layout: center

---

# Define generic classes `TypeVarTuple`


---

# Define generic classes `TypeVarTuple`

<Transform :scale="1.25">
<v-clicks depth="1">

For generics, one (and only one) type variable can be a `TypeVarTuple`

Normal type variables can proceed and/or follow a `TypeVarTuple`

</v-clicks>
</Transform>


---

# Generic Classes with `TypeVarTuple` and `Unpack` (< 3.12)

<Transform :scale="1.25">

```python
Ts = TypeVarTuple('Ts')
class Record(Generic[Ts]): ...

r1: Record[int, str]
r2: Record[int, str, Unpack[tuple[float, ...]]] # unpack is a component
```
</Transform>


---

# Generic Classes with `TypeVarTuple` and `Unpack` (>= 3.12)

<Transform :scale="1.25">

```python
class Record[*Ts]: ...

r1: Record[int, str]
r2: Record[int, str, *tuple[float, ...]] # unpack is star expansion
```
</Transform>


---

# 1. Annotating `Record`

<Transform :scale="1.25">

```python
class Record[*Ts]:
    def __init__(self, arg: tuple[*Ts]):
        self._store = arg

def process(arg: Record[int, str, float]): ...

process(Record((3, 'x', 4.2))) # mypy passes
process(Record((3, 'x', 4.2, 5.2))) # mypy fails: error:
    # Argument 1 to "Record" has incompatible type
    # "tuple[int, str, float, float]"; expected "tuple[int, str, float]"
```
</Transform>


---

# 2. Annotating `Record`

<Transform :scale="1.25">

```python
class Record[*Ts]:
    def __init__(self, arg: tuple[*Ts]):
        self._store = arg

def process(arg: Record[*tuple[float, ...]]): ...

process(Record((4.2, 5.2))) # mypy passes
process(Record(())) # mypy passes

process(Record((4.2, 5.2, 'x'))) # mypy fails: error:
    # Argument 1 to "Record" has incompatible type
    # "tuple[float, float, str]"; expected "tuple[float, ...]"
```
</Transform>


---

# 3. Annotating `Record`

<Transform :scale="1.25">

```python
class Record[*Ts]:
    def __init__(self, arg: tuple[*Ts]):
        self._store = arg

def process(arg: Record[int, *tuple[float, ...], str]): ...

process(Record((3, 4.2, 5.2, 'x'))) # mypy passes
process(Record((3, 'x'))) # mypy passes

process(Record((3, 4.2, 5.2, False))) # mypy fails: error:
    # Argument 1 to "Record" has incompatible type
    # "tuple[int, float, float, bool]";
    # expected "tuple[int, *tuple[float, ...], str]"
```
</Transform>


---

# Annotating `TaggedRecord`

<Transform :scale="1.25">

```python
class TaggedRecord[T, *Ts]:
    def __init__(self, tag: T, values: tuple[*Ts]):
        self._tag = tag
        self._values = values

def process(arg: TaggedRecord[str, str, *tuple[float, ...]]): ...

process(TaggedRecord('foo', ('x', 4.2, 5.2))) # mypy passes

process(TaggedRecord(3, ('x', 4.2, 5.2))) # mypy fails: error:
    # Argument 1 to "TaggedRecord" has incompatible type "int";
    # expected "str"
process(TaggedRecord('foo', (4.2, 5.2, 'x'))) # mypy fails: error:
    # Argument 2 to "TaggedRecord" has incompatible type
    # "tuple[float, float, str]";
    # expected "tuple[str, *tuple[float, ...]]"
```
</Transform>



---
layout: center

---

# Generic DataFrames



---

# Insufficient Type Specification

<Transform :scale="1.25">
<v-clicks depth="1">

Common typing with Pandas DataFrames is insufficient

```python
import pandas as pd

def process(v: pd.DataFrame, q: pd.Series) -> pd.Series: ...
```

Most other DataFrame libraries do no better

</v-clicks>
</Transform>


---

# A DataFrame is a Variadic Type

<Transform :scale="1.25">
<v-clicks depth="2">

* A DataFrame is generic to many variables
    * The type of the index labels
    * The type of the columns labels
    * The variadic types of columnar data
* StaticFrame has implemented a true generic definition
* `TypeVarTuple` makes it possible

</v-clicks>
</Transform>

---

# A Generic DataFrame

<Transform :scale="1.5">

```python
class Frame[TIndex, TColumns, *TDtypes]: ...
```
</Transform>


---

# Complete DataFrame Typing

<Transform :scale="1.25">

```python
import static_frame as sf
import numpy as np

def process(
    v: sf.Frame[
        sf.IndexDate,            # type of Frame index labels
        sf.Index[np.str_],       # type of Frame column labels
        np.int64,                # type of Frame first column
        *tuple[np.float64, ...], # type of remaining columns
        ],
    ): ...
```
</Transform>



---

# Type Checking DataFrames

<Transform :scale="1.25">

```python
f1: sf.Frame[
    sf.IndexDate,
    sf.Index[np.str_],
    np.int64, np.float64,
    ] = sf.Frame.from_fields(
        ([20, 30], [1.2, 5.4]),
        index=sf.IndexDate(('2025-01-03', '2025-02-04')),
        columns=sf.Index(('a', 'b')),
        )

process(f1) # mypy passes
```
</Transform>



---

# Type Checking DataFrames

<Transform :scale="1.25">

```python
f2: sf.Frame[
    sf.IndexDate,
    sf.Index[np.str_],
    np.int64, np.float64, np.float64,
    ] = sf.Frame.from_fields(
        ([20, 30], [1.2, 5.4], [8.1, 3.2]),
        index=sf.IndexDate(('2025-01-03', '2025-02-04')),
        columns=sf.Index(('a', 'b', 'c')),
        )

process(f2) # mypy passes
```
</Transform>




---

# Type Checking DataFrames

<Transform :scale="1.25">

```python
f3: sf.Frame[
    sf.IndexDate,
    sf.Index[np.str_],
    np.int64, np.float64, np.str_,
    ] = sf.Frame.from_fields(
        ([20, 30], [1.2, 5.4], ['x', 'y']),
        index=sf.IndexDate(('2025-01-03', '2025-02-04')),
        columns=sf.Index(('a', 'b')),
        )

process(f3) # mypy fails: error:
    # Argument 1 to "process" has incompatible type
    # "Frame[IndexDate, Index[str_], signedinteger[_64Bit], float64, str_]";
    # expected "Frame[IndexDate, Index[str_], signedinteger[_64Bit], *tuple[float64, ...]]"

```
</Transform>



---

# Elastic Generics

<Transform :scale="1.25">
<v-clicks>

`TypeVarTuple` permits variadic generics

Elastic types are common

DataFrames are an excellent application

</v-clicks>
</Transform>





---
layout: center

---

# Thank you

