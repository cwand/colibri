from typing import OrderedDict, Any

def task_roi_means(task: OrderedDict[str, Any],
                   named_obj: dict[str, Any]): ...

def task_tac_fit(task: OrderedDict[str, Any],
                 named_obj: dict[str, Any]): ...

def task_apply_correction(task: OrderedDict[str, Any],
                          named_obj: dict[str, Any]): ...