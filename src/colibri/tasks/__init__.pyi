from typing import OrderedDict, Any

def _check_tags(task_name: str,
                task: OrderedDict[str, Any],
                required_tags: list[str]): ...

def task_save_table(task: OrderedDict[str, Any],
                    named_obj: dict[str, Any]): ...

def task_load_table(task: OrderedDict[str, Any],
                    named_obj: dict[str, Any]): ...

def task_roi_means(task: OrderedDict[str, Any],
                   named_obj: dict[str, Any]): ...

def task_tac_fit(task: OrderedDict[str, Any],
                 named_obj: dict[str, Any]): ...

def task_apply_correction(task: OrderedDict[str, Any],
                          named_obj: dict[str, Any]): ...