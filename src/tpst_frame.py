# static analysis on Frame
import static_frame as sf
import numpy as np
import typing as tp

TFrameDateIntInt = sf.Frame[sf.IndexDate, sf.Index[np.str_], np.int64, np.int64]
TSeriesYMBool = sf.Series[sf.IndexYearMonth, np.bool_]
TSeriesDFloat = sf.Series[sf.IndexDate, np.float64]

def process(v: TFrameDateIntInt, q: TSeriesYMBool) -> TSeriesDFloat:
    t = v.index.iter_label().apply(lambda l: q[l.astype('datetime64[M]')]) # type: ignore
    s = np.where(t, 0.5, 0.25)
    return tp.cast(TSeriesDFloat, (v.via_T * s).mean(axis=1))

q: TSeriesYMBool = sf.Series([True, False], index=sf.IndexYearMonth.from_date_range('2021-12', '2022-01'))
x = process(q, q)
# tpst_frame.py: error: Argument 1 to "process" has incompatible type "Series[IndexYearMonth, bool_]"; expected "Frame[IndexDate, Index[str_], signedinteger[_64Bit], signedinteger[_64Bit]]"  [arg-type]

TFrameDateIntFloat = sf.Frame[sf.IndexDate, sf.Index[np.str_], np.int64, np.float64]
v1: TFrameDateIntFloat = sf.Frame.from_fields([range(5), np.arange(3, 8) * 0.5], columns=('a', 'b'), index=sf.IndexDate.from_date_range('2021-12-30', '2022-01-03'))
x = process(v1, q)
# tpst_frame.py: error: Argument 1 to "process" has incompatible type "Frame[IndexDate, Index[str_], signedinteger[_64Bit], floating[_64Bit]]"; expected "Frame[IndexDate, Index[str_], signedinteger[_64Bit], signedinteger[_64Bit]]"  [arg-type]

v2: TFrameDateIntInt = sf.Frame.from_fields([range(5), range(3, 8)], columns=('a', 'b'), index=sf.IndexDate.from_date_range('2021-12-30', '2022-01-03'))
x = process(v2, q)


print(x)