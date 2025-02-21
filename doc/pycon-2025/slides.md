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

# Generics in Python

<Transform :scale="1.5">
<v-clicks depth="1">

Permit specification of generic component types with `TypeVar`

```python {1-2|1-3|4|5|6}
>>> TK = TypeVar('TK')
>>> TV = TypeVar('TV')
>>> class Map(Generic[TK, TV]): ...
>>> m1 = Map[int, str]()
>>> m2 = Map[str, int]()
```

</v-clicks>
</Transform>
