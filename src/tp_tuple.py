import typing as tp


def proc1(arg: tuple[int, *tuple[bool, ...], str]):
    pass



x = proc1((3, 'x'))
# x = proc1('x') # fails
y = proc1((3, True, False, True, 'x'))

# y = proc1((3, True, 'x', True, 'x')) # fails


def proc2(arg: tuple[int, *tuple[tp.Union[bool, float], ...], str]):
    pass

x = proc2((3, 'x'))

x = proc2((3, False, 'x'))

x = proc2((3, True, 'x'))

x = proc2((3, True, 1.5, False, 1,5, 'x'))

# x = proc2((3, True, 1.5, 'x', False, 1,5, 'x')) # fails


# we probably can do this but there does not seem to be  a reason
def proc3(arg: tuple[int, *tuple[bool, *tuple[float, ...], bool], str]):
    pass



class Record[*T]:
    pass

def proc4(arg: Record[int, str, bool]):
    pass

r1: Record[int, str, bool] = Record()
r2: Record[int, str] = Record()
r3: Record[int, str, bool, bool, bool] = Record()
r4: Record[int, str, bool, bool, bool, str] = Record()

x = proc4(r1)
# x = proc4(r2) # fails

def proc5(arg: Record[int, str, *tuple[bool, ...]]):
    pass

x = proc5(r1)
x = proc5(r2) # passes as zero or more
x = proc5(r3)
# x = proc5(r4) # fails


def proc6(arg: Record[*tuple[bool, ...]]):
    pass

r5: Record[bool, bool, bool] = Record()
r6: Record[bool, bool, bool, bool] = Record()
r7: Record[bool, bool, bool, float] = Record()

x = proc6(r5)
x = proc6(r6)
# x = proc6(r7) # src/tp_tuple.py:68: error: Argument 1 to "proc6" has incompatible type "Record[bool, bool, bool, float]"; expected "Record[*tuple[bool, ...]]"  [arg-type]



# example of a generic function
def gfunc1[*T](arg1: Record[*T], arg2: Record[*T]):
    pass


x = gfunc1(r1, r1)
# x = gfunc1(r1, r2) # fails
x = gfunc1(r3, r3)
x = gfunc1(r4, r4) # does not fail

# x = gfunc1[int, str](r1, r1) # mypy:  error: Type application is only supported for generic classes  [misc]


















# interesting example: https://arjancodes.com/blog/python-generics-syntax/
type TaggedTuple[*Ts] = tuple[str, *Ts]


