import pytest
import numpy as np
from flash.flash import flash_calculation


def test_flash_simple_binary_case():
    z = np.array([0.5, 0.5])
    T = 78.0  # °C
    P = 760.0  # mmHg

    components = [
        {"A": 8.07131, "B": 1730.63, "C": 233.426},  # water
        {"A": 8.20417, "B": 1642.89, "C": 230.300},  # ethanol
    ]

    result = flash_calculation(z, T, P, components)
    x = np.array(result["x"])
    y = np.array(result["y"])
    beta = result["beta"]

    assert x.shape == (2,)
    assert y.shape == (2,)
    assert np.isclose(x.sum(), 1.0, atol=1e-6)
    assert np.isclose(y.sum(), 1.0, atol=1e-6)
    assert 0.0 <= beta <= 1.0
