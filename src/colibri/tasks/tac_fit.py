from typing import OrderedDict, Callable, Any, Optional

import colibri
from colibri.tasks import task_common
import lmfit
import matplotlib.pyplot as plt
import numpy as np
import os
import time

import emcee
import corner
from multiprocessing import Pool


def _fit_leastsq(time_data: list[float],
                 tissue_data: list[float],
                 input_data: list[float],
                 model: Callable[[list[float], list[float], dict[str, float]],
                                 list[float]],
                 params: dict[str, dict[str, float]],
                 labels: dict[str, str],
                 tcut: int,
                 output: Optional[str]) -> None:
    # Fit a TAC to a given function using lmfit

    # Create lmfit Parameters-object
    parameters = lmfit.create_params(**params)

    # Define model to fit
    fit_model = lmfit.Model(model, independent_vars=['t', 'in_func'])
    # Run fit from initial values
    res = fit_model.fit(tissue_data[0:tcut],
                        t=time_data[0:tcut],
                        in_func=input_data[0:tcut],
                        params=parameters)

    # Report!
    lmfit.report_fit(res)
    # Calculate best fitting model
    best_fit = model(time_data[0:tcut],
                     input_data[0:tcut],
                     **res.best_values)
    # Calculate prediction interval
    e_fit = res.eval_uncertainty(t=time_data[0:tcut], sigma=2)
    p_fit = res.dely_predicted

    print("... done!")
    print()

    print("Plotting...")
    fig, ax = plt.subplots()
    ax.plot(time_data, tissue_data, 'gx', label=labels['tissue'])
    ax.plot(time_data, input_data, 'rx--', label=labels['input'])
    ax.plot(time_data[0:tcut], best_fit, 'k-', label="Fit")
    ax.fill_between(time_data[0:tcut],
                    best_fit - p_fit,
                    best_fit + p_fit,
                    color="#d0d0a060", label=r'$2\sigma$ prediction interval')
    ax.fill_between(time_data[0:tcut],
                    best_fit - e_fit,
                    best_fit + e_fit,
                    color="#c0c0c0", label=r'$2\sigma$ confidence interval')
    ax.set_xlabel('Time [sec]')
    ax.set_ylabel('Mean ROI-activity concentration [Bq/mL]')

    plt.legend()
    plt.grid(visible=True)
    if output is None:
        plt.show()
    else:
        fit_png_path = os.path.join(output, "fit.png")
        print("Saving image to file", fit_png_path, ".")
        plt.savefig(fit_png_path)
        plt.clf()
    print("... done!")
    print()


def _log_prob(param_values: list[float],
              param_names: list[str],
              model: Callable[[list[float], list[float], dict[str, float]],
                              list[float]],
              time_data: list[float],
              input_data: list[float],
              tissue_data: list[float],
              param_bounds: dict[str, (float, float)]) -> float:
    # Defines the probability distribution used by emcee (below) to sample
    # the parameter distribution of a fit model

    # Put parameters into dict object (required by model interface)
    params = {}
    for value, name in zip(param_values, param_names):
        params[name] = value

    # Calculate the model given the current parameters
    ymodel = np.array(model(time_data, input_data, **params))

    # __lnsigma is the natural log of the uncertainty of the data (assumed to
    # be a constant), which is treated like a parameter of the model
    s2 = np.exp(2.0 * params['__lnsigma'])

    # Prior parameter distribution:
    # Assumed to be uniform with bounds. i.e., if a parameter is outside the
    # bounds, the likelihood is 0 (so the log-likelihood is -inf)
    for param in params:
        if not param_bounds[param][0] < params[param] < param_bounds[param][1]:
            return -np.inf

    # Calculate and return the log-proability distribution (non-normalised)
    return -0.5 * np.sum((np.array(tissue_data) - ymodel) ** 2 / s2 +
                         np.log(2.0 * np.pi * s2))


def _fit_emcee(time_data: list[float],
               tissue_data: list[float],
               input_data: list[float],
               model: Callable[[list[float], list[float], dict[str, float]],
                                 list[float]],
               params: dict[str, dict[str, float]],
               labels: dict[str, str],
               tcut: int,
               output: Optional[str]) -> None:
    # Sample the posterior parameter distribution space using Monte Carlo
    # simulations with the emcee-package

    # Parameters need to be unpacked when passed to emcee
    param_start = []  # Contains the optimised parameters (from an actual fit)
    param_names = []  # Contains the name of the parameters in the model
    param_bounds = {}  # Contains the parameter bounds (priors)
    for param in params:
        param_names.append(param)
        param_start.append(params[param]['value'])
        param_bounds[param] = (params[param]['min'], params[param]['max'])

    # Cut data as required
    time_data_cut = time_data[0:tcut]
    input_data_cut = input_data[0:tcut]
    tissue_data_cut = tissue_data[0:tcut]

    # Set emcee parameters
    n_walkers = 50  # Number of walkers used to search the space
    n_dim = len(param_start)  # Dimensionality of the parameter space
    steps = 5000  # Number of update steps

    # Start the walkers in a gaussian ball around the optimised parameters
    start_p = np.array(param_start) + 1e-5 * np.random.randn(n_walkers, n_dim)

    # Run as a multithreaded pool
    with Pool(8) as pool:
        # Start MC
        sampler = emcee.EnsembleSampler(n_walkers, n_dim, _log_prob,
                                        args=(param_names, model, time_data_cut,
                                              input_data_cut, tissue_data_cut,
                                              param_bounds),
                                        pool=pool)
        sampler.run_mcmc(start_p, steps, progress=False)
    print("... done!")
    print()

    # Plot the history of each walker
    fig, axes = plt.subplots(n_dim, figsize=(10, 7), sharex=True)
    samples = sampler.get_chain()
    for i in range(n_dim):
        ax = axes[i]
        ax.plot(samples[:, :, i], "k", alpha=0.3)
        ax.set_xlim(0, len(samples))
        ax.set_ylabel(param_names[i])
        ax.yaxis.set_label_coords(-0.1, 0.5)

    axes[-1].set_xlabel("step number")
    if output is None:
        plt.show()
    else:
        samples_png_path = os.path.join(output, "samples.png")
        print("Saving samples image to file", samples_png_path, ".")
        plt.savefig(samples_png_path)
        plt.clf()

    # Try to calculate autocorrelation times
    # (might fail if "steps" is too small)
    try:
        tau = sampler.get_autocorr_time()
        print("Autocorrelation times:")
        for i in len(param_names):
            print(f'   {param_names[i]}: {tau[i]:.1f}')
    except:
        print("Autocorrelation could not be estimated")
    print()

    # Make corner plot
    flat_samples = sampler.get_chain(discard=0, thin=1, flat=True)
    corner.corner(flat_samples, labels=param_names, truths=param_start)
    if output is None:
        plt.show()
    else:
        corner_png_path = os.path.join(output, "corner.png")
        print("Saving corner image to file", corner_png_path, ".")
        plt.savefig(corner_png_path)
        plt.clf()

    # Print parameter quantiles
    print("Parameter quantiles (5%, 16%, 50%, 84%, 95%)")
    for i in range(n_dim):
        mcmc = np.percentile(flat_samples[:, i], [5, 16, 50, 84, 95])
        print(param_names[i], ":", mcmc)
    print()




def task_tac_fit(task: OrderedDict[str, Any],
                 named_obj: dict[str, Any]):
    """Run the TACFit task. Fits model parameters to a measured TAC. The fit
    is shown in standard out and a figure of the fitted curve and the data is
    shown.
    The input is an xml-structure, which must have the following content (in
    any order):

    <tac_name>TAC_KEY_IN_NAMED_OBJ</tac_name>
    <time_label>LABEL_OF_TIME_DATA</time_label>
    <inp_label>LABEL_OF_INPUT_FUNCTION_DATA</inp_label>
    <tis_label>LABEL_OF_TISSUE_DATA</tis_label>
    <method>FIT_METHOD</method> <!-- OPTIONS: leastsq, emcee -->
    <model>FIT_MODEL</model>
    <param>
        <name>PARAM1_NAME</name>
        <init>PARAM1_INIT_VALUE</init>
        <min>PARAM1_MIN_VALUE</min> <!-- OPTIONAL -->
        <max>PARAM1_MAX_VALUE</max> <!-- OPTIONAL -->
    </param>
    <param>
        <name>PARAM2_NAME</name>
        <init>PARAM2_INIT_VALUE</init>
    </param>
    ...
    """

    task_common._print_task("TACFit", task)
    task_start_time = time.time_ns()

    # Check required tags are present
    task_common._check_tags("TACFit", task,
                            ['tac_name', 'time_label', 'inp_label',
                             'tis_label', 'method', 'model'])

    # Get the data path
    tac_name = str(task['tac_name'])

    # Get labels of relevant TACs
    inp_label = str(task['inp_label'])
    time_label = str(task['time_label'])
    tis_label = str(task['tis_label'])

    # Get the fit method
    method = str(task['method'])

    # Get required fit model:
    fit_model = str(task['model'])

    # Load TAC data
    print("Loading TAC-data as ", tac_name, " in named_obj...")
    tac = named_obj[tac_name]
    print("... done!")
    print()

    # Get tcut if required
    t_cut = len(tac[time_label])
    if 'tcut' in task:
        t_cut = int(task['tcut'])

    # Get output directory if required
    output = None
    if 'output' in task:
        output = task['output']

    print("Fitting TAC data to model", fit_model, ".")
    print("Using method", method, ".")
    print()

    # Dict of possible models
    models = {
        'step2': colibri.model.model_step_2,
        'fermi2': colibri.model.model_fermi_2,
        'step_fermi': colibri.model.model_step_fermi,
        'step': colibri.model.model_step,
        'patlak': colibri.model.model_patlak
    }

    # Put parameters into a dict
    params = {}
    for param in task['param']:
        # Initial parameter value
        param_dict = {'value': float(param['init'])}
        # Optional parameter minimum
        if 'min' in param:
            param_dict['min'] = float(param['min'])
        # Optional parameter maximum
        if 'max' in param:
            param_dict['max'] = float(param['max'])
        # Get parameter name and store in dict
        params[param['name']] = param_dict

    # Run the fit based on the method:
    if method == 'leastsq':
        # Fit using lmfit
        _fit_leastsq(
            time_data=tac[time_label],
            tissue_data=tac[tis_label],
            input_data=tac[inp_label],
            model=models[fit_model],
            params=params,
            labels={'input': inp_label, 'tissue': tis_label},
            tcut=t_cut,
            output=output
        )
    elif method == 'emcee':
        _fit_emcee(
            time_data=tac[time_label],
            tissue_data=tac[tis_label],
            input_data=tac[inp_label],
            model=models[fit_model],
            params=params,
            labels={'input': inp_label, 'tissue': tis_label},
            tcut=t_cut,
            output=output
        )
    else:
        print("Unknown fit method:", method,
              ". Possible options are leastsq and emcee.")
        print("Stopping fit-task.")
        print()

    task_run_time = (time.time_ns() - task_start_time) * 1e-9
    print(f'Task run time: {task_run_time:.2f} seconds')

    print("------------------------------------------------------------------")
    print()
    print()