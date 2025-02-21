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
