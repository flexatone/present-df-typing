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

An optional layer of the program

<!-- Independent from run-time -->

Verrifiable with tools like `mypy` and `pyright`
</v-clicks>
</Transform>





---

# Typing in Python

<Transform :scale="1.25">

Since Python 3.5

An optional layer of the program

<!-- Independent from run-time -->

Verrifiable with tools like `mypy` and `pyright`

</Transform>



---

# Simple & Complex Types
<Transform :scale="1.5">
<v-clicks depth="1">

Elemental types are simple

```python
def process(x: int, y: float, z: bool) -> float: ...
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
    def keys() -> Iterator[TK]: ...
    def values() -> Iterator[TV]: ...
    def items() -> Iterator[tuple[TK, TV]]: ...

m1 = Map[str, bool]()
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
```

</v-clicks>
</Transform>



---

# Sometimes Types Imply Shape or Ordering

<Transform :scale="1.5">
<v-clicks depth="1">

We might ask more from our types

`list[str]`: unbound in size

`Interator[str | bool]`: unordered component types


</v-clicks>
</Transform>


---

# The Power of `tuple`

<Transform :scale="1.5">
<v-clicks depth="1">

As an immutable sequence, use `tuple` differently

`tuple[str, float, float, bool]`: ordered types of size four

`tuple[str, ...]`: 0 or more `str`


</v-clicks>
</Transform>



---

# The Power of `tuple`

<Transform :scale="1.5">
<v-clicks depth="1">

* `tuple` since Python 3.5
    1. Orderings of a component types
    2. Unbound sequences of a single type
* What if you need both?
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
* `Unpack` is a generic alias or a new syntax
* `class Record[*Ts]: ...`
    * `Record[int, str]`
    * `Record[int, str, float]`
    * `Record[int, str, *tuple[float, ...]]`

</v-clicks>
</Transform>



---

# Understanding Elastic Generics

<Transform :scale="1.5">
<v-clicks depth="1">

Typing opportunities with `tuple`

Using `Unpack` syntax

Using `TypeVarTuyple` to define generic classes

A compelling application: generic DataFrames

</v-clicks>
</Transform>


---
layout: center
---
# What's in it for me?


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
# What's in it for you?



---

# Type Annotations for the Modern `tuple`

<Transform :scale="1.5">
<v-clicks depth="1">

* `tuple` since 3.11:
    * `class tuple[*Ts]: ...`
* Supports all forms
    * `tuple[int, ...]`
    * `tuple[int, str, float]`
    * `tuple[int, str, *tuple[float, ...]]`

</v-clicks>
</Transform>
