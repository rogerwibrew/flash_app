import numpy as np
from typing import Any
from .thermo import equilibrium_ratios
from .rr import solve_rr


def calc_xi(z: np.ndarray, beta: float, K: np.ndarray) -> np.ndarray:
    return z / (1.0 + beta * (K - 1.0))


def calc_yi(x: np.ndarray, K: np.ndarray) -> np.ndarray:
    return K * x


def flash_calculation(
    z, T: float, P: float, components: list[dict[str, Any]]
) -> dict[str, Any]:
    z = np.asarray(z, dtype=float)
    K = equilibrium_ratios(T, P, components)
    beta = solve_rr(z, K)

    x = calc_xi(z, beta, K)
    y = calc_yi(x, K)

    # normalize to remove numerical drift
    x /= x.sum()
    y /= y.sum()

    return {"x": x.tolist(), "y": y.tolist(), "beta": float(beta)}
