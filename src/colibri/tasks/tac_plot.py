from typing import OrderedDict, Any
from colibri.tasks import task_common
import matplotlib.pyplot as plt


def task_tac_plot(task: OrderedDict[str, Any],
                  named_obj: dict[str, Any]):
    """Run the TACPlot task. Shows a series of measured time activity curves
    (TACs).
    The input is an xml-structure, which must have the following content (in
    any order):

    <tac_name>TAC_KEY_IN_NAMED_OBJ</tac_name>
    <time_label>LABEL_OF_TIME_DATA</time_label>
    <labels>LABEL1,LABEL2,...</inp_label>
    <xlabel>TEXT_ON_X_AXIS</xlabel> <!-- OPTIONAL -->
    <ylabel>TEXT_ON_Y_AXIS</ylabel> <!-- OPTIONAL -->

    The <tac_name> tag describes the name of the TAC-table in the named object
    containter (previously computed using e.g. the ROIMeans task.
    The <time_label> tag gives the label name of the acquisition times in the
    TAC-table.
    The <labels> tag sets which of the labels in the TAC-table should be
    plotted. Should be a comma-separated list.
    To write custom text on the axis, the <xlabel> and <ylabel> tags can be
    used. If these are not given, no text is wirtten on the axis.
    As an example, we assume a TAC-table has been computed using the ROIMeans
    task, and the resulting table (dict), stored in named_obj under the name
    'tac_table', looks like this:
    {
        'tacq': [0.0, 1.0, 2.0, 3.0],
        '1'   : [0.0, 5.0, 7.0, 3.0],
        '2'   : [1.0, 2.0, 4.0, 8.0],
        'Q'   : [0.5, 3.0, 7.0, 400.0],
    }
    If we want to plot '1' and '2' as a function of 'tacq', then the XML input
    should look like:

    <tac_name>tac_table</tac_name>
    <time_label>tacq</time_label>
    <labels>1,2</labels>
    <xlabel>Time [sec]</xlabel>
    <ylabel>ROI Mean activity conc. [Bq/mL]</ylabel>
    """

    print("Starting TAC-plotting...")

    # Check required tags are present
    task_common._check_tags("TACPlot", task,
                            ['tac_name', 'time_label', 'labels'])

    # Get data from named object container
    tac = named_obj[task['tac_name']]
    time_data = tac[task['time_label']]
    # Split required labels by comma
    plot_labels = task['labels'].split(',')

    # Start plotting
    fig, ax = plt.subplots()
    for label in plot_labels:
        ax.plot(time_data, tac[label], label=label)

    # If labels are required, set them
    if 'xlabel' in task:
        ax.set_xlabel(task['xlabel'])
    if 'ylabel' in task:
        ax.set_ylabel(task['ylabel'])

    # Show legend, grid and figure
    plt.legend()
    plt.grid(visible=True)
    plt.show()

    print("...done")
    print()
