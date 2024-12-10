from typing import OrderedDict, Any
import colibri
import lmfit
import matplotlib.pyplot as plt


def task_tac_fit(task: OrderedDict[str, Any],
                 named_obj: dict[str, Any]):
    """Run the TACFit task. Fits model parameters to a measured TAC. The fit
    is shown in standard out and a figure of the fitted curve and the data is
    shown.
    The input is an xml-structure, which must have the following content (in
    any order):

    <tac_path>PATH_TO_TAC_FILE</tac_path>
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

    # Get the data path
    tac_path = str(task['tac_path'])

    # Get labels of relevant TACs
    inp_label = str(task['inp_label'])
    time_label = str(task['time_label'])
    tis_label = str(task['tis_label'])

    # Get required fit model:
    fit_model = str(task['model'])

    # Load TAC data
    print("Loading TAC-data from", tac_path, "...")
    tac = colibri.load_table(tac_path)
    print("... done!")
    print()

    # Get tcut if required
    t_cut = len(tac[time_label])
    if 'tcut' in task:
        t_cut = int(task['tcut'])

    print("Fitting TAC data to model ", fit_model, ".")

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

    # Create lmfit Parameters-object
    parameters = lmfit.create_params(**params)

    # Define model to fit
    model = lmfit.Model(models[fit_model], independent_vars=['t', 'in_func'])
    # Run fit from initial values
    res = model.fit(tac[tis_label][0:t_cut], t=tac[time_label][0:t_cut],
                    in_func=tac[inp_label][0:t_cut],
                    params=parameters)

    # Report!
    lmfit.report_fit(res)
    # Calculate best fitting model
    best_fit = models[fit_model](t=tac[time_label][0:t_cut],  # type: ignore
                                 in_func=list(tac[inp_label][0:t_cut]),
                                 **res.best_values)
    # Calculate prediction interval
    e_fit = res.eval_uncertainty(t=tac[time_label][0:t_cut], sigma=2)
    p_fit = res.dely_predicted

    print("... done!")
    print()

    print("Plotting...")
    fig, ax = plt.subplots()
    ax.plot(tac[time_label], tac[tis_label], 'gx', label=tis_label)
    ax.plot(tac[time_label], tac[inp_label], 'rx--', label=inp_label)
    ax.plot(tac[time_label][0:t_cut], best_fit, 'k-', label="Fit")
    ax.fill_between(tac[time_label][0:t_cut],
                    best_fit - p_fit,
                    best_fit + p_fit,
                    color="#d0d0a060", label=r'$2\sigma$ prediction interval')
    ax.fill_between(tac[time_label][0:t_cut],
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
