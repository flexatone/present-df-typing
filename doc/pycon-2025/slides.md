---
theme: default
class: text-center
highlighter: shiki
lineNumbers: false
transition: slide-left
aspectRatio: 16/9
favicon: /favicon.ico
title: "Elastic Generics: Flexible Static Typing with TypeVarTuple and Unpack"
background: /IMG_4390.jpg

---

<div class="bg-black bg-opacity-80 p-4 rounded-xl text-white">

# Elastic Generics: Flexible Static Typing with `TypeVarTuple` & `Unpack`


<br />
<br />

#### Christopher Ariza
#### CTO, Research Affiliates

</div>

<style>
h1 {font-size: 3.5em !important; line-height: 1.3 !important;}
</style>

<!-- NOTE: this is tested on slidev 0.50, 0.51 did not work!

Point out how strange TaggedRecord is
Pydantic / Panderra: show how these are insufficient

-->



---

# Static Typing of Complex Containers

<!--
If you work with DataFrames, you might have noticed that, when passing around DataFrames, your types are woefully insufficient
-->

<Transform :scale="1.25">

```python {all}
import pandas as pd

def process(
    x: pd.DataFrame,
    y: pd.DataFrame,
    ) -> pd.DataFrame: ...
```
</Transform>





---

# Elastic Generics

<!--
Python now has the tools to type DataFrames not just column by column, but with expressive definitions that permit variable or elastic regions of columnar types
-->

<Transform :scale="1.25">

```python {all}
import static_frame as sf
import numpy as np

def process(
    arg: sf.Frame[
        sf.IndexDate,                      # type of Frame index labels
        sf.Index[np.str_],                 # type of Frame column labels
        np.int64, *tuple[np.float64, ...], # fixed and elastic columnar types
        ],
    ): ...
```
</Transform>




---

# A Decade of Python Type Annotations


<Transform :scale="1.25">
<v-clicks>

Introduced in Python 3.5 (2015)

An optional layer, independent of run-time

Improves code quality and maintainability

Statically verifiable with tools like `mypy` and `pyright`

Numerous tools for run-time validation

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
        ): ...
```

Types composed of other types are generic

```python
def process(
        x: Sequence[int],
        y: frozenset[str],
        z: dict[str, bool],
        ): ...
```

</v-clicks>
</Transform>


---

# Generic Types
<Transform :scale="1.25">
<v-clicks depth="1">

* Generic types are made concrete with type parameters
* Type parameters are positional parameters
* Python containers are generic
    * `list[str]`
    * `set[int]`
* Python abstract base classes are generic
    * `Iterator[float]`
    * `Mapping[str, bool]`

</v-clicks>
</Transform>


---
layout: quote
---

## All built-in generic containers (except one!) define unsized, homogeneously typed values

<!-- While a list can hold any type, have to define it as having a single type (which might be a union type)
(all but one)
-->


---
layout: center
---

# Defining Generic Types


---

# Defining Generic Types in Python (< 3.12)

<Transform :scale="1.25">
<v-clicks depth="1">

Subclass `Generic`

Provide `TypeVar` instances to `Generic` to specify type variables

```python {1-2|1-4|1-5|1-6|1-7|all}
TK = TypeVar('TK')
TV = TypeVar('TV')

class Map(Generic[TK, TV]):
    def keys(self) -> Iterator[TK]: ...
    def values(self) -> Iterator[TV]: ...
    def items(self) -> Iterator[tuple[TK, TV]]: ...
    def __getitem__(self, key: TK) -> TV: ...

```

</v-clicks>
</Transform>




---

# Defining Generic Types in Python (>= 3.12)

<Transform :scale="1.25">
<v-clicks depth="1">

```python {1|all}
class Map[TK, TV]:
    def keys() -> Iterator[TK]: ...
    def values() -> Iterator[TV]: ...
    def items() -> Iterator[tuple[TK, TV]]: ...
    def __getitem__(self, key: TK) -> TV: ...
```

No longer need to subclass `Generic`

`TypeVar` implicitly defined

</v-clicks>
</Transform>




---
layout: quote
---
## Can a generic define size or ordering of types?

<!--
Examples we have seen are of a homogenously typed collections
 -->

---

# Asking More from our Types

<Transform :scale="1.25">
<v-clicks depth="2">

Could a `list[str]` specify a size?

Could an `Sequence[str | bool]` specify an ordering of `str` and `bool`?

</v-clicks>
</Transform>


---

# The Dual Capability of `tuple`

<Transform :scale="1.25">
<v-clicks depth="1">

* `tuple` can do more
* A sequence with defined size and ordering of types
    * `tuple[str, float, float, bool]`
* An unsized sequence of homogenous types
    * `tuple[str, ...]`

</v-clicks>
</Transform>


---

# Extending `tuple` Flexibility

<Transform :scale="1.25">
<v-clicks depth="1">

Combining both ordered and unsized sequences of types

Fixed `int`, `str` followed by zero or more `float`

A dataset of identifiers followed by observations

`tuple[int, str, ZeroOrMore[float]]`

<!-- Not hypothetical: this is a practical form of dataset -->

</v-clicks>
</Transform>


---

# `TypeVarTuple` and `Unpack`

<Transform :scale="1.25">
<v-clicks depth="2">

Defining and concretizing generics with both ordered and unsized sequences

Introduced in Python 3.11 (PEP 646)

Backwards compatibility through `typing-extensions`

</v-clicks>
</Transform>

---

# Generics Defined with `TypeVarTuple`

<Transform :scale="1.25">
<v-clicks depth="2">

A placeholder in the type parameter list

Variadic: permits zero or more type variables

Supports `tuple`-like flexibility

Can be combined with one or more `TypeVar`

</v-clicks>
</Transform>


---

# `Unpack`

<Transform :scale="1.25">
<v-clicks depth="2">

* A component or syntax for concretizing `TypeVarTuple`
* Leverages the unsized sequence notation of `tuple`
* Python < 3.11: `Unpack[tuple[int, ...]]`
* Python >= 3.11: `*tuple[int, ...]`
* The `*` matters:
    * `('a', 5, 3, 8, 11): tuple[str, *tuple[int, ...]]`
    * `('a', (5, 3)): tuple[str, tuple[int, ...]]`
* Think `*tuple[int, ...]` as `ZeroOrMore[int]]`
</v-clicks>
</Transform>


---

# Elastic Generics with `TypeVarTuple` and `Unpack`

<!-- now that we have some idea of what these things are for we can explore them in depth -->

<Transform :scale="1.25">
<v-clicks depth="1">

1. Typing opportunities with `tuple` and `Unpack` syntax
2. Using `TypeVarTuple` to define generic classes
3. A compelling application: generic DataFrames

</v-clicks>
</Transform>


---
layout: center
---
## Why me?

<!--
I did not work on the PEP or implementation
Much credit to those who did
I was just the person who had been looking for this feature for years
-->


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

Long pondered static typing of arrays and DataFrames
</v-clicks>
</Transform>




---
layout: cover
background: /IMG_4390.jpg

---
<div class="bg-black bg-opacity-80 p-4 rounded-xl text-white">

# 1. Typing opportunities with `tuple`

</div>
<!--
By understanding what we can do with tuple we learn what we can do with TypeVarTuple
 -->

---

# Concretizing `tuple`

<Transform :scale="1.25">
<v-clicks depth="1">

* Since 3.5:
    * `tuple[int, ...]`
    * `tuple[int, str, float]`
* Since 3.11:
    * Can use `Unpack` syntax
    * `tuple[int, str, *tuple[float, ...]]`
* A range of options
    * Sized & ordered
    * Unsized
    * Sized & ordered & unsized

</v-clicks>
</Transform>


---

# Concretizing `tuple`: Sized & Ordered

<Transform :scale="1.25">
<v-clicks depth="1">

Define size and an ordering of types

```python {1|1-3|all}
def process(arg: tuple[int, str, float]): ...

process((3, 'x', 4.2)) # mypy passes

process((3, 'x', 4.2, 5.2)) # mypy fails: error:
    # Argument 1 to "process" has incompatible type
    # "tuple[int, str, float, float]"; expected "tuple[int, str, float]"
```
</v-clicks>
</Transform>


---

# Concretizing `tuple`: Unsized

<Transform :scale="1.25">
<v-clicks depth="1">

Define zero or more of one type

```python {1|1-3|1-4|all}
def process(arg: tuple[float, ...]): ...

process((4.2, 5.8)) # mypy passes
process(()) # mypy passes

process((4.2, 5.8, 7.2, 'y')) # mypy fails: error:
    # Argument 1 to "process" has incompatible type
    # "tuple[float, float, float, str]"; expected "tuple[float, ...]"
```
</v-clicks>
</Transform>



---

# Concretizing `tuple`: Sized & Ordered & Unsized

<Transform :scale="1.25">
<v-clicks depth="1">

Can define only one unsized `Unpack` region

Ordered segments be before or after an `Unpack` region

```python {1|1-3|1-4|1-5|all}
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



<!-- ---

# Concretizing `tuple`: Sized & Ordered & Unsized & Sized & Ordered

<Transform :scale="1.25">
<v-clicks depth="1">

Ordered segments can proceed and/or follow an `Unpack` region

```python {1|1-3|1-4|all}
def process(arg: tuple[int, *tuple[float, ...], str, bool]): ...

process((3, 4.2, 5.8, 'x', False)) # mypy passes
process((3, 'y', True)) # mypy passes

process((3, 'x', 4.2, 5.8, 'y', 7.2, 'x', False)) # mypy fails: error:
    # Argument 1 to "process" has incompatible type
    # "tuple[int, str, float, float, str, float, str, bool]";
    # expected "tuple[int, *tuple[float, ...], str, bool]"
```

</v-clicks>
</Transform> -->






---
layout: cover
background: /IMG_4390.jpg

---
<div class="bg-black bg-opacity-80 p-4 rounded-xl text-white">

# 2. Defining Generic Classes with `TypeVarTuple`

</div>

<!--
Now that we have seen the flexibility of the generic tuple, we can see how TypeVarTuple lets use have that same flexibility with our own classes
 -->




---

# Defining Generic Classes with `TypeVarTuple`

<Transform :scale="1.25">
<v-clicks depth="1">

Only one type variable can be a `TypeVarTuple`

A placeholder for ordered types and/or an `Unpack` expression

Normal `TypeVar` can proceed and/or follow a `TypeVarTuple`

</v-clicks>
</Transform>


---

# Generic Classes with `TypeVarTuple` and `Unpack` (< 3.12)

<Transform :scale="1.25">

```python {0|1|1-2|1-4|1-5}
Ts = TypeVarTuple('Ts')
class Record(Generic[Ts]): ...

r1: Record[int, str]
r2: Record[int, str, Unpack[tuple[float, ...]]] # unpack is a component
```
</Transform>


---

# Generic Classes with `TypeVarTuple` and `Unpack` (>= 3.12)

<Transform :scale="1.25">

```python {1|1-3|1-4}
class Record[*Ts]: ...

r1: Record[int, str]
r2: Record[int, str, *tuple[float, ...]] # unpack is star expansion
```
</Transform>


---

# Concretizing `Record`

<Transform :scale="1.25">

```python {1|1-3|5|5-7|5-10}
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

# Concretizing `Record`

<Transform :scale="1.25">

<!-- We can make the same class concrete in many different ways -->

```python {1-3|5|5-7|5-8|5-12}
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

# Concretizing `Record`

<Transform :scale="1.25">

```python {1-3|5|5-7|5-8|5-13}
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

# Combining `TypeVar` and `TypeVarTuple`

<Transform :scale="1.25">

```python {1|1-4|6|6-8|6-12|6-16}
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
layout: cover
background: /IMG_4390.jpg

---
<div class="bg-black bg-opacity-80 p-4 rounded-xl text-white">

# 3. Generic DataFrames

</div>





---

# Insufficient Type Specification

<Transform :scale="1.25">
<v-clicks depth="1">

Common typing with Pandas DataFrames is insufficient

```python
import pandas as pd

def process(v: pd.DataFrame, q: pd.Series) -> pd.Series: ...
```

</v-clicks>
</Transform>


---

# A DataFrame is Generic

<Transform :scale="1.25">
<v-clicks depth="2">

* A DataFrame type is generic to many variables
    * The index label types
    * The columns label types
    * The variadic types of columnar data
* Idiomatic DataFrame usage is diverse
    * Fixed column size and type
    * Flexible size with optional columns

</v-clicks>
</Transform>


---

# A Comprehensively Generic DataFrame

<Transform :scale="1.25">
<v-clicks depth="2">

StaticFrame 2.0: a complete generic DataFrame

Leverages `TypeVarTuple`

Statically verifiable with `mypy` and `pyright`

Run-time validation with `@sf.CallGuard.check`

Integrated with generic `Series`, `Index`, and `IndexHierarchy`

</v-clicks>
</Transform>


---

# StaticFrame's Generic DataFrame

<Transform :scale="1.5">

```python
class Frame[TIndex, TColumns, *TDtypes]: ...
```
</Transform>


---

# Concretizing a DataFrame

<Transform :scale="1.25">

```python {1-4|1-5|1-6|1-7|1-12}
import static_frame as sf
import numpy as np

def process(
    arg: sf.Frame[
        sf.IndexDate,                      # type of Frame index labels
        sf.Index[np.str_],                 # type of Frame column labels
        np.int64, *tuple[np.float64, ...], # type of first and following columns
        ],
    ): ...
```
</Transform>


---

# 1. Type-Checking DataFrames

<Transform :scale="1.25">

```python {1-3|4|1-9|1-11}
f2: sf.Frame[
    sf.IndexDate,
    sf.Index[np.str_],
    np.int64, np.float64, np.float64, np.float64, # int followed by three float columns
    ] = sf.Frame.from_fields(
        ([20, 30], [1.2, 5.4], [8.1, 3.2], [3.1, 7.9]),
        index=sf.IndexDate(('2025-01-03', '2025-02-04')),
        columns=sf.Index(('a', 'b', 'c')),
        )

process(f2) # mypy passes
```
</Transform>


---

# 2. Type-Checking DataFrames

<Transform :scale="1.25">

```python {1-3|4|1-9|11-15}
f3: sf.Frame[
    sf.IndexDate,
    sf.Index[np.str_],
    np.int64, np.float64, np.str_, # int, float, and string columns
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

Static typing can be elastic

`TypeVarTuple` permits flexible, variadic generic types

Unlock idiomatic DataFrame typing

</v-clicks>
</Transform>



---
layout: cover
background: /IMG_4390.jpg

---
<div class="bg-black bg-opacity-80 p-4 rounded-xl text-white">

# Thank you

</div>

