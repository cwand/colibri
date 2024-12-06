import SimpleITK as sitk
from datetime import datetime
from typing import Any, Optional, Union, OrderedDict

# From core.py

def get_acq_datetime(dicom_path: str) -> datetime: ...

def shift_time(y: list[float], t: list[float],
               deltat: float) -> list[float]: ...

def save_tac(tac: dict[Union[str, int], list[float]], path: str): ...

def load_tac(path: str) -> dict[str, list[float]]: ...

# From image.py

def load_dynamic_series(dicom_path: str) \
        -> dict[str, Any]: ...

def resample_series_to_reference(series: list[sitk.Image],
                                 ref: sitk.Image) -> list[sitk.Image]: ...

def series_roi_means(series: list[sitk.Image],
                     roi: sitk.Image) -> dict[int, list[float]]: ...

def lazy_series_roi_means(series_path: str,
                          roi_path: str,
                          resample: Optional[str] = ...,
                          labels: Optional[dict[str, str]] = ...)\
        -> dict[Union[str, int], list[float]]: ...

# From model.py

def model_step(t: list[float], in_func: list[float],
               amp: float, extent: float) -> list[float]: ...

def model_step_2(t: list[float],
                 in_func: list[float],
                 amp1: float,
                 extent1: float,
                 amp2: float,
                 extent2: float) -> list[float]: ...

def model_step_fermi(t: list[float],
                     in_func: list[float],
                     amp1: float,
                     extent1: float,
                     width1: float,
                     amp2: float,
                     extent2: float,
                     width2: float) -> list[float]: ...

def model_fermi_2(t: list[float],
                  in_func: list[float],
                  amp1: float,
                  extent1: float,
                  width1: float,
                  amp2: float,
                  extent2: float,
                  width2: float) -> list[float]: ...

def model_patlak(t: list[float],
                 in_func: list[float],
                 k1: float,
                 v0: float) -> list[float]: ...

# From tasks.py

def task_roi_means(task: OrderedDict[str, Any]): ...

def task_tac_fit(task: OrderedDict[str, Any]): ...