from typing import OrderedDict, Any, Callable

def _check_tags(task_name: str,
                task: OrderedDict[str, Any],
                required_tags: list[str]): ...

def task_save_table(task: OrderedDict[str, Any],
                    named_obj: dict[str, Any]): ...

def task_load_table(task: OrderedDict[str, Any],
                    named_obj: dict[str, Any]): ...

def task_roi_means(task: OrderedDict[str, Any],
                   named_obj: dict[str, Any]): ...

def task_tac_plot(task: OrderedDict[str, Any],
                  named_obj: dict[str, Any]): ...

def _fit_leastsq(time_data: list[float],
                 tissue_data: list[float],
                 input_data: list[float],
                 model: Callable[[list[float], list[float], dict[str, float]],
                                 list[float]],
                 params: dict[str, dict[str, float]],
                 labels: dict[str, str],
                 tcut: int): ...

def _log_prob(param_values: list[float],
              param_names: list[str],
              model: Callable[[list[float], list[float], dict[str, float]],
                              list[float]],
              time_data: list[float],
              input_data: list[float],
              tissue_data: list[float],
              param_bounds: dict[str, (float, float)]) -> float: ...

def task_tac_fit(task: OrderedDict[str, Any],
                 named_obj: dict[str, Any]): ...

def task_apply_correction(task: OrderedDict[str, Any],
                          named_obj: dict[str, Any]): ...

