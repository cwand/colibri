from typing import OrderedDict, Any
from colibri.tasks import task_common
import colibri
import time


def task_save_table(task: OrderedDict[str, Any],
                    named_obj: dict[str, Any]):
    """Save a table (represented as a dict-object) stored in named_obj
    to a file. The XML-structure of the task should look like this:

    <name>TABLE_KEY_IN_NAMED_OBJ</name>
    <file>FILE_PATH_TO_WRITE</file>
    """

    task_common._print_task("SaveTable", task)
    task_start_time = time.time_ns()

    # Check tags
    task_common._check_tags("SaveTable", task, ['file', 'name'])

    file_path = task['file']
    table_name = task['name']
    print("Saving table", table_name, "to file", file_path, "...")
    colibri.save_table(named_obj[table_name], file_path)
    print("... done!")
    print()

    task_run_time = (time.time_ns() - task_start_time) * 1e-9
    print(f'Task run time: {task_run_time:.2f} seconds')

    print("------------------------------------------------------------------")
    print()
    print()


def task_load_table(task: OrderedDict[str, Any],
                    named_obj: dict[str, Any]):
    """Load a table (represented as a dict-object) from a file
    to named_obj. The XML-structure of the task should look like this:

    <name>TABLE_NAME_IN_NAMED_OBJ</name>
    <file>FILE_PATH_TO_READ</file>
    """

    task_common._print_task("LoadTable", task)
    task_start_time = time.time_ns()

    # Check tags:
    task_common._check_tags("LoadTable", task, ['file', 'name'])

    file_path = task['file']
    table_name = task['name']
    print("Loading table", table_name, "from file", file_path, "...")
    named_obj[table_name] = colibri.load_table(file_path)
    print("... done!")
    print()

    task_run_time = (time.time_ns() - task_start_time) * 1e-9
    print(f'Task run time: {task_run_time:.2f} seconds')

    print("------------------------------------------------------------------")
    print()
    print()
