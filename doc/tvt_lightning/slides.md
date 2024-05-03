---
theme: default
class: text-center
highlighter: shiki
lineNumbers: false
transition: slide-left
aspectRatio: 16/9
favicon: /favicon.ico
title: "Unlock Variadic Generics with TypeVarTuple"

---

# Unlock Variadic Generics with `TypeVarTuple`

<!-- Unlock Variadic Python Generics with TypeVarTuple -->

#### Christopher Ariza
#### CTO, Research Affiliates

<style>
h1 {font-size: 1.5em;}
</style>



---

# Limits of Python Generics

<Transform :scale="1.25">
<v-clicks depth="3">

- Python generic specification is limited
- Up until Python 3.11, generic classes could only be defined with positional TypeVars

```python
>>> T1 = TypeVar('T1')
>>> T2 = TypeVar('T2')
>>> class Foo(Generic[T1, T2]): ...
>>> d: Foo[int, str] = Foo()
```

</v-clicks>
</Transform>


---

# What if a Type Needs a Variable Number of Generics?

<Transform :scale="1.25">
<v-clicks depth="3">

- Some types might vary the number of generics needed
- Typing the shape of n-dimensional array
    - ``Array[tp.Literal[4]]``
    - ``Array[tp.Literal[4], tp.Literal[8]]``
    - ``Array[tp.Literal[4], tp.Literal[8], tp.Literal[6]]``
- Typing the columns of variable sized table
    - ``Table[int]``
    - ``Table[int, str]``
    - ``Table[int, str, float]``

</v-clicks>
</Transform>


---

# `TypeVarTuple`

<Transform :scale="1.25">
<v-clicks depth="3">

- New in Python 3.11 (PEP XXX)
- Define a type variable region of zero or more generic specifications
- Can follow and/or proceed positional type vars
- Can express zero or more generics of the same type

</v-clicks>
</Transform>



---

# Thank You

<Transform :scale="1.25">

StaticFrame: https://static-frame.dev
</Transform>


