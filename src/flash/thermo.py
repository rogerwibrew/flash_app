import numpy as np


def antoine_pressure(T: float, A: float, B: float, C: float) -> float:
    """
    Saturation pressure (mmHg) using Antoine equation.
    """
    return 10 ** (A - B / (T + C))


def equilibrium_ratios(T: float, P: float, components: list[dict]) -> np.ndarray:
    """
    Compute equilibrium ratios (K-values).
    """
    Ks = []
    for comp in components:
        psat = antoine_pressure(T, comp["A"], comp["B"], comp["C"])
        Ks.append(psat / P)
    return np.array(Ks, dtype=float)
