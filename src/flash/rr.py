import numpy as np
from scipy.optimize import brentq
from typing import cast


def solve_rr(z, K) -> float:
    """
    Solve the Rachford-Rice equation for vapor fraction (beta).

    Args:
        z (array-like): overall mole fractions (must sum to 1)
        K (array-like): equilibrium ratios (same length as z)

    Returns:
        float: vapor fraction beta in [0.0, 1.0]
    """
    z = np.asarray(z, dtype=float)
    K = np.asarray(K, dtype=float)

    if not np.isclose(z.sum(), 1.0):
        raise ValueError(f"Mole fractions z must sum to 1 (got {z.sum():.6f})")

    if z.shape != K.shape:
        raise ValueError("z and K must have the same length")

    if np.allclose(K, 1.0):
        return 0.5
    if np.all(K < 1.0):
        return 0.0
    if np.all(K > 1.0):
        return 1.0

    def rachford_rice(beta: float) -> float:
        return float(np.sum(z * (K - 1.0) / (1.0 + beta * (K - 1.0))))

    beta = cast(float, brentq(rachford_rice, 0.0, 1.0, full_output=False))
    return beta
