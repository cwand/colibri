from typing import OrderedDict, Callable, Any

import colibri
from colibri.tasks import task_common
import lmfit
import matplotlib.pyplot as plt


def _fit_lmfit(time_data: list[float],
               tissue_data: list[float],
               input_data: list[float],
               model: Callable[..., list[float]],
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
                             'tis_label', 'model'])

    # Get the data path
    tac_name = str(task['tac_name'])

    # Get labels of relevant TACs
    inp_label = str(task['inp_label'])
    time_label = str(task['time_label'])
    tis_label = str(task['tis_label'])

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

    # Fit using lmfit
    _fit_lmfit(
        time_data=tac[time_label],
        tissue_data=tac[tis_label],
        input_data=tac[inp_label],
        model=models[fit_model],  # type: ignore
        params=params,
        labels={'input': inp_label, 'tissue': tis_label},
        tcut=t_cut
    )
