---
theme: default
class: text-center
highlighter: shiki
lineNumbers: false
transition: slide-left
aspectRatio: 16/9
favicon: /favicon.ico
title: "Liberate your Generics with TypeVarTuple"

---

# Liberate your Generics with `TypeVarTuple`

<!-- Liberate your Python Generics with TypeVarTuple -->

#### Christopher Ariza
#### CTO, Research Affiliates

<style>
h1 {font-size: 1.5em;}
</style>



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
>>> m3 = Map[tuple[str, int], int]()
```

</v-clicks>
</Transform>


---

# Generics in Python 3.12

<Transform :scale="1.5">
<v-clicks depth="3">

Generics without explicit `TypeVar`

```python {1|2}
>>> class Map[TK, TV]: ...
>>> m3 = Map[tuple[str, int], int]()
```

</v-clicks>
</Transform>


---

# Limits of Python Generics

<Transform :scale="1.5">
<v-clicks depth="3">

Python generic specification is limited

`TypeVar`s have to be positional (no kwargs)

`TypeVar` count is fixed

```python {1|2|3}
>>> class Foo[T1, T2]: ...
>>> class Bar[T1, T2, T3]: ...
>>> class Baz[T1, T2, T3, T4]: ...
```

</v-clicks>
</Transform>



---
layout: center
---
# What if a Type Needs a Variable Number of Generics?



---

# Variadic Generics

<Transform :scale="1.5">
<v-clicks depth="3">

Some types might benefit from a variable numbers of generics

N-dimensional arrays

```python {1|2|3}
>>> class Array1D[TDtype, TLen1]: ...
>>> class Array2D[TDtype, TLen1, TLen2]: ...
>>> class Array3D[TDtype, TLen1, TLen2, TLen3]: ...
```

</v-clicks>
</Transform>


---

# `TypeVarTuple`

<Transform :scale="1.5">
<v-clicks depth="3">

New in Python 3.11 (PEP 646)

Define a type positional region of zero or more generic specifications

Can follow or proceed positional `TypeVar`s

Can conveniently express zero or more generics of the same type

</v-clicks>
</Transform>


---

# A Type with a Variable Number of Generics

<Transform :scale="1.5">
<v-clicks depth="3">

N-dimensional arrays with zero or more dimensional size specifications

```python {1|2|3|4}
>>> class Array[TDtype, *TShape]: ...
>>> a1: Array[float, Literal[10]]
>>> a2: Array[float, Literal[10], Literal[20]]
>>> a2: Array[float, Any, Literal[20]]
```

</v-clicks>
</Transform>


---

# A Type with a Variable Number of Generics

<Transform :scale="1.5">
<v-clicks depth="3">

Can use `Unpack` syntax to specify zero or more of the same type

Can combine with explicit types

```python {1|2|3}
>>> class Array[TDtype, *TShape]: ...
>>> a1: Array[float, *Literal[10]]
>>> a2: Array[float, Literal[5], *tuple[Literal[10], ...]]
```

</v-clicks>
</Transform>



---
layout: center
---
# `TypeVarTuple` in the wild


---

# NumPy

<Transform :scale="1.5">
<v-clicks depth="3">

Defined generic specification of `ndarray` before `TypeVarTuple`

First argument for shape not yet standardized

```python {1|2|3}
>>> class ndarray[TShape, TDtype]: ...
>>> a1: np.ndarray[Any, np.dtype[np.float64]]
>>> a2: np.ndarray[Literal[10], np.dtype[np.float64]]
```

</v-clicks>
</Transform>


---

# Component Types of DataFrames

<Transform :scale="1.5">
<v-clicks depth="3">

Row label type

Column label type

A variable number of columnar types

</v-clicks>
</Transform>


---

# StaticFrame

<Transform :scale="1.5">
<v-clicks depth="3">

A DataFrame library built on an immutable data model

With version 2.0, introduces a variadic generic DataFrame

</v-clicks>
</Transform>


---

# Components of a Generic DataFrame

<Transform :scale="1.5">
<v-clicks depth="1">

```python {1|1-3|1-4|1-5|1-6|1-8}
>>> class Frame[TIndex, TColumns, *TDtypes]: ...

>>> f: sf.Frame[
        sf.Index[np.int64], # index label type
        sf.Index[np.str_],  # column label type
        np.int8,            # column 1 type
        np.bool_,           # column 2 type
        ]
```

</v-clicks>
</Transform>


---

# Components of a Generic DataFrame

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

# Generics with Expressive `Unpack` Syntax

<Transform :scale="1.5">
<v-clicks depth="1">

```python {1|1-2|1-3|1-4|1-6}
>>> f = sf.Frame[
        sf.Index[np.int64],
        sf.Index[np.str_],
        np.bool_,
        *tuple[np.float64, ...],
        ]()
```


</v-clicks>
</Transform>

---

# Generics with Expressive `Unpack` Syntax

<Transform :scale="1.5">
<v-clicks depth="1">

```python {1|1-2|1-3|1-4|1-5|1-6|1-8}
>>> f = sf.Frame[
        sf.IndexDate,
        sf.Index[np.str_],
        np.bool_,
        *tuple[np.int64, ...],
        np.str_,
        np.str_,
        ]()
```

</v-clicks>
</Transform>



---

# StaticFrame + `mypy`, `pyright`, `sf.CallGuard`

<Transform :scale="1.5">
<v-clicks depth="1">

Static type checking with `mypy`, `pyright`

Run-time validation with `sf.CallGuard`

</v-clicks>
</Transform>





---

# Liberate your Generics

<Transform :scale="1.5">
<v-clicks depth="1">

Your types might benefit from `TypeVarTuple`

Variadic generic DataFrames are available in StaticFrame

</v-clicks>
</Transform>



---
layout: center
---
# Thank you

