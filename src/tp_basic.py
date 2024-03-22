import typing as tp
import static_frame as sf

@sf.CallGuard.check
def process(v: int, q: bool) -> list[float]:
    return [x * (0.5 if q else 0.25) for x in range(v)]

x = process(v=5, q=20)

# tp_basic.py:6: error: Argument "q" to "process" has incompatible type "int"; expected "bool"  [arg-type]

y: tp.Sequence[int] = process(v=5, q=False)

# tp_basic.py:11: error: Incompatible types in assignment (expression has type "list[float]", variable has type "Sequence[int]")  [assignment]


z = process(v=6, q='foo')
print(z)