import SimpleITK as sitk
from datetime import datetime
from typing import Any, Optional, Union

from colibri import tasks, model

# From core.py

def get_acq_datetime(dicom_path: str) -> datetime: ...

def shift_time(y: list[float], t: list[float],
               deltat: float) -> list[float]: ...

def save_table(table: dict[Union[str, int], list[float]], path: str): ...

def load_table(path: str) -> dict[str, list[float]]: ...

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
                          labels: Optional[dict[str, str]] = ...,
                          ignore: Optional[list[str]] = ...,
                          frame_dur: bool = ...)\
        -> dict[Union[str, int], list[float]]: ...

def segment_volume(roi: sitk.Image) -> dict[str, float]: ...
