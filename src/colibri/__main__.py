import sys
import colibri
import xmltodict
from typing import Any
import importlib.metadata
import time


def main(argv: list[str]):

    # Get version number from pyproject.toml
    __version__ = importlib.metadata.version("colibri")

    colibri_start_time = time.time_ns()
    print("Starting COLIBRI", __version__)
    print()

    # Define tasks
    tasks = {
        'ROIMeans': colibri.tasks.task_roi_means,
        'TACFit': colibri.tasks.task_tac_fit,
        'TACPlot': colibri.tasks.task_tac_plot,
        'Correction': colibri.tasks.task_apply_correction,
        'SaveTable': colibri.tasks.task_save_table,
        'LoadTable': colibri.tasks.task_load_table
    }

    # Created named object container
    named_obj: dict[str, Any] = {}

    # Parse XML input file
    if len(argv) != 1:
        exit("Missing command line argument: path to an XML file. Exiting!")
    xml_file = open(argv[0], "r")
    task_tree = xmltodict.parse(xml_file.read(), force_list='task')
    root = task_tree['colibri']

    for task in root['task']:
        tasks[task['@name']](task, named_obj)

    run_time = (time.time_ns() - colibri_start_time) * 1e-9
    print("All tasks completed.")
    print(f'Total run time: {run_time:.1f} seconds.')
    print()

    print("COLIBRI ended!")


if __name__ == "__main__":
    main(sys.argv[1:])
