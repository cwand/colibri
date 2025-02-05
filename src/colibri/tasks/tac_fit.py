from typing import OrderedDict, Callable, Any

import colibri
from colibri.tasks import task_common
import lmfit
import matplotlib.pyplot as plt
import numpy as np

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
                 tcut: int) -> None:
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
    plt.show()
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
    params = {}
    for value, name in zip(param_values, param_names):
        params[name] = value
    ymodel = np.array(model(time_data, input_data, **params))
    s2 = np.exp(2.0 * params['__lnsigma'])
    for param in params:
        if not param_bounds[param][0] < params[param] < param_bounds[param][1]:
            return -np.inf
    return -0.5 * np.sum((np.array(tissue_data) - ymodel) ** 2 / s2 +
                         np.log(2.0 * np.pi * s2))


def _fit_emcee(time_data: list[float],
               tissue_data: list[float],
               input_data: list[float],
               model: Callable[[list[float], list[float], dict[str, float]],
                                 list[float]],
               params: dict[str, dict[str, float]],
               labels: dict[str, str],
               tcut: int) -> None:

    param_start = []
    param_names = []
    param_bounds = {}
    for param in params:
        param_names.append(param)
        param_start.append(params[param]['value'])
        param_bounds[param] = (params[param]['min'], params[param]['max'])

    time_data_cut = time_data[0:tcut]
    input_data_cut = input_data[0:tcut]
    tissue_data_cut = tissue_data[0:tcut]

    n_walkers = 50
    n_dim = len(param_start)
    steps = 30

    start_p = np.array(param_start) + 1e-5 * np.random.randn(n_walkers, n_dim)
    with Pool(8) as pool:
        sampler = emcee.EnsembleSampler(n_walkers, n_dim, _log_prob,
                                        args=(param_names, model, time_data_cut,
                                              input_data_cut, tissue_data_cut,
                                              param_bounds),
                                        pool=pool)
        sampler.run_mcmc(start_p, steps, progress=True)

    fig, axes = plt.subplots(n_dim, figsize=(10, 7), sharex=True)
    samples = sampler.get_chain()
    for i in range(n_dim):
        ax = axes[i]
        ax.plot(samples[:, :, i], "k", alpha=0.3)
        ax.set_xlim(0, len(samples))
        ax.set_ylabel(param_names[i])
        ax.yaxis.set_label_coords(-0.1, 0.5)

    axes[-1].set_xlabel("step number")
    plt.show()

    try:
        tau = sampler.get_autocorr_time()
        print("Autocorrelation times:")
        for i in len(param_names):
            print(f'   {param_names[i]}: {tau[i]:.1f}')
    except:
        print("Autocorrelation could not be estimated")
    print()

    flat_samples = sampler.get_chain(discard=0, thin=1, flat=True)
    corner.corner(flat_samples, labels=param_names, truths=param_start)
    plt.show()

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

    print("Starting TAC-fitting.")

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

    print("Fitting TAC data to model", fit_model, ".")

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
            tcut=t_cut
        )
    elif method == 'emcee':
        _fit_emcee(
            time_data=tac[time_label],
            tissue_data=tac[tis_label],
            input_data=tac[inp_label],
            model=models[fit_model],
            params=params,
            labels={'input': inp_label, 'tissue': tis_label},
            tcut=t_cut
        )
    else:
        print("Unknown fit method:", method,
              ". Possible options are leastsq and emcee.")
        print("Stopping fit-task.")
        print()
