import typing as tp
import static_frame as sf


def process(
        v: np.ndarray[tp.Any, np.dtype[np.int8]],
        q: np.ndarray[tp.Any, np.dtype[np.bool_]],
        ) -> np.ndarray[tp.Any, np.float64]:
    r = np.full(v.shape, 0.5)
    r[~q] = 1
    s = np.full(v.shape, 0.25)
    s[q] = 1
    return v * r * s


x = process()
