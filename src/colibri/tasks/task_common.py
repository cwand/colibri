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
