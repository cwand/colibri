import sys
import colibri
import xmltodict
from typing import Any


def main(argv: list[str]):

    print("Starting COLIBRI")
    print()

    # Define tasks
    tasks = {
        'ROIMeans': colibri.tasks.task_roi_means,
        'TACFit': colibri.tasks.task_tac_fit,
        'Correction': colibri.tasks.task_apply_correction
    }

    # Created named object container
    named_obj: dict[str, Any] = {}

    # Parse XML input file
    if len(argv) != 1:
        exit("Missing command line argument: path to an XML file.")
    xml_file = open(argv[0], "r")
    task_tree = xmltodict.parse(xml_file.read(), force_list=('task'))
    root = task_tree['colibri']

    for task in root['task']:
        tasks[task['@name']](task, named_obj)

    print("COLIBRI ended!")


if __name__ == "__main__":
    main(sys.argv[1:])
