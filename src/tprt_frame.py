# runtime analysis on Frame
import static_frame as sf
import numpy as np
import typing as tp

TFrameDateIntInt = sf.Frame[sf.IndexDate, sf.Index[np.str_], np.int64, np.int64]
TSeriesYMBool = sf.Series[sf.IndexYearMonth, np.bool_]
TSeriesDFloat = sf.Series[sf.IndexDate, np.float64]

@sf.CallGuard.warn
def process2(v: TFrameDateIntInt, q: TSeriesYMBool) -> TSeriesDFloat:
    t = v.index.iter_label().apply(lambda l: q[l.astype('datetime64[M]')]) # type: ignore
    s = np.where(t, 0.5, 0.25)
    return tp.cast(TSeriesDFloat, (v.via_T * s).mean(axis=1))



q: TSeriesYMBool = sf.Series([True, False], index=sf.IndexYearMonth.from_date_range('2021-12', '2022-01'))



TFrameDateIntFloat = sf.Frame[sf.IndexDate, sf.Index[np.str_], np.int64, np.float64]
v1: TFrameDateIntFloat = sf.Frame.from_fields([range(5), np.arange(3, 8) * 0.5], columns=('a', 'b'), index=sf.IndexDate.from_date_range('2021-12-30', '2022-01-03'))
v2: TFrameDateIntInt = sf.Frame.from_fields([range(5), range(3, 8)], columns=('a', 'b'), index=sf.IndexDate.from_date_range('2021-12-30', '2022-01-03'))

x = process2(v1, q)
# static_frame.core.type_clinic.ClinicError:
# In args of (v: Frame[IndexDate, Index[str_], int64, int64], q: Series[IndexYearMonth, bool_]) -> Series[IndexDate, float64]
# └── Frame[IndexDate, Index[str_], int64, int64]
#     └── Expected int64, provided float64 invalid


TFrameDateNum = sf.Frame[sf.IndexDate, sf.Index[np.str_], np.number[tp.Any], np.number[tp.Any]]

@sf.CallGuard.warn
def process3(v: TFrameDateNum, q: TSeriesYMBool) -> TSeriesDFloat:
    t = v.index.iter_label().apply(lambda l: q[l.astype('datetime64[M]')]) # type: ignore
    s = np.where(t, 0.5, 0.25)
    return tp.cast(TSeriesDFloat, (v.via_T * s).mean(axis=1))

x = process3(v1, q)
x = process3(v2, q)

TFrameDateIntIntInt = sf.Frame[sf.IndexDate, sf.Index[np.str_], np.int64, np.int64, np.int64]
v3: TFrameDateIntIntInt = sf.Frame.from_fields([range(5), range(3, 8), range(1, 6)], columns=('a', 'b', 'c'), index=sf.IndexDate.from_date_range('2021-12-30', '2022-01-03'))


x = process3(v3, q)
# static_frame.core.type_clinic.ClinicError:
# In args of (v: Frame[IndexDate, Index[str_], number[Any], number[Any]], q: Series[IndexYearMonth, bool_]) -> Series[IndexDate, float64]
# └── Frame[IndexDate, Index[str_], number[Any], number[Any]]
#     └── Expected Frame has 2 dtype, provided Frame has 3 dtype



TFrameDateNums = sf.Frame[sf.IndexDate, sf.Index[np.str_], *tuple[np.number[tp.Any], ...]]
@sf.CallGuard.check
def process4(v: TFrameDateNums, q: TSeriesYMBool) -> TSeriesDFloat:
    t = v.index.iter_label().apply(lambda l: q[l.astype('datetime64[M]')]) # type: ignore
    s = np.where(t, 0.5, 0.25)
    return tp.cast(TSeriesDFloat, (v.via_T * s).mean(axis=1))

x = process4(v3, q)


TFrameDateNumsValid = sf.Frame[tp.Annotated[sf.IndexDate, sf.Require.Len(10)], tp.Annotated[sf.Index[np.str_], sf.Require.LabelsOrder('a', 'b', ...)], *tuple[np.number[tp.Any], ...]]
@sf.CallGuard.check
def process5(v: TFrameDateNumsValid, q: TSeriesYMBool) -> TSeriesDFloat:
    t = v.index.iter_label().apply(lambda l: q[l.astype('datetime64[M]')]) # type: ignore
    s = np.where(t, 0.5, 0.25)
    return tp.cast(TSeriesDFloat, (v.via_T * s).mean(axis=1))

x = process5(v3, q)
# static_frame.core.type_clinic.ClinicError:
# In args of (v: Frame[Annotated[IndexDate, Len(10)], Index[str_], Unpack[tuple[number[Any], ...]]], q: Series[IndexYearMonth, bool_]) -> Series[IndexDate, float64]
# └── Frame[Annotated[IndexDate, Len(10)], Index[str_], Unpack[tuple[number[Any], ...]]]
#     └── Annotated[IndexDate, Len(10)]
#         └── Len(10)
#             └── Expected length 10, provided length 5

