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

# Elastic Generics: Flexible Static Typing with TypeVarTuple and Unpack

<br />
<br />

#### Christopher Ariza
#### CTO, Research Affiliates

<style>
h1 {font-size: 3em !important; line-height: 1.1 !important;}
</style>

<!-- /NOTE: this is tested on slidev 0.50.0, 0.51 did not work! -->


---

# Typing in Python


<Transform :scale="1.25">
<v-clicks>

Since Python 3.5 (PEP 484)

An optional layer, independent of run-time

Statically verifiable with tools like `mypy` and `pyright`

Numerous tools for run-time usage

</v-clicks>
</Transform>

---

# Simple & Complex Types
<Transform :scale="1.25">
<v-clicks depth="1">

Elemental types are simple

```python
def process(
        x: int,
        y: float,
        z: bool,
        ) -> float: ...
```

Types that contain other types are complex

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

# Extending `tuple` Flexability

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
* `Unpack` is a component or a new syntax
    * `Unpack[tuple[int, ...]]` equivalent to `*tuple[int, ...]`
    * Backwards compatibility through `typing-extensions`

</v-clicks>
</Transform>


---

# Elastic Generics with TypeVarTuple and Unpack

<Transform :scale="1.25">
<v-clicks depth="1">

Typing opportunities with `tuple` and `Unpack` syntax

Using `TypeVarTuyple` to define generic classes

A compelling application: generic DataFrames

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

* `tuple` typing upgraded in 3.11
    * Previously: `tuple[int, ...]` and `tuple[int, str, float]`
    * Support Unpack syntax: `tuple[int, str, *tuple[float, ...]]`
* `tuple` is nearly `class Tuple[*Ts]: ...`
    * Must use `Tuple[*tuple[int, ...]]` instead of `Tuple[int, ...]`

</v-clicks>
</Transform>


---

# Annotating `tuple`: Sized & Ordered

<Transform :scale="1.25">
<v-clicks depth="1">

Define size and an ordering of types

```python

```

</v-clicks>
</Transform>


---

# Annotating `tuple`: Unsized

<Transform :scale="1.25">
<v-clicks depth="1">

Define zero or more of one type

```python

```

</v-clicks>
</Transform>



---

# Annotating `tuple`: Sized & Ordered & Unsized

<Transform :scale="1.25">
<v-clicks depth="1">

Can define only one unsized region

Sized and ordered segments can optionally start or end

```python

```

</v-clicks>
</Transform>








---
layout: center

---
# Define generic classes `TypeVarTuple`



<!-- Need to show usage with other type vars, call it `LabelledRecord` -->


---

# `TypeVarTuple` and `Unpack` (< 3.12)

<Transform :scale="1.25">
<v-clicks depth="1">

```python
Ts = TypeVarTuple('Ts')
class Record(Generic[Ts]): ...

r1: Record[int, str]
r2: Record[int, str, float]
r3: Record[int, str, Unpack[tuple[float, ...]]] # unpack is a component
```

</v-clicks>
</Transform>


---

# `TypeVarTuple` and `Unpack` (>= 3.12)

<Transform :scale="1.25">
<v-clicks depth="1">

```python
class Record[*Ts]: ...

r1: Record[int, str]
r2: Record[int, str, float]
r3: Record[int, str, *tuple[float, ...]] # unpack is star expansion
```

</v-clicks>
</Transform>









---
layout: center

---
# Generic DataFrames



---

# A Complex Type with Many Component Types

<Transform :scale="1.25">

* A DataFrame has many components types
    * The type of the index
    * The type of the columns
    * The types of data in columns


</Transform>





---

# Insufficient Type Depth

<Transform :scale="1.25">

```python
import pandas as pd

def process(v: pd.DataFrame, q: pd.Series) -> pd.Series: ...
```

</Transform>




---

# Fully Typed DataFrames

<Transform :scale="1.5">
<v-clicks depth="1">

```python  {1|1-3|1-4|1-5|1-6|1-7|1-8|1-9}
>>> class Frame[TIndex, TColumns, *TDtypes]: ...

>>> f: sf.Frame[
        sf.IndexDate,      # index label type
        sf.Index[np.str_], # column label type
        np.float64,        # column 1 type
        np.float64,        # column 2 type
        np.bool_,          # column 3 type
        np.str_]           # column 4 type
```

</v-clicks>
</Transform>




---

# Variadic Typed DataFrames

<Transform :scale="1.5">
<v-clicks depth="1">

```python {1|1-2|1-3|1-4|1-6}
>>> f = sf.Frame[
        sf.Index[np.int64],
        sf.Index[np.str_],
        np.bool_,
        *tuple[np.float64, ...], # zero or more float64 columns
        ]()
```


</v-clicks>
</Transform>



---

# Complete Type Information

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

# Thank You

<Transform :scale="1.25">

StaticFrame: https://static-frame.dev
fetter: https://fetter.io
</Transform>


