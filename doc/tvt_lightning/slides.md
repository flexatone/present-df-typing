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
>>> m = Map[str, int]()
```

</v-clicks>
</Transform>


---

# Limits of Python Generics

<Transform :scale="1.5">
<v-clicks depth="3">

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

# Variable Number of Generics?

<Transform :scale="1.5">
<v-clicks depth="3">

N-dimensional arrays

Do not want to have a different class for 1D, 2D, 3D, etc.

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

Define region of zero or more generic specifications

Can follow or proceed `TypeVar`s

Can conveniently express zero or more generics of the same type

</v-clicks>
</Transform>


---

# `TypeVarTuple` < 3.12

<Transform :scale="1.5">
<v-clicks depth="3">

An `Array` with a dtype type and zero or more axis length types

``` python {1|2|3}
>>> TDtype = TypeVar('TDtype')
>>> TAxis = TypeVarTuple('TAxis')
>>> class Array(Generic[TDtype, Unpack[TAxis]]):
```

</v-clicks>
</Transform>



---

# `TypeVarTuple` >= 3.12

<Transform :scale="1.5">
<v-clicks depth="3">

An `Array` with a dtype type and zero or more axis length types

```python {1|2|3|4}
>>> class Array[TDtype, *TShape]: ...
>>> a1: Array[float, Literal[10]] # 1D shape (10,)
>>> a2: Array[float, Literal[10], Literal[20]] # 2D shape (10, 20)
>>> a3: Array[float, Any, Literal[20]] # 2D shape (*, 20)
```

</v-clicks>
</Transform>



---

# Expressive Opportunities of `TypeVarTuple`

<Transform :scale="1.5">
<v-clicks depth="3">

Can use `Unpack` (< 3.11) or `*` (>= 3.11) syntax to specify zero or more of the same type

Can combine with fixed types for the same `TypeVarTuple` region

```python {1|2|3}
>>> class Array[TDtype, *TShape]: ...
>>> a1: Array[float, *tuple[Literal[10], ...]] # ND of length 10
>>> a2: Array[float, Literal[5], *tuple[Any, ...]] # ND with first of length 5
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

First argument for shape is just a `TypeVar`

Usage not yet standardized

```python {1|2|3}
>>> class ndarray[TShape, TDtype]: ...
>>> a1: np.ndarray[Any, np.dtype[np.float64]]
>>> a2: np.ndarray[Literal[10], np.dtype[np.float64]]
```

</v-clicks>
</Transform>


---

# DataFrames

<Transform :scale="1.5">
<v-clicks depth="3">

Numerous component types

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

Version 2 introduces a variadic generic DataFrame

</v-clicks>
</Transform>


---

# Fully Typed DataFrames

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

# Variadic Typed DataFrames

<Transform :scale="1.5">
<v-clicks depth="1">

```python {1|1-2|1-3|1-4|1-5|1-6|1-8}
>>> f = sf.Frame[
        sf.IndexDate,
        sf.Index[np.str_],
        np.bool_,
        *tuple[np.int64, ...], # zero or more float64 columns
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

Variadic generic DataFrames in StaticFrame

</v-clicks>
</Transform>



---
layout: center
---
# Thank you

