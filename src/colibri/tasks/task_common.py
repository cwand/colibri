from typing import OrderedDict, Any


def _check_tags(task_name: str,
                task: OrderedDict[str, Any],
                required_tags: list[str]):
    """Private function. Checks that all required tags are present in a task
    tree and raises a relevant exception if not.
    """

    missing = []  # Container for missing required tags
    for k in required_tags:
        if k not in task:
            # Append all missing tags to container
            missing.append(k)
    # If there are no missing tags, do nothing
    # If there are missing tags, raise exception with relevant message
    if len(missing) > 0:
        msg = "Missing tags in " + task_name + " task:"
        for t in missing:
            msg = msg + " <" + t + ">"
        raise KeyError(msg)


def _print_task_options(task: OrderedDict[str, Any],
                        indent: int):
    for tag in task:
        indent_string = ' ' * indent * 3
        if isinstance(task[tag], list):
            print(f'{indent_string}{tag}:')
            for elem in task[tag]:
                _print_task_options(elem, indent + 1)
                print()
        else:
            dots_needed = 68 - len(indent_string) - len(tag) - len(str(task[tag]))
            print(f'{indent_string}{tag}: {"." * dots_needed} {task[tag]}')

def _print_task(task_name: str,
                task: OrderedDict[str, Any]):
    """Private function. Prints a task setup to the user."""
    print(f'Starting task: {task_name.upper()}')
    print('   ---   ---   ---')
    print('Task options:')
    _print_task_options(task, 1)
    print('   ---   ---   ---')
    print()