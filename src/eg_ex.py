

# def process(arg: tuple[int, str, float]): ...

# process((3, 'x', 4.2)) # mypy passes
# process((3, 'x', 4.2, 5.2)) # mypy fails: error:
#     # Argument 1 to "process" has incompatible type
#     # "tuple[int, str, float, float]"; expected "tuple[int, str, float]"

#-----------------------------------------

# def process(arg: tuple[float, ...]): ...

# process((4.2, 5.8)) # mypy passes
# process(()) # mypy passes
# process((4.2, 5.8, 7.2)) # mypy passes

# process((4.2, 5.8, 7.2, 'y')) # mypy fails: error:
#     # Argument 1 to "process" has incompatible type
#     # "tuple[float, float, float, str]"; expected "tuple[float, ...]"


#-----------------------------------------

# def process(arg: tuple[int, str, *tuple[float, ...]]): ...

# process((3, 'x', 4.2)) # mypy passes
# process((3, 'x')) # mypy passes
# process((3, 'x', 4.2, 5.8, 7.2)) # mypy passes

# process((3, 'x', 4.2, 5.8, 7.2, None)) # mypy fails: error:
#     # Argument 1 to "process" has incompatible type
#     # "tuple[int, str, float, float, float, None]";
#     # expected "tuple[int, str, *tuple[float, ...]]"


#-----------------------------------------

# def process(arg: tuple[int, *tuple[float, ...], str, bool]): ...

# process((3, 4.2, 5.8, 'x', False)) # mypy passes
# process((3, 'y', True)) # mypy passes

# process((3, 'x', 4.2, 5.8, 'y', 7.2, 'x', False)) # mypy fails: error:
#     # Argument 1 to "process" has incompatible type
#     # "tuple[int, str, float, float, str, float, str, bool]";
#     # expected "tuple[int, *tuple[float, ...], str, bool]"


#-----------------------------------------

# class Record[*Ts]:
#     def __init__(self, arg: tuple[*Ts]):
#         self._store = arg

# def process(arg: Record[int, str, float]): ...

# process(Record((3, 'x', 4.2))) # mypy passes
# process(Record((3, 'x', 4.2, 5.2))) # mypy fails: error:
#     # Argument 1 to "Record" has incompatible type
#     # "tuple[int, str, float, float]"; expected "tuple[int, str, float]"



# #-----------------------------------------

# class Record[*Ts]:
#     def __init__(self, arg: tuple[*Ts]):
#         self._store = arg

# def process(arg: Record[*tuple[float, ...]]): ...

# process(Record((4.2, 5.2))) # mypy passes
# process(Record(())) # mypy passes

# process(Record((4.2, 5.2, 'x'))) # mypy fails: error:
#     # Argument 1 to "Record" has incompatible type
#     # "tuple[float, float, str]"; expected "tuple[float, ...]"


#-----------------------------------------

# class Record[*Ts]:
#     def __init__(self, arg: tuple[*Ts]):
#         self._store = arg

# def process(arg: Record[int, *tuple[float, ...], str]): ...

# process(Record((3, 4.2, 5.2, 'x'))) # mypy passes
# process(Record((3, 'x'))) # mypy passes

# process(Record((3, 4.2, 5.2, False))) # mypy fails: error:
#     # Argument 1 to "Record" has incompatible type
#     # "tuple[int, float, float, bool]";
#     # expected "tuple[int, *tuple[float, ...], str]"


#-----------------------------------------

# class TaggedRecord[T, *Ts]:
#     def __init__(self, tag: T, values: tuple[*Ts]):
#         self._tag = tag
#         self._values = values

# def process(arg: TaggedRecord[str, str, *tuple[float, ...]]): ...

# process(TaggedRecord('foo', ('x', 4.2, 5.2))) # mypy passes

# process(TaggedRecord(3, ('x', 4.2, 5.2))) # mypy fails: error:
#     # Argument 1 to "TaggedRecord" has incompatible type "int";
#     # expected "str"

# process(TaggedRecord('foo', (4.2, 5.2, 'x'))) # mypy fails: error:
#     # Argument 2 to "TaggedRecord" has incompatible type
#     # "tuple[float, float, str]";
#     # expected "tuple[str, *tuple[float, ...]]"


import static_frame as sf
import numpy as np

def process(
    v: sf.Frame[
        sf.IndexDate,            # type of Frame index labels
        sf.Index[np.str_],       # type of Frame column labels
        np.int64,                # type of Frame first column
        *tuple[np.float64, ...], # type of remaining columns
        ],
    ) -> sf.Series[
        sf.IndexDate,      # type of Series in0dex labels
        np.float64,        # type of Series values
        ]: ...

f1: sf.Frame[sf.IndexDate, sf.Index[np.str_], np.int64, np.float64] = sf.Frame.from_fields(([20, 30], [1.2, 5.4]), index=sf.IndexDate(('2025-01-03', '2025-02-04')), columns=sf.Index(('a', 'b')))

process(f1)
