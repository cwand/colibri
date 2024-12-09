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

