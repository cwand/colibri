import numpy as np
import scipy


def _model_fermi_2_integrand(tau: float, t: float,
                             amp1: float,
                             extent1: float,
                             width1: float,
                             amp2: float,
                             extent2: float,
                             width2: float,
                             tp: list[float], in_func: list[float]) -> float:
    """Defines the integrand when the input response is a 2-step
    fermi-function. The response function is defined on the domain
    [0, infinty). It has value amp1+amp2 on at t=0, stays nearly constant until
    t=extent1 where it transitions smoothly to a vlaue of amp2. It then stays
    nearly constant at amp2 until t=extent2, where it smoothly approaches a
    value of 0.
    The integrand is the product of the response function evaluated at t-tau
    and the input function evaluated at tau. The input function is interpolated
    linearly between the sampled points.

    Arguments:
    tau     --  The integration variable.
    t       --  The time point at which the integral is evaluated.
    amp1    --  The amplitude of the first fermi function.
    extent1 --  The length of the first fermi function.
    width1  --  The decay width of the first fermi function.
    amp2    --  The amplitude of the second fermi function.
    extent2 --  The length of the second fermi function.
    width2  --  The decay width of the second fermi function
    tp      --  The time points of the input function samples.
    in_func --  The input function samples.

    Return value:
    The integrand evaluated at time point t and integration variable value tau.
    """

    # Compute response function value at t - tau
    resp = (amp1 *
            (1.0 + np.exp(-extent1 / width1)) /
            (1.0 + np.exp((t - tau - extent1) / width1)) +
            amp2 * (1.0 + np.exp(-extent2 / width2)) /
            (1.0 + np.exp((t - tau - extent2) / width2)))

    # Return integrand value.
    # Numpy.interp returns an array, which is cast back to a float value.
    return float(resp) * float(np.interp(tau, tp, in_func))


def model_fermi_2(t: list[float],
                  in_func: list[float],
                  **kwargs: float) -> list[float]:
    """Solves the model where the input response function is assumed to be a
    2-step fermi-function.
    This function calculates the convolution of a sampled input function with
    a 2-step fermi-function.
    The formula for the fermi function is:
    f = A1 * (1 + exp(-t1/b1)) / (1 + exp((t-t1)/b1)) + ...
    The ... indicates a second term of exactly the same construction, but
    other parameters.
    A1 is called the amplitude (of the first fermi function)
    t1 is called the extent (of the first fermi function)
    b1 is called the width (of the first fermi function)
    The convolution is evaluated at the same time points as the sampled
    input function and returned as a list.
    The convolution is performed numerically using scipy.integrate.quad and
    the input function is interpolated linearly between sample points.

    Arguments:
    t       --  The time points of the input function samples.
    in_func --  The input function samples.
    amp1    --  The amplitude of the first fermi function.
    extent1 --  The length of the first function.
    width1  --  The decay width of the first fermi function.
    amp2    --  The amplitude of the second fermi function.
    extent2 --  The length of the second fermi function.
    width2  --  The decay width of the second fermi function.

    Return value:
    A list containing the modeled values at each time point.
    """
    res = []
    for ti in t:
        # For each time point the integrand (see above) is integrated.
        # We use a higher subproblem limit and higher error tolerances to avoid
        # running into problems, since the functions are not necessarily very
        # well-behaved.
        y = scipy.integrate.quad(_model_fermi_2_integrand, 0, ti,
                                 args=(ti, kwargs['amp1'], kwargs['extent1'],
                                       kwargs['width1'], kwargs['amp2'],
                                       kwargs['extent2'], kwargs['width2'],
                                       t, in_func),
                                 limit=100,
                                 epsabs=1e-2, epsrel=1e-4)
        res.append(y[0])
    return res
