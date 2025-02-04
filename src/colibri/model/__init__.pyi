# From model.py

def model_step(
        t: list[float], in_func: list[float],
        **kwargs: float) -> list[float]: ...

def model_step_2(
        t: list[float], in_func: list[float],
        **kwargs: float) -> list[float]: ...

def model_step_fermi(
        t: list[float], in_func: list[float],
        **kwargs: float) -> list[float]: ...

def model_fermi_2(
        t: list[float], in_func: list[float],
        **kwargs: float) -> list[float]: ...

def model_patlak(
        t: list[float], in_func: list[float],
        **kwargs: float) -> list[float]: ...

