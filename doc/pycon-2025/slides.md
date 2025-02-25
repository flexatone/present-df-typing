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

<!-- Liberate your Python Generics with TypeVarTuple -->

#### Christopher Ariza
#### CTO, Research Affiliates

<style>
h1 {font-size: 1.5em;}
</style>





---

# Typing in Python

<Transform :scale="1.25">
<v-clicks>

Since Python 3.5

An optional layer independent of run-time

Verrifiable with tools like `mypy` and `pyright`

</v-clicks>
</Transform>


---

# Simple & Complex Types
<Transform :scale="1.5">
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
<Transform :scale="1.5">
<v-clicks depth="1">

* Complex types are "generic"
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

<Transform :scale="1.5">
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

<Transform :scale="1.5">
<v-clicks depth="1">


```python
class Map[TK, TV]:
    def keys() -> Iterator[TK]: ...
    def values() -> Iterator[TV]: ...
    def items() -> Iterator[tuple[TK, TV]]: ...
    def __getitem__(self, key: TK) -> TV: ...
```

</v-clicks>
</Transform>



---

# Can Types Define Shape or Ordering

<Transform :scale="1.5">
<v-clicks depth="2">

* We might ask more from our types
* `list[str]`
    * Unbound in size
    * Might specify size
* `Interator[str | bool]`
    * Unordered component types
    * Might specify explicit ordering


</v-clicks>
</Transform>


---

# The Power of `tuple`

<Transform :scale="1.5">
<v-clicks depth="1">

* As an immutable sequence, `tuple` is different
* Can define order and count of types
    * `tuple[str, float, float, bool]`
* Can define zero or more of a single type
    * `tuple[str, ...]`

<!-- * `tuple` since Python 3.5
    1. Orderings of a component types
    2. Unbound sequences of a single type -->

</v-clicks>
</Transform>



---

# The Power of `tuple`

<Transform :scale="1.5">
<v-clicks depth="1">

* What if you need both ordering and an unbound sequence
* A `tuple` that starts with an `int` and a `str` and follows with zero or more `float`
* A dataset of identifiers followed by variable observations
* A `Record` type that can be flexible & elastic

</v-clicks>
</Transform>




---

# `TypeVarTuple` and `Unpack`

<Transform :scale="1.5">
<v-clicks depth="1">

* `TypeVarTuple` & `Unpack` since Python 3.11
* Define generics tuple-like flexibility
* `Unpack` is a generic alias or a new syntax
* Backwards compatibility through `typing-extensions`

</v-clicks>
</Transform>


---

# `TypeVarTuple` and `Unpack` (< 3.12)

<Transform :scale="1.5">
<v-clicks depth="1">

```python
Ts = TypeVarTuple('Ts')
class Record(Generic[Ts]): ...

r1: Record[int, str]
r2: Record[int, str, float]
r3: Record[int, str, Unpack[tuple[float, ...]]]
```

</v-clicks>
</Transform>


---

# `TypeVarTuple` and `Unpack` (>= 3.12)

<Transform :scale="1.5">
<v-clicks depth="1">

```python
class Record[*Ts]: ...

r1: Record[int, str]
r2: Record[int, str, float]
r3: Record[int, str, *tuple[float, ...]]
```

</v-clicks>
</Transform>



---

# Understanding Elastic Generics

<Transform :scale="1.5">
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
# Why you?


---
layout: center

---
# Typing opportunities with `tuple`



---

# Annotating `tuple`

<Transform :scale="1.5">
<v-clicks depth="1">

* `tuple` typing upgraded in 3.11
* Essentially equivalent to `class tuple[*Ts]: ...`
* Supports all forms
    * `tuple[int, ...]`
    * `tuple[int, str, float]`
    * `tuple[int, str, *tuple[float, ...]]`

</v-clicks>
</Transform>


---

# Annotating `tuple`: Sized & Ordered

<Transform :scale="1.5">
<v-clicks depth="1">

Define size and an ordering of types

```python

```

</v-clicks>
</Transform>


---

# Annotating `tuple`: Unsized

<Transform :scale="1.5">
<v-clicks depth="1">

Define zero or more of one type

```python

```

</v-clicks>
</Transform>



---

# Annotating `tuple`: Sized & Ordered & Unsized

<Transform :scale="1.5">
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




---

# A `Record` class

<Transform :scale="1.5">
<v-clicks depth="1">

```python
class Record[*Ts]: ...

r1: Record[int, ...]
r2: Record[int, str, float]
r3: Record[int, str, *tuple[float, ...]]
r4: Record[int, str, *tuple[float, ...], bool]
```

</v-clicks>
</Transform>





---
layout: center

---
# Generic DataFrames

