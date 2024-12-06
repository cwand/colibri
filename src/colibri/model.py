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
               amp: float, extent: float) -> list[float]:
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
                                 args=(ti, amp, extent, t, in_func),
                                 limit=100,
                                 epsabs=1e-2, epsrel=1e-4)
        res.append(y[0])
    return res


def _model_step_2_integrand(tau: float, t: float,
                            amp1: float,
                            extent1: float,
                            amp2: float,
                            extent2: float,
                            tp: list[float], in_func: list[float]) -> float:
    """Defines the integrand when the input response is a 2-step function.
    The response function is defined on the domain [0, infinty). It has value
    amp1+amp2 on the interval [0, extent1), value amp2 on the interval
    [extent1, extent2) and value 0 on the interval [extent2, infinity).
    The integrand is the product of the response function evaluated at t-tau
    and the input function evaluated at tau. The input function is interpolated
    linearly between the sampled points.

    Arguments:
    tau     --  The integration variable.
    t       --  The time point at which the integral is evaluated.
    amp1    --  The amplitude of the step function on [0, extent1).
    extent1 --  The length of the first step function.
    amp2    --  The amplitude of the step function on [0, extent2).
    extent2 --  The length of the second step function.
    tp      --  The time points of the input function samples.
    in_func --  The input function samples.

    Return value:
    The integrand evaluated at time point t and integration variable value tau.
    """

    # Compute response function value at t - tau
    if t - tau < extent1:
        resp = amp1 + amp2
    elif t - tau < extent2:
        resp = amp2
    else:
        resp = 0.0

    # Return integrand value.
    # Numpy.interp returns an array, which is cast back to a float value.
    return resp * float(np.interp(tau, tp, in_func))


def model_step_2(t: list[float],
                 in_func: list[float],
                 amp1: float,
                 extent1: float,
                 amp2: float,
                 extent2: float) -> list[float]:
    """Solves the model where the input response function is assumed to be a
    2-step function.
    This function calculates the convolution of a sampled input function with
    a 2-step function. The step function has value amp1+amp2 on the interval
    [0, extent1), value amp2 on the interval [extent1, extent2) and value 0 on
    the interval [extent2, infinity).
    The convolution is evaluated at the same time points as the sampled
    input function and returned as a list.
    The convolution is performed numerically using scipy.integrate.quad and
    the input function is interpolated linearly between sample points.

    Arguments:
    t       --  The time points of the input function samples.
    in_func --  The input function samples.
    amp1    --  The amplitude of the step function on [0, extent1).
    extent1 --  The length of the first step function.
    amp2    --  The amplitude of the step function on [0, extent2).
    extent2 --  The length of the second step function.

    Return value:
    A list containing the modeled values at each time point.
    """
    res = []
    for ti in t:
        # For each time point the integrand (see above) is integrated.
        # We use a higher subproblem limit and higher error tolerances to avoid
        # running into problems, since the functions are not necessarily very
        # well-behaved.
        y = scipy.integrate.quad(_model_step_2_integrand, 0, ti,
                                 args=(ti, amp1, extent1, amp2, extent2,
                                       t, in_func),
                                 limit=100,
                                 epsabs=1e-2, epsrel=1e-4)
        res.append(y[0])
    return res


def _model_step_fermi_integrand(tau: float, t: float,
                                amp1: float,
                                extent1: float,
                                amp2: float,
                                extent2: float,
                                width2: float,
                                tp: list[float],
                                in_func: list[float]) -> float:
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
    resp = (amp2 * (1.0 + np.exp(-extent2 / width2)) /
            (1.0 + np.exp((t - tau - extent2) / width2)))
    if t - tau < extent1:
        resp = resp + amp1

    # Return integrand value.
    # Numpy.interp returns an array, which is cast back to a float value.
    return float(resp) * float(np.interp(tau, tp, in_func))


def model_step_fermi(t: list[float],
                     in_func: list[float],
                     amp1: float,
                     extent1: float,
                     amp2: float,
                     extent2: float,
                     width2) -> list[float]:
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
        y = scipy.integrate.quad(_model_step_fermi_integrand, 0, ti,
                                 args=(ti, amp1, extent1,
                                       amp2, extent2, width2, t, in_func),
                                 limit=100,
                                 epsabs=1e-2, epsrel=1e-4)
        res.append(y[0])
    return res


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
                  amp1: float,
                  extent1: float,
                  width1: float,
                  amp2: float,
                  extent2: float,
                  width2) -> list[float]:
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
                                 args=(ti, amp1, extent1, width1,
                                       amp2, extent2, width2, t, in_func),
                                 limit=100,
                                 epsabs=1e-2, epsrel=1e-4)
        res.append(y[0])
    return res


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
