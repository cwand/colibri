import numpy as np
import scipy


def _model_step_integrand(tau: float, t: float, amp: float, extent: float,
                          tp: list[float], in_func: list[float]) -> float:
    """Defines the integrand when the input response is a step function.
    The response function is defined on the domain [0, infinty). It has value
    amp on the interval [0, extent), and value 0 on the interval
    [extent, infinity).
    The integrand is the product of the response function evaluated at t-tau
    and the input function evaluated at tau. The input function is interpolated
    linearly between the sampled points.

    Arguments:
    tau     --  The integration variable
    t       --  The time point at which the integral is evaluated
    amp     --  The amplitude of the step function
    extent  --  The length of the step function
    tp      --  The time points of the input function samples
    in_func --  The input function samples

    Return value:
    The integrand evaluated at time point t and integration variable value tau.
    """

    # Compute response function value at t - tau
    if t - tau < extent:
        resp = amp
    else:
        resp = 0.0

    # Return integrand value.
    # Numpy.interp returns an array, which is cast back to a float value.
    return resp * float(np.interp(tau, tp, in_func))


def model_step(t: list[float], in_func: list[float],
               **kwargs: float) -> list[float]:
    """Solves the model where the input response function is assumed to be a
    step function.
    This function calculates the convolution of a sampled input function with
    a step function. The step function has value amp on the interval
    [0, extent) and value 0 on the interval [extent, infinity).
    The convolution is evaluated at the same time points as the sampled
    input function and returned as a list.
    The convolution is performed numerically using scipy.integrate.quad and
    the input function is interpolated linearly between sample points.

    Arguments:
    t       --  The time points of the input function samples.
    in_func --  The input function samples.
    amp     --  The amplitude of the step function.
    extent  --  The length of the step function.

    Return value:
    A list containing the modeled values at each time point.
    """

    res = []
    for ti in t:
        # For each time point the integrand (see above) is integrated.
        # We use a higher subproblem limit and higher error tolerances to avoid
        # running into problems, since the functions are not necessarily very
        # well-behaved.
        y = scipy.integrate.quad(_model_step_integrand, 0, ti,
                                 args=(ti, kwargs['amp'], kwargs['extent'],
                                       t, in_func),
                                 limit=100,
                                 epsabs=1e-2, epsrel=1e-4)
        res.append(y[0])
    return res
