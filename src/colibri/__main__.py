import sys

import colibri
import xmltodict


def main(argv: list[str]):

    print("Starting COLIBRI")
    print()

    tasks = {
        'ROIMeans': colibri.task_roi_means,
        'TACFit': colibri.task_tac_fit
    }

    # Parse XML input file
    if len(argv) != 1:
        exit("Missing command line argument: path to an XML file.")
    xml_file = open(argv[0], "r")
    task_tree = xmltodict.parse(xml_file.read(), force_list=('task'))
    root = task_tree['colibri']

    for task in root['task']:
        tasks[task['@name']](task)

    print("COLIBRI ended!")


if __name__ == "__main__":
    main(sys.argv[1:])
