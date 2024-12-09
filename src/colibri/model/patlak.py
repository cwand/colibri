import scipy


def model_patlak(t: list[float],
                 in_func: list[float],
                 k1: float,
                 v0: float) -> list[float]:
    """Solves the Patlak-model.
    In the Patlak model the observed signal is assumed to be a constant k1
    times the integrated input function up until that point, plus another
    constant v0 times the input function value at that time point:
    R(t) = k1 * int(in_func, 0, t) + v0*in_func(t)

    Arguments:
    t       --  The time points of the input function samples.
    in_func --  The input function samples.
    k1      --  The constant k1 in the Patlak model.
    v0      --  The constant v0 in the Patlak model.

    Return value:
    A list containing the modeled values at each time point.
    """

    return [k1 * scipy.integrate.trapezoid(in_func[0:i+1], t[0:i+1])
            + v0 * in_func[i] for i in range(len(t))]
