from typing import OrderedDict, Any
import numpy as np


def task_apply_correction(task: OrderedDict[str, Any],
                          named_obj: dict[str, Any]):
    """Apply a data correction to a set of data. Several correction strategies
    can be used, and each is selected by setting the xml-tag <type>:

    Scale correction:
    Multiply one label in a table with a set scalar. The xml-structure
    should then look like this.
    <type>Scale</img_path>
    <table_name>TABLE_NAME_IN_NAMED_OBJ</tac_in>
    <label_in>LABEL_TO_BE_SCALED<label_in>
    <label_out>NEW_SCALED_DATA_LABEL</label_out>
    <factor>SCALAR_TO_USE_AS_FACTOR</factor>
    """

    print("Applying correction.")

    # Check correction type:
    cor_type = str(task['type'])
    if cor_type == "Scale":
        _scale_tac(task, named_obj)


def _scale_tac(task: OrderedDict[str, Any],
               named_obj: dict[str, Any]):
    # Get the input table from named obj
    print("Loading table", task['table_name'], "from named_obj...")
    tab = named_obj[task['table_name']]
    print("... done!")

    # Scale desired label
    new_label = task['label_out']
    old_label = task['label_in']
    factor = float(task['factor'])
    print("Applying correction to label", old_label,
          "and saving as label", new_label, "...")
    tab[new_label] = np.array(tab[old_label]) * factor
    print("... done!")
