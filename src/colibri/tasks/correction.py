from typing import OrderedDict, Any
import numpy as np
import colibri


def task_apply_correction(task: OrderedDict[str, Any],
                          named_obj: dict[str, Any]):
    """Apply a data correction to a set of data. Several correction strategies
    can be used, and each is selcted by setting the xml-tag <type>:

    TAC-scale correction:
    Multiply one label in a TAC-file with a set scalar. The xml-structure
    should then look like this.
    <type>ScaleTAC</img_path>
    <tac_in>PATH_TO_INPUT_TAC_FILE</tac_in>
    <tac_out>PATH_TO_OUTPUT_TAC_FILE</tac_out>
    <label>LABEL_TO_SCALE</label>
    <new_label>NAME_OF_CORRECTED_LABEL_IN_OUTPUT_FILE</new_label>
    <factor>SCALAR_TO_USE_AS_FACTOR</factor>
    """

    print("Applying correction.")

    # Check correction type:
    cor_type = str(task['type'])
    if cor_type == "ScaleTAC":
        _scale_tac(task, named_obj)


def _scale_tac(task: OrderedDict[str, Any],
               named_obj: dict[str, Any]):
    # Get the input TAC-file
    tac_path = str(task['tac_in'])
    print("Loading TAC from ", tac_path, "...")
    dyn = colibri.load_tac(tac_path)
    print("... done!")

    # Prepare output dict
    dyn_cor = {}

    # Scale desired label
    new_label = task['new_label']
    old_label = task['label']
    factor = float(task['factor'])
    print("Applying correction to label ", old_label, "...")
    for key in dyn.keys():
        if key == old_label:
            dyn_cor[new_label] = list(factor * np.array(dyn[old_label]))
        else:
            dyn_cor[key] = dyn[key]
    print("... done!")

    # Save the result
    out_path = str(task['tac_out'])
    print("Saving new TAC to file ", out_path, "...")
    colibri.save_tac(dyn_cor, out_path)
    print("... done!")
